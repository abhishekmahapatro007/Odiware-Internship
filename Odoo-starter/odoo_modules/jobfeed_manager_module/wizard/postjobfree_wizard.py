import logging
from datetime import timedelta, datetime

from odoo import fields, models
from odoo.exceptions import ValidationError, AccessError
from ..utils.pjf_job_queue import PJF_JobType, add_job

_logger = logging.getLogger(__name__)

class PostJobFreeJobQueueWizard(models.TransientModel):
    _name = 'postjobfree.jobqueue.wizard'
    _description = 'Add a job to the TipTopJobQueue (job_queue.xml)'

    job_id = fields.Many2one('hr.job', string="Job", required=True)
    # ref_nb = fields.Char(required=True, string="Job Reference Number")
    job_url = fields.Char(required=True, string="Job URL Address")
    company_name = fields.Char(required=True, string="Company Name")
    salary = fields.Char(required=True, string="Expected Salary")
    description = fields.Html(string="Job Description", required=True)

    def add_to_job_queue(self):
        self.ensure_one()
        # print(f"{self.description}")
        try:
            job: PJF_JobType = {
                "title": self.job_id.name,
                "company": self.company_name,
                "date": self.job_id.create_date,
                "description": f"{self.description}",
                "location": f'{self.job_id.city}, {self.job_id.country_id.name}',
                "referencenumber": f'ODI-{self.job_id.id}',
                "salary": self.salary,
                "url": self.job_url,
            }

            if not all([job["title"], job["company"], job['date'], job['description'], job['location'], job['referencenumber'], job['url']]):
                raise ValidationError(f'Various required fields are not provided/filled. They are needed to post on PostJobFree. Please fill them up before submitting.')

            add_job(job)

            scheduled_cron_time = datetime.now() + timedelta(days=30)
            self.env['ir.cron'].create({
                'name': f'Clean up PJF feed - {self.job_id.id}',
                'model_id': self.env['ir.model'].search([('model','=', 'hr.job')]).id,
                'state': 'code',
                'code': f'model._remove_from_feed({self.job_id.id}, "postjobfree")',
                'interval_number': 30,
                'interval_type': 'days',
                'numbercall': 1,
                'nextcall': scheduled_cron_time.strftime("%Y-%m-%d %H:%M:%S"),
                'priority': 8,
            })

            exp_date_job = scheduled_cron_time
            # print(date(exp_date_job.year,exp_date_job.month, exp_date_job.day))
            self.job_id.postjobfree_posted = fields.Date.today()
            self.job_id.postjobfree_expire = fields.Date.from_string(exp_date_job.strftime('%Y-%m-%d'))

            return {'type': 'ir.actions.act_window_close'}
        except ValidationError as e:
            raise e
        except Exception as e:
            _logger.error("Error Occurred in LinkedinPostWiz: %s", e)
            raise AccessError(
                'An unexpected error has cropped up. No worries, you can try again.'
            )
