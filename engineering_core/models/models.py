# -*- coding: utf-8 -*-
from odoo import models, fields, api

# ==============================================================================
#  NEW MODELS FOR HIERARCHY
# ==============================================================================

class KuwaitGovernorate(models.Model):
    _name = 'kuwait.governorate'
    _description = 'Governorate'
    name = fields.Char(string="المحافظة", required=True)

class KuwaitRegion(models.Model):
    _name = 'kuwait.region'
    _description = 'Region'
    name = fields.Char(string="المنطقة", required=True)
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة", ondelete='cascade')


# ==============================================================================
#  RES PARTNER
# ==============================================================================
class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار", tracking=True)
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة", tracking=True)
    civil_number = fields.Char(string="الرقم المدني (Civil ID)")
    plot_no = fields.Char(string="رقم القسيمة (Plot)")
    block_no = fields.Char(string="القطعة (Block)")
    street_no = fields.Char(string="الشارع (Street)")
    area = fields.Char(string="مساحة الارض (Area)")
    
    # Updated to Many2one
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة")
    region_id = fields.Many2one('kuwait.region', string="المنطقة (Region)")


# ==============================================================================
#  CRM LEAD
# ==============================================================================
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار")
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة")
    plot_no = fields.Char(string="رقم القسيمة (Plot)")
    block_no = fields.Char(string="القطعة (Block)")
    street_no = fields.Char(string="الشارع (Street)")
    area = fields.Char(string="مساحة الارض (Area)")
    
    # Updated to Many2one
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة")
    region_id = fields.Many2one('kuwait.region', string="المنطقة (Region)")
    
    def _prepare_sale_order_values(self, partner, company, access_token):
        values = super()._prepare_sale_order_values(partner, company, access_token)
        values['building_type'] = self.building_type
        values['service_type'] = self.service_type
        values['plot_no'] = self.plot_no
        values['block_no'] = self.block_no
        values['street_no'] = self.street_no
        values['area'] = self.area
        values['governorate_id'] = self.governorate_id.id
        values['region_id'] = self.region_id.id
        return values


# ==============================================================================
#  SALE ORDER
# ==============================================================================
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار", store=True)
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة", store=True)

    plot_no = fields.Char(string="رقم القسيمة", store=True)
    block_no = fields.Char(string="القطعة", store=True)
    street_no = fields.Char(string="الشارع", store=True)
    area = fields.Char(string="مساحة الارض", store=True)
    
    # Updated to Many2one
    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة", store=True)
    region_id = fields.Many2one('kuwait.region', string="المنطقة (Region)", store=True)
