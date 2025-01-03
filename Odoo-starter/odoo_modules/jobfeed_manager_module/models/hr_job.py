from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from ..utils.job_queue import delete_job as delete_linkedin_job
from ..utils.pjf_job_queue import delete_job as delete_pjf_job

class LinkedinJobFeedManager(models.Model):
    _inherit = "hr.job"

    linkedin_posted = fields.Date()
    formatted_linkedin_posted = fields.Char(string='Linkedin Post Date', compute='_compute_formatted_post_date')
    linkedin_expire = fields.Date()
    formatted_linkedin_expire = fields.Char(string='Linkedin Expire Date', compute='_compute_formatted_expire_date')

    postjobfree_posted = fields.Date()
    formatted_postjobfree_posted = fields.Char(string='PostJobFree Post Date', compute='_compute_formatted_pjf_post')
    postjobfree_expire = fields.Date()
    formatted_postjobfree_expire = fields.Char(string='PostJobFree Expire Date', compute='_compute_formatted_pjf_expire')

    @api.depends('linkedin_posted')
    def _compute_formatted_post_date(self):
        for record in self:
            if record.linkedin_posted:
                record.formatted_linkedin_posted = fields.Date.from_string(record.linkedin_posted).strftime('%d-%m-%Y')
            else:
                record.formatted_linkedin_posted = ''

    @api.depends('linkedin_expire')
    def _compute_formatted_expire_date(self):
        for record in self:
            if record.linkedin_expire:
                record.formatted_linkedin_expire = fields.Date.from_string(record.linkedin_expire).strftime('%d-%m-%Y')
            else:
                record.formatted_linkedin_expire = ''

    @api.depends('postjobfree_posted')
    def _compute_formatted_pjf_post(self):
        for record in self:
            if record.postjobfree_posted:
                record.formatted_postjobfree_posted = fields.Date.from_string(record.postjobfree_posted).strftime('%d-%m-%Y')
            else:
                record.formatted_postjobfree_posted = ''

    @api.depends('postjobfree_expire')
    def _compute_formatted_pjf_expire(self):
        for record in self:
            if record.postjobfree_expire:
                record.formatted_postjobfree_expire = fields.Date.from_string(record.postjobfree_expire).strftime('%d-%m-%Y')
            else:
                record.formatted_postjobfree_expire = ''


    def action_open_linkedinjobs_wizard(self):
        for record in self:
            if not record.description:
                raise ValidationError(_("Please fill the Job Summary before trying to post it on job boards"))
            if not record.country_id:
                raise ValidationError(_("Please fill the Country field before trying to post it on job boards"))
            if not record.city:
                raise ValidationError(_("Please fill the City field before trying to post it on job boards"))
            if not record.name:
                raise ValidationError(_("Please fill the Name of the job before trying to post it on job boards"))

            return {
                'name': _('Post to Linkedin Jobs'),
                'type': 'ir.actions.act_window',
                'res_model': 'linkedinjobs.jobqueue.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_job_id': record.id,
                    'default_description': record.description,
                },
            }

    def action_open_postjobfree_wiz(self):
        for record in self:
            if not record.country_id:
                raise ValidationError(_("Please fill the Country field before trying to post it on job boards"))
            if not record.city:
                raise ValidationError(_("Please fill the City field before trying to post it on job boards"))
            if not record.description:
                raise ValidationError(_("Please fill the Job Summary before trying to post it on job boards"))
            if not record.name:
                raise ValidationError(_("Please fill the Name of the job before trying to post it on job boards"))

            return {
                'name': _('Post to PostJobFree Jobs'),
                'type': 'ir.actions.act_window',
                'res_model': 'postjobfree.jobqueue.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_job_id': record.id,
                    'default_description': record.description,
                },
            }


    def action_remove_linkedinjob_from_feed(self):
        for record in self:
            job_id = record.id
            delete_linkedin_job(job_id)

            cron_jobs = self.env['ir.cron'].search([
                '&',
                    ('name', '=', f'Clean up LKN feed - {job_id}'),
                    '|', ('active', '=', True), ('active', '=', False)
            ])

            for cj in cron_jobs:
                cj.unlink()

            self.linkedin_posted = False
            self.linkedin_expire = False

    def action_remove_job_from_pjf_feed(self):
        for record in self:
            job_id = record.id
            delete_pjf_job(f'ODI-{job_id}')

            cron_jobs = self.env['ir.cron'].search([
                '&',
                    ('name', '=', f'Clean up PJF feed - {job_id}'),
                #     '|', ('name', '=', f'Clean up ODI-{job_id}'), ('name', '=', f'Clean up {job_id}'),
                    '|', ('active', '=', True), ('active', '=', False)
            ])

            for cj in cron_jobs:
                cj.unlink()

            self.postjobfree_posted = False
            self.postjobfree_expire = False

    @api.model
    def _remove_from_feed(self, job_id, feed_for: str):
        # print(">>>>>> CRON CRON >>>>>>>> ", job_id)
        # NOTE - setting record values to something in a cron job will not work directly.
        # this will need to be done using queries.
        rec = self.browse(job_id)
        if feed_for == "linkedin":
            delete_linkedin_job(job_id)

            rec.linkedin_posted = False
            rec.linkedin_expire = False

        if feed_for == "postjobfree":
            # for PostJobFree, reference numbers are just record.id prefixed with 'ODI-'
            delete_pjf_job(f'ODI-{job_id}')

            rec.postjobfree_posted = False
            rec.postjobfree_expire = False

    # @api.model
    # def add_message_to_chatter(self, message):
    #     odoo_bot_user_id = self.env.ref('base.partner_root').id
    #
    #     self.message_post(
    #         body=message,
    #         author_id=odoo_bot_user_id,
    #         # message_type='comment',
    #         # subtype_xmlid='mail.mt_comment'
    #     )

    # @api.model
    # def cleanup_old_jobs(self, job_id):
    #     if not job_id:
    #         raise ValidationError(_("No job_id received to perform proper clean up"))
    #
    #     # remove_oldest_job()