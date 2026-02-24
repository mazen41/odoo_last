# -*- coding: utf-8 -*-
from odoo import models, fields, api

class EngineeringContractTemplate(models.Model):
    _name = 'engineering.contract.template'
    _description = 'Engineering Contract Template'
    _order = 'building_type, service_type, package_type'

    name = fields.Char(string='اسم القالب (Template Name)', required=True)
    
    building_type = fields.Selection([
        ('residential', 'سكن خاص (Private Housing)'),
        ('investment', 'استثماري (Investment Building)'),
        ('commercial', 'تجاري (Commercial Building)'),
        ('industrial', 'صناعي (Industrial Building)'),
        ('cooperative', 'جمعيات وتعاونيات (Cooperative)'),
        ('mosque', 'مساجد (Mosques)'),
        ('hangar', 'مخازن / شبرات (Hangar)'),
        ('farm', 'مزارع (Farms)'),
        ('garden', 'حدائق (Garden)'),
        ('shades', 'مظلات (Shades)'),
    ], string="نوع المبنى (Building Type)", required=True)

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
    ], string="نوع الخدمة (Service Type)", required=True)

    package_type = fields.Selection([
        ('basic', 'الباقة الأساسية (Basic Package)'),
        ('premium', 'الباقة المميزة (Premium Package)'),
        ('gold', 'الباقة الذهبية (Gold Package)'),
        ('supervision', 'باقة الإشراف (Supervision Package)'),
    ], string="نوع الباقة (Package Type)")

    # Contract Content
    contract_body = fields.Html(string='محتوى العقد (Contract Body)', sanitize=False)
    
    # Terms and Conditions
    terms_conditions = fields.Html(string='الشروط والأحكام (Terms & Conditions)')
    
    # Active flag
    active = fields.Boolean(default=True)

    @api.model
    def get_template_for_contract(self, building_type, service_type, package_type=False):
        """Find the best matching template for given parameters"""
        domain = [
            ('building_type', '=', building_type),
            ('service_type', '=', service_type),
            ('active', '=', True),
        ]
        if package_type:
            domain.append(('package_type', '=', package_type))
        
        template = self.search(domain, limit=1)
        if not template and package_type:
            # Try without package_type
            domain = [
                ('building_type', '=', building_type),
                ('service_type', '=', service_type),
                ('active', '=', True),
            ]
            template = self.search(domain, limit=1)
        return template
