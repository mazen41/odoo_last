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

    # --------------------------------------------------
    # LOAD COMMITMENTS
    # --------------------------------------------------
    def action_load_commitments(self):
        for task in self:
            building_type = getattr(task.project_id, 'building_type', False)

            if not building_type:
                domain = [
                    ('is_commitment', '=', True),
                    ('building_type', '=', 'all')
                ]
            else:
                domain = [
                    ('is_commitment', '=', True),
                    ('building_type', 'in', [building_type, 'all'])
                ]

            templates = self.env['sign.template'].search(domain)
            existing_template_ids = task.commitment_ids.mapped('sign_template_id.id')

            for template in templates:
                if template.id not in existing_template_ids:
                    self.env['engineering.task.commitment'].create({
                        'task_id': task.id,
                        'sign_template_id': template.id,
                    })

    # --------------------------------------------------
    # GENERATE COMMITMENTS
    # --------------------------------------------------
    def action_generate_commitments_pdf(self):
        self.ensure_one()

        required_commitments = self.commitment_ids.filtered(lambda p: p.is_required)
        if not required_commitments:
            raise UserError(_("Please mark at least one commitment as 'Required' first."))

        project = self.project_id
        if not project.partner_id:
            raise UserError(_("The project must have a Customer to generate documents."))

        role_customer = self.env.ref('sign.sign_item_role_customer', raise_if_not_found=False)
        current_partner = self.env.user.partner_id

        replacements = {
            'Name': project.partner_id.name or "NO NAME",
            'Date': fields.Date.context_today(self).strftime("%Y/%m/%d"),
            'Governorate': project.governorate_id.name if project.governorate_id else "NO GOV",
            'Region': project.region_id.name if project.region_id else "NO REGION",
            'Block': project.block_no or "NO BLOCK",
            'Plot': project.plot_no or "NO PLOT",
            'Customer Signature Text': project.partner_id.name or "N/A",
            'Signature Date Text': fields.Date.context_today(self).strftime("%Y/%m/%d"),
            'Company Signature Text': self.env.user.company_id.name or "N/A",
        }

        generated_requests = self.env['sign.request']

        for commitment in required_commitments:

            # -------------------------------
            # Skip already signed
            # -------------------------------
            if commitment.sign_request_id and commitment.sign_request_id.state == 'signed':
                _logger.info(
                    f"Skipping {commitment.sign_template_id.name}, already signed."
                )
                generated_requests |= commitment.sign_request_id
                continue

            # -------------------------------
            # Cancel existing draft/sent
            # -------------------------------
            if commitment.sign_request_id and commitment.sign_request_id.state != 'canceled':
                _logger.info(
                    f"Canceling old request {commitment.sign_request_id.name}"
                )
                commitment.sign_request_id.cancel()
                commitment.sign_request_id = False

            template = commitment.sign_template_id

            # -------------------------------
            # Prepare signers
            # -------------------------------
            roles = template.sign_item_ids.mapped('responsible_id')
            roles = list(set(roles))  # remove duplicates

            signers_list_vals = []

            for role in roles:
                partner_to_assign = (
                    project.partner_id
                    if (role_customer and role.id == role_customer.id)
                    else current_partner
                )

                signers_list_vals.append((0, 0, {
                    'role_id': role.id,
                    'partner_id': partner_to_assign.id,
                }))

            if not signers_list_vals:
                raise UserError(_("No signers defined in the template."))

            # -------------------------------
            # Create sign request
            # -------------------------------
            sign_request = self.env['sign.request'].create({
                'template_id': template.id,
                'reference': f"{template.name} - {project.name}",
                'request_item_ids': signers_list_vals,
            })

            # -------------------------------
            # Fill template fields
            # -------------------------------
            for template_field in template.sign_item_ids:
                field_name = template_field.name

                if field_name in replacements:
                    value_to_insert = replacements[field_name]

                    signer_record = sign_request.request_item_ids.filtered(
                        lambda r: r.role_id.id == template_field.responsible_id.id
                    )

                    if signer_record:
                        self.env['sign.request.item.value'].sudo().create({
                            'sign_request_item_id': signer_record[0].id,
                            'sign_item_id': template_field.id,
                            'value': value_to_insert,
                        })

            # -------------------------------
            # OPTIONAL: Auto sign (SAFE WAY)
            # -------------------------------
            for request_item in sign_request.request_item_ids:
                try:
                    if hasattr(request_item, '_sign'):
                        request_item._sign()
                except Exception as e:
                    _logger.warning(f"Auto-sign failed: {e}")

            # -------------------------------
            # Link back to commitment
            # -------------------------------
            commitment.sign_request_id = sign_request.id
            generated_requests |= sign_request

        # -------------------------------
        # Open result
        # -------------------------------
        if not generated_requests:
            return True

        action = self.env['ir.actions.actions']._for_xml_id('sign.sign_request_action')

        if len(generated_requests) == 1:
            action.update({
                'view_mode': 'form',
                'res_id': generated_requests.id,
                'views': [(False, 'form')],
            })
        else:
            action['domain'] = [('id', 'in', generated_requests.ids)]

        return action
