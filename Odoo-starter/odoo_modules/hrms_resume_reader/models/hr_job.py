from odoo import fields, models


class HrJobPosition(models.Model):
    _inherit = "hr.job"

    def action_on_click_add_from_resume_btn(self):
        for record in self:
            return {
                'name': 'Add Applicant from Resume',
                'type': 'ir.actions.act_window',
                'res_model': 'applicant.record.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_job_id': record.id,
                    'default_application_name': record.name,
                    # 'default_description': record.description,
                },
            }