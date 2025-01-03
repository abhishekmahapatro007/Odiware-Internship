from odoo import api, fields, models, _
from odoo import tools
from odoo.exceptions import UserError, ValidationError


class HrApplicantTreeWizard(models.TransientModel):
    _name = 'hr.applicant.tree.wizard'
    _description = 'Send Assessment Wizard'

    applicant_ids = fields.Many2many('hr.applicant', string="Applicants", required=True)
    recipient_name = fields.Char(string="Recipient Email", readonly=True, required=True)
    subject = fields.Char(string="Subject", required=True)
    choose_template = fields.Many2one('mail.template', string="Choose Template",
                                      domain=[('name', 'ilike', 'survey')], required=True)
    message_body = fields.Html(string="Message", related='choose_template.body_html', readonly=False)

    @api.model
    def default_get(self, fields):
        res = super(HrApplicantTreeWizard, self).default_get(fields)
        applicant_ids = self.env.context.get('active_ids')
        if applicant_ids:
            applicants = self.env['hr.applicant'].browse(applicant_ids)
            email_list = ', '.join(applicant.email_from for applicant in applicants if applicant.email_from)

            # Ensure all selected applicants have the same job position
            job_positions = set(applicants.mapped('job_id.name'))
            if len(job_positions) > 1:
                raise ValidationError(_("All selected applicants must have the same job position."))

            # Update the form to show only the single job position
            job_position = job_positions.pop()
            res.update({
                'applicant_ids': [(6, 0, applicant_ids)],
                'recipient_name': email_list,
                'subject': f"Assessment for {job_position}",
            })
        return res

    def action_send_mail(self):
        template = self.env.ref('hrms_recruitment.mail_template_send_assessment')
        if not template:
            raise UserError(_("Mail template not found!"))
        for applicant in self.applicant_ids:
            template.send_mail(applicant.id, force_send=True)
        return {'type': 'ir.actions.act_window_close'}
