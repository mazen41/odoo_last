# -*- coding: utf-8 -*-
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_engineering_package = fields.Boolean(string='باقة هندسية (Engineering Package)', default=False)
    engineering_package_id = fields.Many2one('engineering.package', string='الباقة المرتبطة')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    engineering_package_id = fields.Many2one('engineering.package', string='الباقة المرتبطة')
