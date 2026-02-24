# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_type = fields.Selection([
        ('residential', 'سكن خاص (Private Housing)'),
        ('investment', 'استثماري (Investment Building)'),
        ('commercial', 'تجاري (Commercial Building)'),
        ('industrial', 'صناعي (Industrial Building)'),
        ('cooperative', 'جمعيات وتعاونيات (Cooperative)'),
        ('mosque', 'مساجد (Mosques)'),
        ('hangar', 'مخازن / شبرات (Hangar)'),
        ('farm', 'مزارع (Farms)')
    ], string="نوع العقار (Building Type)", tracking=True)

    service_type = fields.Selection([
        ('new_construction', 'بناء جديد (New Construction)'),
        ('demolition', 'هدم (Demolition)'),
        ('modification', 'تعديل (Modification)'),
        ('extension', 'توسعة (Extension)'),
        ('extension_modification', 'تعديل وتوسعة (Extension & Modification)'),
        ('supervision_only', 'إشراف هندسي فقط (Supervision Only)'),
        ('renovation', 'ترميم (Renovation)'),
        ('internal_partitions', 'قواطع داخلية (Internal Partitions)'),
        ('shades_garden', 'مظلات / حدائق (Shades / Garden)')
    ], string="نوع الخدمة (Service Type)", tracking=True)

    civil_number = fields.Char(string="الرقم المدني (Civil ID)")
    plot_no = fields.Char(string="رقم القسيمة (Plot)")
    block_no = fields.Char(string="القطعة (Block)")
    street_no = fields.Char(string="الشارع (Street)")  # Added based on Contract requirements
    area = fields.Char(string="المساحة (Area)")


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    building_type = fields.Selection([
        ('residential', 'سكن خاص (Private Housing)'),
        ('investment', 'استثماري (Investment Building)'),
        ('commercial', 'تجاري (Commercial Building)'),
        ('industrial', 'صناعي (Industrial Building)'),
        ('cooperative', 'جمعيات وتعاونيات (Cooperative)'),
        ('mosque', 'مساجد (Mosques)'),
        ('hangar', 'مخازن / شبرات (Hangar)'),
        ('farm', 'مزارع (Farms)')
    ], string="نوع العقار (Building Type)")

    service_type = fields.Selection([
        ('new_construction', 'بناء جديد (New Construction)'),
        ('demolition', 'هدم (Demolition)'),
        ('modification', 'تعديل (Modification)'),
        ('extension', 'توسعة (Extension)'),
        ('extension_modification', 'تعديل وتوسعة (Extension & Modification)'),
        ('supervision_only', 'إشراف هندسي فقط (Supervision Only)'),
        ('renovation', 'ترميم (Renovation)'),
        ('internal_partitions', 'قواطع داخلية (Internal Partitions)'),
        ('shades_garden', 'مظلات / حدائق (Shades / Garden)')
    ], string="نوع الخدمة (Service Type)")

    plot_no = fields.Char(string="رقم القسيمة (Plot)")
    block_no = fields.Char(string="القطعة (Block)")
    street_no = fields.Char(string="الشارع (Street)")
    area = fields.Char(string="المساحة (Area)")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # Related fields allow auto-filling from the Opportunity (CRM)
    building_type = fields.Selection(related='opportunity_id.building_type', readonly=False, store=True, string="نوع العقار")
    service_type = fields.Selection(related='opportunity_id.service_type', readonly=False, store=True, string="نوع الخدمة")

    plot_no = fields.Char(related='opportunity_id.plot_no', readonly=False, store=True, string="رقم القسيمة")
    block_no = fields.Char(related='opportunity_id.block_no', readonly=False, store=True, string="القطعة")
    street_no = fields.Char(related='opportunity_id.street_no', readonly=False, store=True, string="الشارع")
    area = fields.Char(related='opportunity_id.area', readonly=False, store=True, string="المساحة")
