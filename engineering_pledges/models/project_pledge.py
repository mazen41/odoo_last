# -*- coding: utf-8 -*-
from odoo import models, fields, api
import datetime

class EngineeringTaskPledge(models.Model):
    _name = 'engineering.task.pledge' 
    _description = 'Task Municipality Pledge'

    task_id = fields.Many2one('project.task', string='Task', ondelete='cascade')
    template_id = fields.Many2one('engineering.pledge.template', string='نوع التعهد (Pledge Type)', required=True)
    is_completed = fields.Boolean(string='متوفر / تم التوقيع (Completed)', default=False)
    
    # --- THE FIX IS HERE: ADDED sanitize=False ---
    generated_html = fields.Html(string='Generated Content', sanitize=False) 

class ProjectTask(models.Model):
    _inherit = 'project.task'

    stage_sequence = fields.Integer(related='stage_id.sequence', readonly=True)
    pledge_ids = fields.One2many('engineering.task.pledge', 'task_id', string='تعهدات البلدية (Pledges)')

    def action_load_required_pledges(self):
        """ Loads pledges based on the project's building type """
        for task in self:
            building_type = task.project_id.building_type
            if not building_type:
                continue

            domain = [('active', '=', True), ('building_type', 'in', [building_type, 'all'])]
            templates = self.env['engineering.pledge.template'].search(domain)
            existing_template_ids = task.pledge_ids.mapped('template_id.id')
            
            for template in templates:
                if template.id not in existing_template_ids:
                    self.env['engineering.task.pledge'].create({
                        'task_id': task.id,
                        'template_id': template.id,
                    })

    def action_generate_pledges_pdf(self):
        """ 
        1. Finds all pledges for this task.
        2. Replaces placeholders {{...}} with real data.
        3. Saves it to generated_html.
        4. Calls the PDF report action.
        """
        self.ensure_one()
        
        # Get project data to fill the templates
        project = self.project_id
        partner_name = project.partner_id.name or "__________________"
        date_today = datetime.date.today().strftime("%Y/%m/%d")
        
        # Map values. If empty, print an empty line.
        replacements = {
            '{{partner_name}}': partner_name,
            '{{date}}': date_today,
            '{{governorate}}': project.region or "__________________", # Region holds Governorate in your setup
            '{{region}}': project.region or "__________________",
            '{{block_no}}': project.block_no or "____",
            '{{plot_no}}': project.plot_no or "____",
            '{{street_no}}': project.street_no or "____",
        }

        # Process each pledge in the list
        for pledge in self.pledge_ids:
            if not pledge.template_id.body_html:
                continue
                
            raw_html = pledge.template_id.body_html
            for key, value in replacements.items():
                raw_html = raw_html.replace(key, str(value))
                
            pledge.generated_html = raw_html

        # Trigger the PDF download
        return self.env.ref('engineering_pledges.action_report_unified_pledges').report_action(self)
