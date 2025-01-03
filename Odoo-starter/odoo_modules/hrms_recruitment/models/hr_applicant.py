from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError

class HrRecruitment(models.Model):
    _inherit = "hr.applicant"

    current_city_ids = fields.Char(string="Current City")
    preferred_city_ids = fields.Char(string="Preferred City")
    current_CTC = fields.Float(string='Current CTC', group_operator="avg", help="Current Salary of the Applicant")
    offer_in_hand = fields.Selection([('yes', 'Yes'), ('no', 'No')], string="Offer in Hand")
    official_notice_period = fields.Integer(string="Official Notice Period(in days)")
    how_soon_can_be_joined = fields.Integer(string="How soon can be joined(in days)")
    last_working_day = fields.Date(string="Last Working Day")
    current_organization = fields.Text(string="Current Organization")
    total_experience = fields.Char(string='Total Experience',
                                   help="Enter the total experience in the format 'X Years Y Months'")
    relevant_experience = fields.Char(string="Relevant Experience")
    recruiter_name = fields.Many2one("hr.employee", string="Recruiter name")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string="Attachment")

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)

    _sql_constraints = [
        ('phone_unique', 'UNIQUE(partner_phone)', 'This phone number is already used for another candidate'),
        ('email_unique', 'UNIQUE(email_from)', 'This email address is already used for another candidate')
    ]

    # @api.model
    # def create(self, vals):
    #     res = super(HrRecruitment, self).create(vals)
    #     res._send_interview_invitation()
    #     return res
    #
    # def write(self, vals):
    #     res = super(HrRecruitment, self).write(vals)
    #     if 'stage_id' in vals and vals['stage_id']:
    #         self._send_interview_invitation()
    #     return res
    #
    # def _send_interview_invitation(self):
    #     interview_stage = self.env.ref(
    #         'hr_recruitment.hr_recruitment_stage_form')
    #     for applicant in self:
    #         if applicant.stage_id == interview_stage:
    #             template = self.env.ref('hrms_recruitment.interview_invitation_meeting')
    #             if template:
    #                 template.send_mail(applicant.id, force_send=True)

    assessment_assigned = fields.Many2one(related='job_id', string="Assessment Assigned", readonly=True)

    # def action_send_assignment_link(self):
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': _("Share a Survey"),
    #         'view_mode': 'form',
    #         'res_model': 'survey.survey',
    #         'target': 'new',
    #         'view_id': self.env.ref('survey.survey_survey_view_form').id,
    #     }

    def action_send_assignment_link(self):
        # Get the survey.survey model
        survey_survey_model = self.env['survey.survey']

        # Find the survey record you want to call the method on
        survey_id = 1  # This id value 1 is showing the data of survey wizard id from addons

        # Call the action_send_survey method on the survey record
        survey_record = survey_survey_model.browse(survey_id)
        return survey_record.action_send_survey()

    def action_open_mail_wizard(self):
        return {
            'name': _('Send Mail'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.applicant.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_applicant_id': self.id,
            },
        }

    def action_send_assessment_tree(self):
        return {
            'name': _('Send Assessment'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.applicant.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_applicant_id': self.id,
            },
        }
