from datetime import timedelta, datetime, date
from collections import defaultdict
from dateutil.relativedelta import relativedelta
from pytz import utc
from odoo.tools import float_utils
from odoo import api, fields, models
from odoo.http import request

ROUNDING_FACTOR = 16


class Employee(models.Model):
    _inherit = 'hr.employee'

    is_manager = fields.Boolean(compute='_compute_is_manager',
                                help="Flag indicating whether the employee "
                                     "is a manager.")

    def _compute_is_manager(self):
        """Compute function for checking whether it is a manager or not"""
        for rec in self:
            rec.is_manager = rec.env.user.has_group('hr_payroll_community.group_hr_payroll_community_manager')

    @api.model
    def check_user_group(self):
        uid = request.session.uid
        user = self.env['res.users'].sudo().browse(uid)
        return user.has_group('hr.group_hr_manager')

    @api.model
    def get_user_employee_info(self):
        """To get the employee information"""
        uid = request.session.uid
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', uid)], limit=1)
        all_recruitment_stages = self.env['hr.recruitment.stage'].search([])
        all_rec_stages_name = all_recruitment_stages.mapped('name')

        new_active_jobs = self.env['hr.job'].sudo().search_count([('active', '=', True)])
        
        total_applicants = self.env['hr.applicant'].sudo().search_count([
            ('stage_id', 'in', all_rec_stages_name)
        ])

        new_submission = self.env['hr.applicant'].sudo().search_count([('stage_id', '=', 'Initial Qualification')])
        new_interview = self.env['hr.applicant'].sudo().search_count([
            '|',
            ('stage_id', '=', 'First Interview'),
            ('stage_id', '=', 'Second Interview')
        ])
        hired_stage_ids = self.env['hr.recruitment.stage'].sudo().search([('hired_stage', '=', True)]).ids
        new_hired = self.env['hr.applicant'].sudo().search_count([('stage_id', 'in', hired_stage_ids)])

        # salary_structures = self.env['hr.payroll.structure'].sudo().search_count([])

        job_names = self.get_all_job_positions_with_company() # get job names along with the count for number of applicant in each stage

        job_opening = self.get_published_job_openings()

        new_active_candidate = self.get_active_candidates()

        data = {
            'active_jobs_count': new_active_jobs,
            'active_jobs_list': job_names,
            'active_job_opening': job_opening,
            'active_candidates': new_active_candidate,
            # 'emp_leave': manager_leave_request if employee.is_manager else leave_request_count,
            'interview_count': new_interview,
            'submission_count': new_submission,
            'leave_requests': total_applicants, # leave_requests corresponds to total_applicants
            'hired_count': new_hired,
            'all_stages': all_rec_stages_name,
            # 'attendance_state': employee.attendance_state if employee else None,
        }
        return [data] if employee else []

    def get_all_job_positions_with_company(self):
        """
        Fetch active job positions along with their corresponding company names from the hr.job model.
        Also fetch applicant counts for each stage, using 'job_id' for grouping.
        """
        job_positions = self.env['hr.job'].search([('active', '=', True)], order='name asc')

        all_recruitment_stages = self.env['hr.recruitment.stage'].search([])
        all_rec_stages_name = all_recruitment_stages.mapped('name')

        # Fetch applicant counts for each stage using 'job_id'
        applicants_data = self.env['hr.applicant'].read_group(
            [('stage_id.name', 'in', all_rec_stages_name)],
            ['job_id', 'stage_id', 'id:count'],  # Group by 'job_id' and 'stage_id'
            ['job_id', 'stage_id'],  # Group by job_id and stage_id
            lazy=False  # Ensure all results are returned
        )

        # Organize applicant count by job_id and stage_id

        """
        -----------
        """
        job_data = []

        for job in job_positions:
            job_data_record = {"id": job.id,
                               "name": job.name,
                               "company_name": job.company_name.name if job.company_name else ''}

            for record in applicants_data:
                # print(isinstance(record.get('job_id'), tuple), "\n\n\n")
                if record.get('job_id') and job.id == record.get('job_id')[0]:
                    stage_data_name = record.get('stage_id')[1]
                    normalize_stage_name = '_'.join(stage_data_name.split()).lower()
                    normalize_stage_name_postfix = normalize_stage_name + "_count"

                    job_data_record[normalize_stage_name_postfix] = record.get("__count", 0)
            
            job_data.append(job_data_record)

        # print("\n\n", job_data)
        return job_data

        """
        job_applicant_count = {}
        for record in applicants_data:
            job_id = record.get('job_id')[0] if record.get('job_id') else None
            stage_data = record.get('stage_id')[1] if record.get('stage_id') else 'Unknown Stage'
            count = record.get('__count', 0)  # Correct count field

            if job_id:
                if job_id not in job_applicant_count:
                    job_applicant_count[job_id] = {}
                job_applicant_count[job_id][stage_data] = count

        # print("\n\n", job_applicant_count)
        # Prepare the final job data with counts for each stage
        for job in job_positions:
            stage_counts = job_applicant_count.get(job.id, {})

            # Prepare job data with stage counts
            job_data.append({
                'id': job.id,
                'name': job.name,
                'company_name': job.company_name.name if job.company_id else '',
                'new_count': stage_counts.get('New', 0),
                'initial_qualification_count': stage_counts.get('Initial Qualification', 0),
                'first_interview_count': stage_counts.get('First Interview', 0),
                'second_interview_count': stage_counts.get('Second Interview', 0),
                'contract_proposal_count': stage_counts.get('Contract Proposal', 0),
                'contract_signed_count': stage_counts.get('Contract Signed', 0),
            })

        return job_data
        """

    def get_published_job_openings(self):
        # Search for published job openings
        published_jobs = self.env['hr.job'].search([])

        # Return a list of dictionaries with job details, including 'no_of_recruitment'
        return [{
            'id': job.id,
            'name': job.name,
            'no_of_recruitment': job.no_of_recruitment,  # Fetch the number of candidates required
            'time_to_fill': (job.target_date - job.creation_date).days if job.creation_date and job.target_date else 0
        } for job in published_jobs]

    def get_active_candidates(self):
        # Search for active candidates in specific stages
        all_candidates = self.env['hr.applicant'].sudo().search([])

        # Return a list of dictionaries with candidate IDs and their partner names
        return [{
            'id': candidate.id,
            'name': candidate.partner_name,
            'job_position': candidate.job_id.name,
            'time_to_hire': (
                    candidate.date_closed - candidate.create_date).days
            if candidate.create_date and candidate.date_closed else 0
        } for candidate in all_candidates]


def get_work_days_dashboard(from_datetime, to_datetime, compute_leaves=False, calendar=None, resource=None):
    """
    Calculate the total work days between two datetimes.
    """
    calendar = calendar or resource.resource_calendar_id
    if not from_datetime.tzinfo:
        from_datetime = from_datetime.replace(tzinfo=utc)
    if not to_datetime.tzinfo:
        to_datetime = to_datetime.replace(tzinfo=utc)

    from_full = from_datetime - timedelta(days=1)
    to_full = to_datetime + timedelta(days=1)
    intervals = calendar._attendance_intervals_batch(from_full, to_full, resource)
    day_total = defaultdict(float)

    for start, stop, meta in intervals[resource.id]:
        day_total[start.date()] += (stop - start).total_seconds() / 3600

    intervals = calendar._work_intervals_batch(from_datetime, to_datetime, resource) if compute_leaves else \
        calendar._attendance_intervals_batch(from_datetime, to_datetime, resource)
    day_hours = defaultdict(float)

    for start, stop, meta in intervals[resource.id]:
        day_hours[start.date()] += (stop - start).total_seconds() / 3600

    days = sum(
        float_utils.round(ROUNDING_FACTOR * day_hours[day] / day_total[day]) / ROUNDING_FACTOR for day in day_hours)
    return days


@api.model
def get_department_leave(self):
    # Placeholder for future implementation of department leave calculations.
    pass


@api.model
def employee_leave_trend(self):
    # Placeholder for future implementation of employee leave trend calculations.
    pass
