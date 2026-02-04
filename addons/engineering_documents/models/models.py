# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

# TASK 4.2 – Project Documents Model
class EngineeringProjectDocument(models.Model):
    _name = 'engineering.project.document'
    _description = 'Engineering Project Document'
    _order = 'sent_date desc'

    name = fields.Char(string='Document Name', required=True)
    quotation_id = fields.Many2one('sale.order', string='Related Quotation', ondelete='set null')
    project_id = fields.Many2one('project.project', string='Related Project', ondelete='set null')
    
    # حقل لرفع الملف (للمستندات الكبيرة)
    pdf_file = fields.Binary(string="PDF File", required=True)
    pdf_filename = fields.Char(string="Filename")
    
    sent_date = fields.Datetime(string='Sent Date', readonly=True)
    sent_by_id = fields.Many2one('res.users', string='Sent By', readonly=True)
    
    customer_id = fields.Many2one('res.partner', string='Customer', related='quotation_id.partner_id', readonly=True, store=True)

    # TASK 4.3 – Send Button (WhatsApp Redirect)
    def action_generate_whatsapp_redirect(self):
        self.ensure_one()
        customer_phone = self.customer_id.phone
        
        if not customer_phone:
            raise UserError(_("Customer phone number is missing on the contact card."))

        # تنظيف رقم الهاتف وإزالة أي مسافات أو رموز غير ضرورية
        cleaned_phone = ''.join(filter(str.isdigit, customer_phone))
        
        # رسالة تلقائية للعميل
        message = _("Please review the attached contract for project: %s. Thank you." % self.quotation_id.name)
        
        # بناء رابط WhatsApp (الـ PDF يجب إرساله يدويًا)
        # Odoo لا يستطيع إرسال المرفق مباشرة بدون API
        whatsapp_url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (cleaned_phone, message)
        
        # تسجيل عملية الإرسال
        self.write({
            'sent_date': fields.Datetime.now(),
            'sent_by_id': self.env.user.id,
        })
        
        # إعادة توجيه المستخدم
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_url,
            'target': 'new', # لفتح الرابط في نافذة جديدة
        }