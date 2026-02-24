# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

# --- YOUR EXISTING CODE (Kept as is) ---
class EngineeringProjectDocument(models.Model):
    _name = 'engineering.project.document'
    _description = 'Engineering Project Document'
    _order = 'sent_date desc'

    name = fields.Char(string='Document Name', required=True)
    quotation_id = fields.Many2one('sale.order', string='Related Quotation', ondelete='set null')
    project_id = fields.Many2one('project.project', string='Related Project', ondelete='set null')
    pdf_file = fields.Binary(string="PDF File", required=True)
    pdf_filename = fields.Char(string="Filename")
    sent_date = fields.Datetime(string='Sent Date', readonly=True)
    sent_by_id = fields.Many2one('res.users', string='Sent By', readonly=True)
    customer_id = fields.Many2one('res.partner', string='Customer', related='quotation_id.partner_id', readonly=True, store=True)

    def action_generate_whatsapp_redirect(self):
        self.ensure_one()
        customer_phone = self.customer_id.phone
        if not customer_phone:
            raise UserError(_("Customer phone number is missing."))
        cleaned_phone = ''.join(filter(str.isdigit, customer_phone))
        message = _("Please review the attached contract for project: %s." % self.quotation_id.name)
        whatsapp_url = "https://web.whatsapp.com/send?phone=%s&text=%s" % (cleaned_phone, message)
        self.write({'sent_date': fields.Datetime.now(), 'sent_by_id': self.env.user.id})
        return {'type': 'ir.actions.act_url', 'url': whatsapp_url, 'target': 'new'}

# --- NEW: Logic to Print the Correct Contract ---
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_print_engineering_contract(self):
        self.ensure_one()
        # Logic: If service is 'Supervision Only', print Supervision Contract.
        # Otherwise, print Design & Licensing Contract.
        
        if self.service_type == 'supervision_only':
            return self.env.ref('engineering_documents.action_report_supervision_contract').report_action(self)
        else:
            return self.env.ref('engineering_documents.action_report_design_contract').report_action(self)
