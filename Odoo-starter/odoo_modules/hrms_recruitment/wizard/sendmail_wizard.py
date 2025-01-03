from odoo import api, fields, models, _


class HrApplicantMailWizard(models.TransientModel):
    _name = 'hr.applicant.mail.wizard'
    _description = 'HR Applicant Mail Wizard'

    applicant_id = fields.Many2one('hr.applicant', string="Applicant", required=True)
    partner_name = fields.Char(related='applicant_id.partner_name', string="Partner Name", store=True, readonly=True)
    choose_template = fields.Many2one('mail.template', string="Choose Template",
                                      domain=[('name', 'ilike', 'recruitment')], required=True)
    template_body = fields.Html(string="Template Body", related='choose_template.body_html', readonly=False)

    def send_mail(self):
        self.ensure_one()
        template = self.choose_template
        if template:
            mail_values = {
                'subject': template.subject,
                'body_html': self.template_body,
                'email_to': self.applicant_id.partner_name,
                'recipient_ids': [(6, 0, [self.applicant_id.partner_id.id])],
                'model': 'hr.applicant',
                'res_id': self.applicant_id.id,
                'email_from': self.env.user.email,
            }
            self.env['mail.mail'].create(mail_values).send()

    # def send_mail(self):
    #     self.ensure_one()
    #     template = self.env.ref('__custom__.hr_recruitment.email_template_First_interview')
    #     if template:
    #         template.send_mail(self.applicant_id.id, force_send=True)
