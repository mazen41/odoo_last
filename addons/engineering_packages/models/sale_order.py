# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    package_id = fields.Many2one('engineering.package', string='الباقة المختارة (Selected Package)')

    @api.onchange('package_id')
    def _onchange_package_id(self):
        """When package is selected, add package products to order lines"""
        if self.package_id and self.package_id.product_line_ids:
            # Clear existing lines if needed (optional)
            new_lines = []
            for line in self.package_id.product_line_ids:
                new_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_qty': line.quantity,
                    'price_unit': line.price_unit,
                }))
            if new_lines:
                self.order_line = new_lines

    def action_add_package(self):
        """Action to open package selection wizard"""
        return {
            'type': 'ir.actions.act_window',
            'name': _('Select Package'),
            'res_model': 'engineering.package',
            'view_mode': 'tree,form',
            'target': 'new',
            'context': {
                'default_building_type': self.building_type or 'all',
            },
            'domain': [
                '|',
                ('building_type', '=', self.building_type),
                ('building_type', '=', 'all'),
            ],
        }
