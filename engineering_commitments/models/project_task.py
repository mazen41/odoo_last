# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, _, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    commitment_ids = fields.One2many(
        'engineering.task.commitment', 
        'task_id', 
        string='Engineering Commitments (التعهدات)'
    )

    def action_load_commitments(self):
        for task in self:
            building_type = getattr(task.project_id, 'building_type', False)
            if not building_type:
                domain = [('is_commitment', '=', True), ('building_type', '=', 'all')]
            else:
                domain = [('is_commitment', '=', True), ('building_type', 'in', [building_type, 'all'])]
            
            templates = self.env['sign.template'].search(domain)
            existing_template_ids = task.commitment_ids.mapped('sign_template_id.id')
            
            for template in templates:
                if template.id not in existing_template_ids:
                    self.env['engineering.task.commitment'].create({
                        'task_id': task.id,
                        'sign_template_id': template.id,
                    })

    def action_generate_commitments_pdf(self):
        self.ensure_one()

        required_commitments = self.commitment_ids.filtered(lambda p: p.is_required)
        if not required_commitments:
            raise UserError(_("Please mark at least one commitment as 'Required' first."))

        project = self.project_id
        if not project.partner_id:
            raise UserError(_("The project must have a Customer to generate documents."))

        role_customer = self.env.ref('sign.sign_item_role_customer', raise_if_not_found=False)
        
        # ==========================================
        # 1. GET VALUES (WITH "NO DATA" FALLBACKS FOR TESTING)
        # ==========================================
        val_name = project.partner_id.name or "NO NAME"
        val_date = fields.Date.context_today(self).strftime("%Y/%m/%d")
        val_gov = project.governorate_id.name if project.governorate_id else "NO GOV"
        val_region = project.region_id.name if project.region_id else "NO REGION"
        val_block = project.block_no or "NO BLOCK"
        val_plot = project.plot_no or "NO PLOT"
        val_street = project.street_no or "NO STREET"

        generated_requests = self.env['sign.request']

        for commitment in required_commitments:
            if commitment.sign_request_id and commitment.sign_request_id.state != 'canceled':
                generated_requests |= commitment.sign_request_id
                continue

            template = commitment.sign_template_id
            if not template.sign_item_ids:
                raise UserError(_(f"Template '{template.name}' has no fields/signature configured."))

            # 2. Define Signers
            roles = template.sign_item_ids.mapped('responsible_id')
            signers_list = []
            for role in roles:
                partner_id = project.partner_id.id if (role_customer and role.id == role_customer.id) else self.env.user.partner_id.id
                signers_list.append((0, 0, {
                    'role_id': role.id,
                    'partner_id': partner_id,
                }))

            # 3. Create Request
            sign_request = self.env['sign.request'].create({
                'template_id': template.id,
                'reference': f"{template.name} - {project.name}",
                'request_item_ids': signers_list,
            })

            # 4. BULLETPROOF AUTOFILL MATCHING
            for template_field in template.sign_item_ids:
                # Get the name and type, and make them lowercase to avoid case-sensitivity issues
                t_name = (template_field.name or '').lower()
                t_type = (template_field.type_id.name or '').lower()
                
                val_to_insert = False
                
                # Check if the word exists anywhere in the field name or type
                if 'date' in t_name or 'date' in t_type or 'تاريخ' in t_name or 'تاريخ' in t_type:
                    val_to_insert = val_date
                elif 'governorate' in t_name or 'governorate' in t_type:
                    val_to_insert = val_gov
                elif 'region' in t_name or 'region' in t_type:
                    val_to_insert = val_region
                elif 'block' in t_name or 'block' in t_type:
                    val_to_insert = val_block
                elif 'plot' in t_name or 'plot' in t_type:
                    val_to_insert = val_plot
                elif 'street' in t_name or 'street' in t_type:
                    val_to_insert = val_street
                elif 'name' in t_name or 'name' in t_type or 'اسم' in t_name or 'اسم' in t_type:
                    val_to_insert = val_name

                # If we found a match, forcefully write the value into the PDF box
                if val_to_insert:
                    signer_record = sign_request.request_item_ids.filtered(
                        lambda r: r.role_id.id == template_field.responsible_id.id
                    )
                    if signer_record:
                        self.env['sign.request.item.value'].sudo().create({
                            'sign_request_item_id': signer_record[0].id,
                            'sign_item_id': template_field.id,
                            'value': str(val_to_insert),
                        })

            commitment.sign_request_id = sign_request.id
            generated_requests |= sign_request

        if not generated_requests:
            return True

        action = self.env['ir.actions.actions']._for_xml_id('sign.sign_request_action')
        if len(generated_requests) == 1:
            action.update({'view_mode': 'form', 'res_id': generated_requests.id, 'views': [(False, 'form')]})
        else:
            action['domain'] = [('id', 'in', generated_requests.ids)]
        
        return action
