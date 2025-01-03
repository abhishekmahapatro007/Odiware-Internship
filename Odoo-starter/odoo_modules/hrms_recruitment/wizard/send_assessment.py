from odoo import models, fields, api, _
from odoo import tools
from odoo.exceptions import UserError, ValidationError


class SurveyInviteWizard(models.TransientModel):
    _inherit = 'survey.invite'

    recipient = fields.Char(string='Recipient Name', readonly=True, required=True)

    def action_invite(self):
        """ Process the wizard content and proceed with sending the related
            email(s), rendering any template patterns on the fly if needed """
        self.ensure_one()
        Partner = self.env['res.partner']

        # Use the recipient instead of partner_ids
        recipient_value = self.recipient
        valid_partners = Partner.browse()  # Start with an empty recordset
        langs = set()

        if recipient_value:
            # Assuming recipient contains emails separated by commas or spaces
            emails = tools.email_split(recipient_value)
            valid_emails = []

            for email in emails:
                partner = False
                email_normalized = tools.email_normalize(email)
                if email_normalized:
                    limit = None if self.survey_users_login_required else 1
                    partner = Partner.search([('email_normalized', '=', email_normalized)], limit=limit)
                if partner:
                    valid_partners |= partner
                    langs.add(partner.lang)
                else:
                    email_formatted = tools.email_split_and_format(email)
                    if email_formatted:
                        valid_emails.extend(email_formatted)

            if len(langs) == 1:
                self = self.with_context(lang=langs.pop())

            if not valid_partners and not valid_emails:
                raise UserError(_("Please enter at least one valid recipient."))

            answers = self._prepare_answers(valid_partners, valid_emails)
            for answer in answers:
                self._send_mail(answer)

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields):
        res = super(SurveyInviteWizard, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        if active_model == 'hr.applicant' and active_id:
            applicant = self.env['hr.applicant'].browse(active_id)
            res['recipient'] = applicant.email_from
        return res

    def _send_mail(self, answer):
        """ Customize the email sending process to include the recipient in email_to """
        mail_values = {
            'subject': self.subject,
            'body_html': self.body,
            'email_to': self.recipient,  # Set the recipient field's value in the email_to field
        }
        mail = self.env['mail.mail'].create(mail_values)
        mail.send()
