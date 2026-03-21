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
#  NEW MODEL FOR ENGINEERING PACKAGE
# ==============================================================================
class EngineeringPackage(models.Model):
    _name = 'engineering.package'
    _description = 'Engineering Package'

    name = fields.Char(string="اسم الباقة الهندسية", required=True)
    code = fields.Char(string="كود الباقة", copy=False, default='جديد')

# ==============================================================================
#  RES PARTNER (Customer Profile)
# ==============================================================================
class ResPartner(models.Model):
    _inherit = 'res.partner'

    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار", tracking=True)
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة", tracking=True)
    civil_number = fields.Char(string="الرقم المدني (Civil ID)")
    plot_no = fields.Char(string="رقم القسيمة (Plot)")
    block_no = fields.Char(string="القطعة (Block)")
    street_no = fields.Char(string="الضاحيه")
    area = fields.Char(string="مساحة الارض (Area)")
    
    # أضفنا الحقل هنا ليتم حفظه في بيانات العميل الأساسية
    electricity_receipt = fields.Char(string="إيصال تيار كهرباء")

    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة")
    region_id = fields.Many2one('kuwait.region', string="المنطقة (Region)")


# ==============================================================================
#  SALE ORDER
# ==============================================================================
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار", store=True)
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة", store=True)

    plot_no = fields.Char(string="رقم القسيمة", store=True)
    block_no = fields.Char(string="القطعة", store=True)
    street_no = fields.Char(string="الضاحيه", store=True)
    area = fields.Char(string="مساحة الارض", store=True)
    
    # الحقل المطلوب في عرض السعر
    electricity_receipt = fields.Char(string="إيصال تيار كهرباء", store=True)

    governorate_id = fields.Many2one('kuwait.governorate', string="المحافظة", store=True)
    region_id = fields.Many2one('kuwait.region', string="المنطقة (Region)", store=True)

    engineering_package_id = fields.Many2one(
        'engineering.package', 
        string="Engineering Package",
        help="Select the engineering package for this sale order",
        store=True,
    )

    # تحديث الدالة لتسحب حقل إيصال الكهرباء من العميل تلقائياً
    @api.onchange('partner_id')
    def _onchange_partner_id_engineering_fields(self):
        if self.partner_id:
            self.building_type = self.partner_id.building_type
            self.service_type = self.partner_id.service_type
            self.plot_no = self.partner_id.plot_no
            self.block_no = self.partner_id.block_no
            self.street_no = self.partner_id.street_no
            self.area = self.partner_id.area
            self.governorate_id = self.partner_id.governorate_id
            self.region_id = self.partner_id.region_id
            # سحب القيمة من ملف العميل
            self.electricity_receipt = self.partner_id.electricity_receipt


# ==============================================================================
#  PROJECT PROJECT (لحل مشكلة الـ RPC Error)
# ==============================================================================
class ProjectProject(models.Model):
    _inherit = 'project.project'

    # يجب إضافة الحقل هنا أيضاً لأن دالة إنشاء المشروع تحاول إرسال القيمة لهذا الموديل
    electricity_receipt = fields.Char(string="إيصال تيار كهرباء")
    
    # الحقول الأخرى التي قد تحتاجها في المشروع لتجنب أخطاء مشابهة
    plot_no = fields.Char(string="رقم القسيمة")
    block_no = fields.Char(string="القطعة")
    street_no = fields.Char(string="الضاحيه")
    area = fields.Char(string="المساحة")
    building_type = fields.Selection([('residential', 'سكن خاص'), ('investment', 'استثماري'), ('commercial', 'تجاري'), ('industrial', 'صناعي'), ('cooperative', 'جمعيات وتعاونيات'), ('mosque', 'مساجد'), ('hangar', 'مخازن / شبرات'), ('farm', 'مزارع')], string="نوع العقار")
    service_type = fields.Selection([('new_construction', 'بناء جديد'), ('demolition', 'هدم'), ('modification', 'تعديل'), ('addition', 'اضافة'), ('addition_modification', 'تعديل واضافة'), ('supervision_only', 'إشراف هندسي فقط'), ('renovation', 'ترميم'), ('internal_partitions', 'قواطع داخلية'), ('shades_garden', 'مظلات / حدائق')], string="نوع الخدمة")
