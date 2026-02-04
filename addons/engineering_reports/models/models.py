# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

# TASK 9 – إدارة تقارير الإشراف (Site Visit Report Model)
class EngineeringSiteVisit(models.Model):
    _name = 'engineering.site.visit'
    _description = 'Site Visit Report'
    _order = 'visit_date desc'

    name = fields.Char(string='Report Title', required=True, default=lambda self: _('Site Visit Report - %s' % fields.Date.today()))
    
    # الروابط الرئيسية
    project_id = fields.Many2one('project.project', string='Project', required=True, ondelete='cascade')
    task_id = fields.Many2one('project.task', string='Related Task', ondelete='set null')
    customer_id = fields.Many2one('res.partner', string='Customer', related='project_id.partner_id', readonly=True, store=True)

    # بيانات التقرير
    visit_date = fields.Datetime(string='Visit Date', default=fields.Datetime.now, required=True)
    visitor_id = fields.Many2one('res.users', string='Engineer/User', default=lambda self: self.env.user, required=True)
    
    # Upload Site Visit Report (PDF)
    pdf_report = fields.Binary(string="PDF Report File", attachment=True)
    pdf_filename = fields.Char(string="Filename")

    # زر إرسال التقرير للمالك (Send Report Button)
    sent_to_customer = fields.Boolean(string='Sent to Customer', readonly=True)
    sent_date = fields.Datetime(string='Sent Date', readonly=True)

    # TASK 9.2 – Send Report Button Logic
    def action_generate_whatsapp_redirect_report(self):
        self.ensure_one()
        customer_phone = self.customer_id.phone
        
        if not customer_phone:
            raise UserError(_("Customer phone number is missing on the project/customer card."))
        if not self.pdf_report:
            raise UserError(_("Please upload the PDF report file before sending."))

        # تنظيف رقم الهاتف وإزالة أي مسافات أو رموز غير ضرورية
        cleaned_phone = ''.join(filter(str.isdigit, customer_phone))
        
        # رسالة تلقائية للعميل
        message = _("Please review the attached Site Visit Report: %s" % self.name)
        
        # بناء رابط WhatsApp
        whatsapp_url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (
            cleaned_phone, 
            message.replace(' ', '%20') # ترميز المسافات
        )
        
        # تسجيل عملية الإرسال
        self.write({
            'sent_to_customer': True,
            'sent_date': fields.Datetime.now(),
        })
        
        # إعادة توجيه المستخدم
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new', # لفتح الرابط في نافذة جديدة
        }


# ربط نموذج المهمة بتقرير الزيارة
class ProjectTask(models.Model):
    _inherit = 'project.task'
    
    site_visit_report_ids = fields.One2many(
        'engineering.site.visit', 
        'task_id', 
        string='Site Visit Reports'
    )
    
    # دالة لفتح نافذة إنشاء تقرير زيارة جديد
    def action_create_site_visit_report(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'engineering.site.visit',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'new',
            'context': {
                'default_task_id': self.id,
                'default_project_id': self.project_id.id,
                'default_name': _('Site Visit Report - %s' % self.project_id.name),
            },
        }