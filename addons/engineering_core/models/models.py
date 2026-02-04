# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # --- EDITED: Changed from Char to Selection ---
    building_type = fields.Selection([
        ('residential', 'Residential – Private Housing'),
        ('investment', 'Investment Building'),
        ('commercial', 'Commercial Building'),
        ('industrial', 'Industrial Building'),
        ('cooperative', 'Cooperative / Associations'),
        ('mosque', 'Mosques'),
        ('hangar', 'Hangar'),
        ('farm', 'Farms')
    ], string="Building Type", tracking=True)

    # --- EDITED: Changed from Char to Selection ---
    service_type = fields.Selection([
        ('new_construction', 'New Construction'),
        ('demolition', 'Demolition'),
        ('modification', 'Modification'),
        ('extension', 'Extension'),
        ('extension_modification', 'Extension & Modification'),
        ('supervision_only', 'Engineering Supervision Only'),
        ('renovation', 'Renovation'),
        ('internal_partitions', 'Internal Partitions'),
        ('shades_garden', 'Shades / Garden Permit (Residential)')
    ], string="Service Type", tracking=True)

    civil_number = fields.Char(string="Civil Number")
    plot_no = fields.Char(string="Plot No.")
    block_no = fields.Char(string="Block No.")
    area = fields.Char(string="Area")


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    # --- EDITED: Changed from Char to Selection ---
    building_type = fields.Selection([
        ('residential', 'Residential – Private Housing'),
        ('investment', 'Investment Building'),
        ('commercial', 'Commercial Building'),
        ('industrial', 'Industrial Building'),
        ('cooperative', 'Cooperative / Associations'),
        ('mosque', 'Mosques'),
        ('hangar', 'Hangar'),
        ('farm', 'Farms')
    ], string="Building Type")

    # --- EDITED: Changed from Char to Selection ---
    service_type = fields.Selection([
        ('new_construction', 'New Construction'),
        ('demolition', 'Demolition'),
        ('modification', 'Modification'),
        ('extension', 'Extension'),
        ('extension_modification', 'Extension & Modification'),
        ('supervision_only', 'Engineering Supervision Only'),
        ('renovation', 'Renovation'),
        ('internal_partitions', 'Internal Partitions'),
        ('shades_garden', 'Shades / Garden Permit (Residential)')
    ], string="Service Type")

    plot_no = fields.Char(string="Plot No.")
    block_no = fields.Char(string="Block No.")
    area = fields.Char(string="Area")


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    # --- EDITED: Changed from Char to Selection ---
    # The `related` attribute works perfectly with Selection fields.
    building_type = fields.Selection(related='opportunity_id.building_type', readonly=False, store=True)
    service_type = fields.Selection(related='opportunity_id.service_type', readonly=False, store=True)

    plot_no = fields.Char(string="Plot No.", related='opportunity_id.plot_no', readonly=False, store=True)
    block_no = fields.Char(string="Block No.", related='opportunity_id.block_no', readonly=False, store=True)
    area = fields.Char(string="Area", related='opportunity_id.area', readonly=False, store=True)