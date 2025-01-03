from odoo import fields, models
from datetime import date



class HrRecruitment(models.Model):
    _inherit = "hr.job"

    account_manager = fields.Many2one("hr.employee", string="Account Manager")
    recruiter_name = fields.Many2one("hr.employee", string="Recruiter assignee")
    no_of_position = fields.Integer(string="Number of positions")
    status = fields.Selection([('in progress', 'In progress'), ('inactive', 'Inactive')],
                              string="Status")
    # type_ids = fields.Selection([('fte', 'FTE'), ('tpc', 'TPC')], string="Type")
    work_experience = fields.Integer(string="Work Experience(Years)")
    # skills = fields.Char(string="Skills")
    attachment_ids = fields.One2many('ir.attachment', 'res_id', string="Attachment")
    rate = fields.Integer(string="Rate", default=0)
    target_date = fields.Date(string="Target Date")
    creation_date = fields.Date(string='Creation Date', readonly=True, default=lambda self: date.today())
    city = fields.Char(string="City")
    country_id = fields.Many2one('res.country', string="Country")
    zip_code = fields.Char(string="Zip Code")
    company_name = fields.Many2one("res.partner", string="Company Name")

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user.id)

    # add_assessment_id = fields.One2many('ir.attachment', 'res_id', string="Assessment",
    #                                     domain=[('res_model', '=', 'hr.job')])
    assign_id = fields.Many2one("survey.survey", string="Choose Assessment")

    # @api.depends('assign_id')
    # def _compute_attachments_ids(self):
    #     for record in self:
    #         if record.assign_id:
    #             record.attachments_ids = [(6, 0, record.assign_id.attachments_ids.ids)]
    #         else:
    #             record.attachments_ids = [(5, 0, 0)]
    #
    # attachments_ids = fields.Many2many(
    #     'ir.attachment',
    #     'hr_job_attachment_rel',
    #     'job_id',
    #     'attachment_id',
    #     string="Attachments",
    #     compute='_compute_attachments_ids',
    #     store=True
    # )

    #
    # def add_message_to_chatter(self, message):
    #     odoo_bot_user_id = self.env.ref('base.partner_root').id
    #
    #     self.message_post(
    #         body=message,
    #         author_id=odoo_bot_user_id,
    #         # message_type='comment',
    #         # subtype_xmlid='mail.mt_comment'
    #     )

    # def action_open_postjobfree_wizard(self):
    #     return {
    #         'name': _('Post to PostJobFree'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'postjobfree.jobqueue.wizard',
    #         'view_mode': 'form',
    #         'target': 'new',
    #         'context': {
    #             'default_job_id': self.id,
    #             'default_description': self.description,
    #         },
    #     }

    def add_message_to_chatter(self, message):
        odoo_bot_user_id = self.env.ref('base.partner_root').id

        self.message_post(
            body=message,
            author_id=odoo_bot_user_id,
            # message_type='comment', 
            # subtype_xmlid='mail.mt_comment'
        )


class CompanyName(models.Model):
    _name = 'company.name'

    company = fields.Char(string="Company", required=True)
    position = fields.Char(string="Position")


class Assignment(models.Model):
    _name = 'assignment'
    _description = 'Assignment'

    name = fields.Char(string="Title", required=True)
    assign_date = fields.Date(string="Assignment Date")
    description = fields.Text(string="Description")
    job_id = fields.Many2one('hr.job', string="Job")
    attachments_ids = fields.One2many('ir.attachment', 'res_id', string="Attach Assignment")
