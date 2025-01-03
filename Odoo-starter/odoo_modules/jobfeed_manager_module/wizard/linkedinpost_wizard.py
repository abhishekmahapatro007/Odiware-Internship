import logging
from datetime import timedelta, datetime, date

from odoo import fields, models, _
from odoo.exceptions import ValidationError, AccessError
from ..utils.job_queue import JobType, add_job

_logger = logging.getLogger(__name__)

"""
To post to linkedin jobs, the system needs to have the following data:
[Required]:  
    Job ID <partnerJobId>
    Company Name <company>
    Job Title <title>
    Job Description <description>
    Location String <location>
    Apply URL <applyUrl>
    LinkedIn Company ID <companyId>

[Non-essential]:
    <skills> <skill/> <skill/> <skill/> </skills>
    <workplaceTypes>
    <listDate>
    <expirationDate>
    <salary> (Doubt)
    <jobtype>
    <experienceLevel>
    <city> <state> <country>
"""
class PostJobFreeJobQueueWizard(models.TransientModel):
    _name = 'linkedinjobs.jobqueue.wizard'
    _description = 'Add a job to the Linkedin Job Listing through XML job feed (job_queue.xml)'

    job_id = fields.Many2one('hr.job', string="Job", required=True)
    company_name = fields.Char(required=True, string="Company Name")
    description = fields.Html(string="Job Description", required=True)
    company_id = fields.Char(required=True, string="Linkedin Company Ref Number")
    apply_url = fields.Char(required=True, string="Job URL Address")
    expiration_date = fields.Date(required=True, string="Expiration Date")
    job_type = fields.Selection(
        [
            ('FULL_TIME', 'Full Time'),
            ('PART_TIME', 'Part Time'),
            ('CONTRACT', 'Contract'),
            ('INTERNSHIP', 'Internship'),
            ('VOLUNTEER', 'Volunteer'),
        ],
        string="Job Type")
    exp_lvl = fields.Selection(
        [
            ('ENTRY_LEVEL', 'Entry Level'),
            ('EXECUTIVE', 'Executive'),
            ('ASSOCIATE', 'Associate'),
            ('INTERNSHIP', 'Internship'),
            ('MID_SENIOR_LEVEL', 'Mid Senior Level'),
            ('DIRECTOR', 'Director'),
            ('NOT_APPLICABLE', 'N/A'),
        ],
        string="Experience Level")
    workplace_type = fields.Selection(
        [
            ('On-site', 'On-site'),
            ('Hybrid', 'Hybrid'),
            ('Remote', 'Remote'),
        ],
        string="Workplace Type")
    # salary = fields.Char(required=True, string="Expected Salary")

    def add_to_job_queue(self):
        self.ensure_one()

        try:
            if self.expiration_date < (date.today() + timedelta(days=1)):
                raise ValidationError(
                    _('The expiration date set for the job is less than 1 day apart from today. Please set a date that is more than 1 day apart from now.'))
            # print(f"{self.description}")
            job: JobType = {
                "partnerJobId": f'{self.job_id.id}',
                "company": self.company_name,
                "title": self.job_id.name,
                "description": f'{self.description}',
                "location": f'{self.job_id.city}, {self.job_id.country_id.name}',
                "applyUrl": self.apply_url,
                "companyId": self.company_id,
                "skills": [],
                "listDate": self.job_id.create_date,
                "expirationDate": self.expiration_date,
                "salary": "",
                "jobtype": self.job_type,
                "experienceLevel": self.exp_lvl,
                "workplaceTypes": self.workplace_type,
                "city": "",
                "state": "",
                "country": ""
            }

            if not all([job["title"], job["company"], job["partnerJobId"], job['description'], job['location'],
                        job['applyUrl'], job['companyId']]):
                raise ValidationError(
                    f'Various required fields are not set. They are needed to post on Linkedin. Please fill them up before submitting.')

            add_job(job)

            scheduled_cron_time = datetime.now() + timedelta(days=30)
            self.env['ir.cron'].create({
                'name': f'Clean up LKN feed - {self.job_id.id}',
                'model_id': self.env['ir.model'].search([('model', '=', 'hr.job')]).id,
                'state': 'code',
                'code': f'model._remove_from_feed({self.job_id.id}, "linkedin")',
                'interval_number': 30,
                'interval_type': 'days',
                'numbercall': 1,
                'nextcall': scheduled_cron_time.strftime("%Y-%m-%d %H:%M:%S"),
                'priority': 8,
            })

            # active_ids = self.env.context.get('active_ids', [])
            # if active_ids:
            #     # Process the records
            #     records = self.env['hr.job'].browse(active_ids)
            #     for record in records:
            #         # Call the method to add a message to chatter
            #         record.add_message_to_chatter(
            #             f'This job has been posted to POSTJOBFREE under the job id. ODI-{self.job_id.id}'
            #         )

            exp_date_job = fields.Date.from_string(self.expiration_date)
            # print(date(exp_date_job.year,exp_date_job.month, exp_date_job.day))
            self.job_id.linkedin_posted = date.today()
            self.job_id.linkedin_expire = date(exp_date_job.year, exp_date_job.month, exp_date_job.day)

            return {'type': 'ir.actions.act_window_close'}
        except ValidationError as e:
            raise e
        except Exception as e:
            _logger.error("Error Occurred in LinkedinPostWiz: %s", e)
            raise AccessError(
                'An unexpected error has cropped up. No worries, you can try again.'
            )



