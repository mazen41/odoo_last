# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    engineering_package_id = fields.Many2one(
        'engineering.package', 
        string='الباقة الهندسية (Package)',
        domain="[('building_type', 'in', [building_type, 'all']), ('active', '=', True)]"
    )
    
    package_features_html = fields.Html(
        string="مميزات الباقة (Package Features)", 
        compute="_compute_package_features_html",
        store=False,
        sanitize=False
    )

    @api.depends('engineering_package_id', 'engineering_package_id.feature_ids')
    def _compute_package_features_html(self):
        """ Generates an HTML list of features for the selected package. """
        for order in self:
            if not order.engineering_package_id or not order.engineering_package_id.feature_ids:
                order.package_features_html = False
                continue

            res = '<ul style="list-style: none; padding: 0; margin: 0; text-align: right; direction: rtl;">'
            for feature in order.engineering_package_id.feature_ids:
                if feature.included:
                    res += f'<li style="margin-bottom: 10px;"><span style="color: green; margin-left: 8px;">✔</span> {feature.name}</li>'
                else:
                    res += f'<li style="margin-bottom: 10px; color: #999;"><span style="color: red; margin-left: 8px;">✘</span> <s>{feature.name}</s></li>'
            res += '</ul>'
            order.package_features_html = res

    @api.onchange('engineering_package_id')
    def _onchange_engineering_package_id(self):
        """ Automatically adds the package product to the order lines. """
        if not self.engineering_package_id:
            return

        package = self.engineering_package_id
        if not package.product_id:
            raise UserError(_("This package '%s' does not have a related product. Please create one from the package form.") % package.name)

        # Clear existing lines and add the package product
        self.order_line = [(5, 0, 0)]
        self.order_line = [(0, 0, {
            'product_id': package.product_id.id,
            'name': package.product_id.name,
            'product_uom_qty': 1,
            'price_unit': package.list_price,
        })]
