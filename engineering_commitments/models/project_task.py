# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class ProjectTask(models.Model):
    _inherit = 'project.task'

    commitment_ids = fields.One2many(
        'engineering.task.commitment',
        'task_id',
        string='Engineering Commitments (التعهدات)'
    )

    # ---------------------------
    # LOAD TEMPLATES
    # ---------------------------
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

    # ---------------------------
    # GENERATE REQUESTS
    # ---------------------------
    def action_generate_commitments_pdf(self):
        self.ensure_one()

        required_commitments = self.commitment_ids.filtered(lambda p: p.is_required)
        if not required_commitments:
            raise UserError(_("Please mark at least one commitment as 'Required' first."))

        if not self.project_id.partner_id:
            raise UserError(_("Project must have a customer."))

        role_customer = self.env.ref('sign.sign_item_role_customer', raise_if_not_found=False)
        current_partner = self.env.user.partner_id

        replacements = {
            'Name': self.project_id.partner_id.name or "NO NAME",
            'Date': fields.Date.context_today(self).strftime("%Y/%m/%d"),
        }

        for commitment in required_commitments:

            if commitment.sign_request_id and commitment.sign_request_id.state == 'signed':
                continue

            if commitment.sign_request_id and commitment.sign_request_id.state != 'canceled':
                commitment.sign_request_id.cancel()
                commitment.sign_request_id = False

            template = commitment.sign_template_id

            roles = list(set(template.sign_item_ids.mapped('responsible_id')))
            signers = []

            for role in roles:
                partner = self.project_id.partner_id if (role_customer and role.id == role_customer.id) else current_partner

                signers.append((0, 0, {
                    'role_id': role.id,
                    'partner_id': partner.id,
                }))

            if not signers:
                raise UserError(_("Template has no signers."))

            sign_request = self.env['sign.request'].create({
                'template_id': template.id,
                'reference': f"{template.name} - {self.name}",
                'request_item_ids': signers,
            })

            # Fill fields
            for item in template.sign_item_ids:
                if item.name in replacements:
                    signer = sign_request.request_item_ids.filtered(
                        lambda r: r.role_id.id == item.responsible_id.id
                    )
                    if signer:
                        self.env['sign.request.item.value'].sudo().create({
                            'sign_request_item_id': signer[0].id,
                            'sign_item_id': item.id,
                            'value': replacements[item.name],
                        })

            commitment.sign_request_id = sign_request.id

        return True


# =========================================================
# COMMITMENT MODEL BUTTON (IMPORTANT)
# =========================================================
class EngineeringTaskCommitment(models.Model):
    _name = 'engineering.task.commitment'
    _description = 'Task Commitment'

    task_id = fields.Many2one('project.task')
    sign_template_id = fields.Many2one('sign.template', required=True)
    sign_request_id = fields.Many2one('sign.request')
    is_required = fields.Boolean("Required")

    # 🔥 DIRECT SIGN BUTTON
    def action_sign_now(self):
        self.ensure_one()

        if not self.sign_request_id:
            raise UserError(_("No generated document yet."))

        request = self.sign_request_id

        request_item = request.request_item_ids.filtered(
            lambda r: r.partner_id.id == self.env.user.partner_id.id
        )

        if not request_item:
            raise UserError(_("You are not assigned to sign this document."))

        return {
            'type': 'ir.actions.act_url',
            'url': f'/sign/document/{request.id}/{request_item.access_token}',
            'target': 'new',
        }
