# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError # Import ValidationError too for robustness

_logger = logging.getLogger(__name__)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    commitment_ids = fields.One2many(
        'engineering.task.commitment', 
        'task_id', 
        string='Engineering Commitments (التعهدات)'
    )

    def action_load_commitments(self):
        """ Loads Sign templates based on the project's building type """
        # This method remains unchanged.
        # It's not directly used by the TEST code below, but kept for completeness.
        for task in self:
            building_type = task.project_id.building_type if hasattr(task.project_id, 'building_type') else False
            
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
        """ 
        TEMPORARY WORKAROUND VERSION: 
        Attempts to create a single Sign Request. If the core Odoo Sign module fails,
        it catches the error and provides a user-friendly message for the meeting.
        """
        self.ensure_one()

        project = self.project_id
        if not project.partner_id:
            raise UserError(_("The project must have a Customer to generate documents. (يجب تحديد عميل للمشروع)"))

        role_customer = self.env.ref('sign.sign_item_role_customer', raise_if_not_found=False)
        if not role_customer:
            raise UserError(_("Error: The 'Customer' role could not be found in the Sign application. Please check its configuration."))

        replacements = {
            'Name': project.partner_id.name or "Test Customer",
            'Date': fields.Date.context_today(self).strftime("%Y/%m/%d"),
            'Governorate': project.governorate_id.name if hasattr(project, 'governorate_id') and project.governorate_id else "",
            'Region': project.region_id.name if hasattr(project, 'region_id') and project.region_id else "",
            'Block': project.block_no or "" if hasattr(project, 'block_no') else "",
            'Plot': project.plot_no or "" if hasattr(project, 'plot_no') else "",
            'Street': project.street_no or "" if hasattr(project, 'street_no') else "",
        }

        # --- TEST-SPECIFIC CODE: Use the Odoo Native PDF Template ---
        test_template_name = '__TEST__ Odoo Native PDF Template' # Ensure this matches your template name
        template = self.env['sign.template'].search([('name', '=', test_template_name)], limit=1)
        if not template:
            raise UserError(_(f"TEST FAILED: Template '{test_template_name}' not found! "
                              f"Please ensure it's created as per instructions."))

        _logger.info(f"Processing TEST commitment for template: {template.name} (ID: {template.id})")
        _logger.info(f"Number of sign items on TEST template before creating request: {len(template.sign_item_ids)}")

        if not template.sign_item_ids:
            _logger.warning(f"TEST FAILED: Template '{template.name}' has no sign items defined. "
                            f"Please ensure you dragged at least ONE Signature field onto it. Skipping.")
            return True # Indicates the test template itself is misconfigured


        # --- CATCH THE ERROR HERE FOR THE MEETING ---
        try:
            # 1. Create the Sign Request from the template.
            sign_request = self.env['sign.request'].create({
                'template_id': template.id,
                'reference': f"{template.name} - {project.name} (TEST REQUEST)",
            })
            
            _logger.info(f"Created sign request {sign_request.id} from TEST template {template.name}.")
            _logger.info(f"Number of request items on the NEWLY CREATED TEST sign request: {len(sign_request.request_item_ids)}")

            # This check will likely not be hit, as the error occurs *during* the create call itself
            if not sign_request.request_item_ids:
                _logger.error(
                    f"TEST FAILED UNEXPECTEDLY: Sign request {sign_request.id} (from TEST template '{template.name}') "
                    f"has NO items after creation, but no direct UserError was raised. This is highly unusual. "
                    f"Deleting the empty sign request."
                )
                sign_request.unlink()
                raise UserError(_("A critical error occurred while preparing the document (no items generated). Please contact support."))


            # 2. Assign the partner to the items with the 'Customer' role.
            customer_items = sign_request.request_item_ids.filtered(
                lambda item: item.role_id.id == role_customer.id
            )
            if customer_items:
                customer_items.write({'partner_id': project.partner_id.id})
            else:
                _logger.warning(f"No customer-assigned items found for TEST sign request {sign_request.id}. (Ensure Signature field is assigned to Customer role)")

            # 3. Loop through items to fill values (only if they match a replacement key).
            for item in sign_request.request_item_ids:
                if item.name and item.name in replacements:
                    item.write({'value': replacements[item.name]})

            # 4. Send the request.
            sign_request.action_sent()
            
            # Return an action to open the generated TEST document for the user
            action = self.env['ir.actions.actions']._for_xml_id('sign.sign_request_action')
            action.update({
                'view_mode': 'form',
                'res_id': sign_request.id,
                'views': [(False, 'form')],
            })
            _logger.info(f"Returning action for generated TEST request: {sign_request.id}")
            return action

        except (UserError, ValidationError) as e:
            # Catch the specific error text
            if "A valid sign request needs at least one sign request item" in str(e):
                _logger.error(
                    f"Critical Odoo Sign module error encountered during sign request creation for template '{template.name}': {e}. "
                    f"This indicates a core system issue with PDF rendering. Please contact Odoo.sh support immediately."
                )
                # Present a user-friendly message for the meeting
                raise UserError(_(
                    "Document generation service is temporarily unavailable due to a system configuration error. "
                    "Please inform your administrator. (Code: SG-001)"
                ))
            else:
                # Re-raise any other UserErrors that might occur
                raise
