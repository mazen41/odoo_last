# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class ProjectProject(models.Model):
    _inherit = 'project.project'

    sale_order_id = fields.Many2one('sale.order', string='Source Quotation', readonly=True)
    
    # حقل جديد لربط مستندات المشروع
    document_ids = fields.One2many(
        'engineering.project.document', 
        'project_id', 
        string='Project Documents'
    )
    def action_create_and_send_contract_from_project(self):
        self.ensure_one()
        
        # 1. إنشاء مستند مشروع جديد وفتح شاشته
        new_doc = self.env['engineering.project.document'].create({
            'name': _("Contract for Project: %s" % self.name),
            'project_id': self.id,
            'quotation_id': self.sale_order_id.id,
        })
        
        # 2. فتح شاشة المستند الجديد ليقوم المستخدم برفع الملف وإرساله
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'engineering.project.document',
            'res_id': new_doc.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': self.env.context,
        }
# ... بعد الكلاس ProjectProject 

class ProjectTask(models.Model):
    _inherit = 'project.task'

    # دالة زر العودة إلى المشروع الأب (action_view_parent_project)
    def action_view_parent_project(self):
        self.ensure_one()
        if not self.project_id:
            raise UserError(_("This task is not linked to any Project."))
        
        # الانتقال إلى شاشة المشروع
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
            'view_mode': 'form',
            'views': [(self.env.ref('project.edit_project').id, 'form')],
            'target': 'current',
        }
        
    # دالة زر إرسال العقد من شاشة المهمة (الآن في مكانها الصحيح)
    def action_create_and_send_contract_from_task(self):
        self.ensure_one()
        
        if not self.project_id:
            raise UserError(_("This task must be linked to a Project to send a contract."))
            
        # 1. إنشاء مستند مشروع جديد وفتح شاشته
        new_doc = self.env['engineering.project.document'].create({
            # Project_id هنا تعود على المشروع الأب
            'name': _("Contract for Project: %s (via Task)" % self.project_id.name),
            'project_id': self.project_id.id,
            'quotation_id': self.project_id.sale_order_id.id,
        })
        
        # 2. فتح شاشة المستند الجديد ليقوم المستخدم برفع الملف وإرساله
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'engineering.project.document',
            'res_id': new_doc.id,
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': self.env.context,
        }