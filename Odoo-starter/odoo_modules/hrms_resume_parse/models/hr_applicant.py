import logging
import os
from datetime import datetime, timedelta
from typing import Any

import requests

from odoo import api, fields, models, _
# from odoo.exceptions import UserError, ValidationError
from odoo.tools import json
# from ..utils.daxtra_func import get_access_tkn, submit_resume
from ..utils.peoplelabs_score import trigger_single_file_parse, check_status

_logger = logging.getLogger(__name__)

class HrRecruitment(models.Model):
    _inherit = "hr.applicant"

    task_id = fields.Char(
        string="Task ID received from Scoring API",
        help="Task ID received from Scoring API",
        readonly=True
    )
    is_scoring_triggered = fields.Selection(
        string='Status',
        selection=[('never', 'Never'), ('pending', 'Pending'), ('received', 'Received')],
        help='Status of Scoring Request',
        readonly=True
    )
    domain_match = fields.Integer(string="Domain Match Score", help="The value is out of 100", readonly=True)
    exp_match = fields.Integer(string="Experience Match Score", help="This value is out of 100", readonly=True)
    location_match = fields.Integer(string="Location Match Score", help="This value is out of 100", readonly=True)
    role_match = fields.Integer(string="Role Match Score", help="This value is out of 100", readonly=True)
    skill_match = fields.Integer(string="Skill Match Score", help="This value is out of 100", readonly=True)
    matching_score = fields.Integer(string="Overall Score", help="This value is out of 100. It is the weighted average of Skill, Location, Experience, Domain matching scores", readonly=True)

    # @api.model
    # def init(self):
    #     # Adding the cleanup cron for cleaning up inactive crons
    #     existing_cron = self.env['ir.cron'].search([('name', '=', 'Clean up inactive Resume Matching API Polling')])
    #     # print(">>>>>>>>>>>>>>>>>>>>\n\n\n\n", existing_cron.id)
    #     if existing_cron.id == False:
    #         scheduled_cron_time = datetime.now() - timedelta(minutes=25)
    #         self.env['ir.cron'].create({
    #             'name': 'Clean up inactive Resume Matching API Polling',
    #             'model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
    #             'state': 'code',
    #             'code': 'model.clean_up_old_cron()',
    #             'interval_number': 30,
    #             'interval_type': 'minutes',
    #             'numbercall': -1,
    #             'nextcall': scheduled_cron_time.strftime("%Y-%m-%d %H:%M:%S"),
    #             'active': True
    #         })

    # def clean_up_old_cron(self):
    #     print("Cleaning inactive cronjobs associated with Applicant model")
    #     target_model_id = self.env['ir.model'].search([('model', '=', self._name)]).id
    #     cron_jobs = self.env['ir.cron'].search([('model_id', '=', target_model_id), ('id', '!=', self.id)])
    #     print(cron_jobs, cron_jobs.active, self.id)
    #     # cron_jobs.unlink()
    #     return True

    def action_on_click_add_from_resume_btn(self):
        for record in self:
            return {
                'name': _('Add Applicant from Resume'),
                'type': 'ir.actions.act_window',
                'res_model': 'applicant.record.wizard',
                'view_mode': 'form',
                'target': 'new',
                # 'context': {
                #     'default_job_id': None,
                #     'default_description': record.description,
                # },
            }

    def action_on_click_parse_resume(self):
        # print(list(parsed_data.keys()))
        api_key = self.env['ir.config_parameter'].sudo().get_param('hrms_resume_parse.api_key', '0')
        _logger.debug(api_key)
        if api_key == '0':
            # raise UserError("You do not have API key entered in the settings.") # This did not work for unknown reasons
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Error",
                    'message': "You do not have Resume Parser API key entered in the settings. Go to Settings > Recruitment. You can find the section to enter the API key provided by Odiware Technologies.",
                    'type': 'danger',  # 'danger', 'info', 'success', 'warning'
                    'sticky': True,  # Set to True to show it until dismissed
                }
            }

        try:
            for applicant in self:
                applicant_id = applicant.id

                if applicant.attachment_ids:
                    attachment = applicant.attachment_ids[0]
                    # print(attachment.datas)
                    # print(attachment.res_name, attachment.store_fname, attachment.local_url)

                    try:
                        odi_server = os.environ.get("ODIWARE_SERVER_ADDR", "http://localhost:8069")
                        json_data_to_send =  attachment.datas.decode('utf-8')
                        parsing_api = requests.post(
                            f"{odi_server}/odi/action/resume/parse",
                            headers={
                                "Content-Type": "application/json",
                                'Authorization': f"Odi_Api {api_key}"
                            },
                            data=json.dumps({"resume": json_data_to_send})
                        )
                        print(parsing_api.status_code, "\n", parsing_api.json())
                        parsed_result = parsing_api.json().get("result")
                        # print(parsed_result, parsed_result.status, parsed_result.text)
                        response_data = json.loads(parsed_result)
                        # print(response_data)
                        if response_data.get("status") == "error":
                            err = response_data.get("error", "Failed to parse resume.")
                            action = {
                                'type': 'ir.actions.client',
                                'tag': 'display_notification',
                                'params': {
                                    'title': 'Warning!',
                                    'message': err,
                                    'sticky': True,  # Set to True if you want the notification to be sticky
                                    'type': 'danger'
                                }
                            }

                            return action

                    except Exception as e:
                        _logger.error(e)
                        action = {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Warning!',
                                'message': "Unexpected error occurred while parsing the resume",
                                'sticky': True,
                                'type': 'danger'
                            }
                        }

                        return action

                    # vvvv This statement below was only for peoplelabs api. It will not be used anymore.
                    # parsed_data, err = parse_pdf(attachment.datas.decode('utf-8'))

                    if response_data is None:
                        action = {
                            'type': 'ir.actions.client',
                            'tag': 'display_notification',
                            'params': {
                                'title': 'Warning!',
                                'message': "Unable to extract information from the resume",
                                'sticky': True,
                                'type': 'danger'
                            }
                        }

                        return action
                    # endif
                    parsed_data = response_data.get("data", {})
                    new_bal = response_data.get("balance", 0)
                    # print(">>>>>>>>>>>\n", parsed_data)
                    applicant.partner_name = parsed_data.get("name", applicant.partner_name)
                    applicant.email_from = parsed_data.get('email', "")
                    applicant.total_experience = f"{parsed_data.get('total_exp', '0')}"
                    applicant.partner_phone = parsed_data.get('contact', "")
                    applicant.current_city_ids = parsed_data.get('current_city', "")
                    applicant.current_organization = parsed_data.get("curr_org", "")
                    applicant.linkedin_profile = parsed_data.get("linkedin_url", "")
                    applicant.priority = "0"

                    # set degree
                    degree_parsed = parsed_data.get("edu", None)
                    recruitment_deg_model = self.env['hr.recruitment.degree']
                    if degree_parsed is not None:
                        deg_in_db = recruitment_deg_model.search([('name', '=', degree_parsed)])
                        if len(deg_in_db) < 1:
                            new_deg_created = recruitment_deg_model.create({
                                'name': degree_parsed
                            })
                            applicant.type_id = new_deg_created.id
                        else:
                            applicant.type_id = deg_in_db[0].id

                    # Grab the skills and parse to enter into applicant records
                    skills_parsed: list[dict[str, str | list[str]]] = parsed_data.get("cluster", [])

                    for skill_group in skills_parsed:
                        skill_type_parsed = skill_group.get("cluster", None)
                        if skill_type_parsed is None:
                            # raise ValidationError("There was a parsing error. Unable to parse skills.")
                            continue
                        # endif

                        skill_list: list[str] = skill_group.get("skills", [])

                        if len(skill_list) < 1:
                            continue
                        # endif

                        self.search_in_skill_cluster_and_add(applicant_id, skill_type_parsed, skill_list)
                    # endfor
                    self.env['ir.config_parameter'].sudo().set_param('hrms_resume_parse.balance', new_bal)
                # endif
            # endfor
        # endtry
        except Exception as e:
            _logger.error(f"Error occurred while parsing resume: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Failed!',
                    'message': "Failed Operation",
                    'type': 'warning',
                    'sticky': True,
                }
            }
        # endexcept

    @api.model
    def search_in_skill_cluster_and_add(self, applicant_id, cluster_name, skill_list):
        skill_model = self.env['hr.skill']
        applicant_skill_model = self.env['hr.applicant.skill']
        skill_type_model = self.env['hr.skill.type']
        skill_lvl_model = self.env['hr.skill.level']

        skill_types_inst = skill_type_model.search([('name', '=', cluster_name)], limit=1)
        if len(skill_types_inst) > 0:
            skill_type_found = skill_types_inst[0]
            skill_type_found_id = skill_type_found.id

            if len(skill_list) < 1:
                return

            # for skill_parsed in skill_list:
            domain: Any = ['|'] * (len(skill_list) - 1)
            for name in skill_list:
                domain.append('&')
                domain.append(('name', '=', name))
                domain.append(('skill_type_id', '=', skill_type_found_id))

            skills_record = skill_model.search(domain)

            if len(skills_record) < 1:
                print(f"None of the skills in the skill list found under cluster name ${cluster_name}")
            # endif

            parsed_skill_ids = skills_record.mapped('id')
            parsed_skill_names: list[str] = skills_record.mapped('name')
            parsed_skill_names_lowercase = list(map(lambda v: v.lower(), parsed_skill_names))
            skill_lvl_record = skill_lvl_model.search(
                [('skill_type_id', '=', skill_type_found_id), ('default_level', '=', True)], limit=1)

            # still need to extract out skills that are not entered in db and process them as required
            parsed_unlisted_skill: list[str] = list(
                filter(lambda v: v.lower() not in parsed_skill_names_lowercase, skill_list))

            if len(parsed_unlisted_skill) > 0:
                try:
                    self.add_hr_skill_to_existing_type(applicant_id, skill_type_found_id, parsed_unlisted_skill, skill_lvl_record[0].id)
                except Exception as e:
                    raise e

            # case - when skills are in db but not associated with an applicant
            preexisting_applicant_skill = applicant_skill_model.search(
                [('applicant_id', '=', applicant_id)])
            preexisting_applicant_skill_id_map = list(
                map(lambda item: item['skill_id'][0], preexisting_applicant_skill.read(["skill_id"])))
            # summary_applicant_skill = list(map(lambda item: item.id, preexisting_applicant_skill))
            # print(preexisting_applicant_skill, preexisting_applicant_skill_id_map)
            unassociated_skills = list(
                filter(lambda item: item not in preexisting_applicant_skill_id_map, parsed_skill_ids))
            # print(">>>>>>>>>", unassociated_skills, parsed_skill_ids)
            applicant_skill_model.create([
                {
                    'applicant_id': applicant_id,
                    'skill_id': each_skill_id,
                    'skill_level_id': skill_lvl_record[0].id,
                    'skill_type_id': skill_type_found_id,
                    'level_progress': 10,
                } for each_skill_id in unassociated_skills
            ])
            return
        else:
            try:
                self.add_to_hr_skill(applicant_id, cluster_name, skill_list)
                return
            except Exception as e:
                raise e

    @api.model
    def add_to_hr_skill(self, applicant_id: int, skill_type_parsed: str, skill_list: list[str]):
        skill_model = self.env['hr.skill']
        applicant_skill_model = self.env['hr.applicant.skill']
        skill_type_model = self.env['hr.skill.type']
        skill_lvl_model = self.env['hr.skill.level']

        skill_type_rec = skill_type_model.search([('name', '=', skill_type_parsed)], limit=1)

        try:
            if not skill_type_rec:
                new_skill_type_record = skill_type_model.create({
                    'name': skill_type_parsed
                })

                new_skill_lvl_rcrd = skill_lvl_model.create({
                    'name': 'Beginner',
                    'skill_type_id': new_skill_type_record.id,
                    'level_progress': 10,
                    'default_level': True
                })

                new_skill_rcrd = skill_model.create(
                    [{'name': name, 'skill_type_id': new_skill_type_record.id} for name in skill_list])

                applicant_skill_model.create([
                    {
                        'applicant_id': applicant_id,
                        'skill_id': each_skill.id,
                        'skill_level_id': new_skill_lvl_rcrd.id,
                        'skill_type_id': new_skill_type_record.id,
                        'level_progress': 10,
                    } for each_skill in new_skill_rcrd
                ])
            else:
                skill_type_record_instance = skill_type_rec[0]
                new_skill_lvl_rcrd = skill_lvl_model.create({
                    'name': 'Beginner',
                    'skill_type_id': skill_type_record_instance.id,
                    'level_progress': 10,
                    'default_level': True
                })

                new_skill_rcrd = skill_model.create(
                    [{'name': name, 'skill_type_id': skill_type_record_instance.id} for name in skill_list])

                applicant_skill_model.create([
                    {
                        'applicant_id': applicant_id,
                        'skill_id': each_skill.id,
                        'skill_level_id': new_skill_lvl_rcrd.id,
                        'skill_type_id': skill_type_record_instance.id,
                        'level_progress': 10,
                    } for each_skill in new_skill_rcrd
                ])
        except Exception as e:
            _logger.error(f"Uncaught error occurred: {e}")
            raise Exception(e)

    @api.model
    def add_hr_skill_to_existing_type(self, applicant_id: int, skill_type_parsed_id: int, skill_list: list[str],
                                      skill_level_id):
        skill_model = self.env['hr.skill']
        applicant_skill_model = self.env['hr.applicant.skill']
        # skill_type_model = self.env['hr.skill.type']
        # skill_lvl_model = self.env['hr.skill.level']

        try:
            new_skill_rcrd = skill_model.create(
                [{'name': name, 'skill_type_id': skill_type_parsed_id} for name in skill_list])

            applicant_skill_model.create([
                {
                    'applicant_id': applicant_id,
                    'skill_id': each_skill.id,
                    'skill_level_id': skill_level_id,
                    'skill_type_id': skill_type_parsed_id,
                    'level_progress': 10,
                } for each_skill in new_skill_rcrd
            ])
        except Exception as e:
            _logger.debug(f"Uncaught error occurred: {e}")
            raise Exception(e)

    def action_on_click_score_resume(self):
        print(">>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<")
        for applicant in self:
            # applicant.is_scoring_triggered = "received"
            # print(applicant.job_id.description)
            job_desc = applicant.job_id.description
            attachment_base64 = applicant.attachment_ids[0].datas.decode('utf-8')
            try:
                returned_task_id = trigger_single_file_parse(attachment_base64, job_desc)
                applicant.task_id = returned_task_id
                # applicant.task_id = "a7cefbe6-c4fb-4ff4-a6dd-56bc414ef2f4"
                applicant.is_scoring_triggered = "pending"

                #  add a job runner that will do this better without having to use ir.cron  
                scheduled_cron_time = datetime.now() + timedelta(minutes=1)
                self.env['ir.cron'].create({
                    'name': f'Resume Matching API Polling task - {applicant.task_id}',
                    # 'name': f'Resume Scoring Cron task {returned_task_id}',
                    'model_id': self.env['ir.model'].search([('model', '=', self._name)]).id,
                    'state': 'code',
                    'code': f'model.check_status_of_task(task_id="{applicant.task_id}")',
                    'interval_number': 1,
                    'interval_type': 'minutes',
                    'numbercall': 8,
                    'nextcall': scheduled_cron_time.strftime("%Y-%m-%d %H:%M:%S"),
                })

                # For a message notification in the chatter (sidebar)
                # odoo_bot_user_id = self.env.ref('base.partner_root').id
                #
                # self.message_post(
                #     body="Resume has been sent for processing. It may take a minute or two. You will be notified when the resume has been processed.",
                #     author_id=odoo_bot_user_id,
                #     # message_type='comment',
                #     # subtype_xmlid='mail.mt_comment'
                # )

                action = {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'INFO!',
                        'message': "Resume has been sent for processing. It may take a minute or two. You will be notified when the resume has been processed.",
                        'sticky': True,  # Set to True if you want the notification to be sticky
                    }
                }

                return action

            except Exception as e:
                print("This error has occurred: \n", e)

    def check_status_of_task(self, task_id: str):
        # print("Tirggering this CRON FUNC")
        applicant = self.search([('task_id', '=', task_id), ('is_scoring_triggered','=','pending')])
        print(applicant)

        try:
            if not applicant.task_id:
                return False
            
            result = check_status(applicant.task_id)
            # print(result)

            _logger.debug(f"\n### : {json.dumps(result, indent=2)}")
            if result['result'] == 'PROCESSING..':
                return

            if result['result'] is None:
                raise ValueError("Resume Matching Failed")

            print("!!!!!!!!!!!!!!!!!Task completed!")

            applicant.task_id = None
            applicant.is_scoring_triggered = "received"
            applicant.domain_match = result['result']['result'][0]['domain_match']
            applicant.exp_match = result['result']['result'][0]['exp_match']
            applicant.location_match = result['result']['result'][0]['location_match']
            applicant.skill_match = result['result']['result'][0]['skill_match']
            applicant.role_match = result['result']['result'][0]['role_match']
            applicant.matching_score = result['result']['result'][0]['matching_score']

            # Search by name or other criteria
            action = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'INFO!',
                    'message': 'Resume scoring results are now available.',
                    'sticky': True,  # Set to True if you want the notification to be sticky
                }
            }

            return action

        except Exception as e:
            print(e)
            action = {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'ERROR!',
                    'message': 'Unable to fetch Resume Scoring Results.',
                    'sticky': True,  # Set to True if you want the notification to be sticky
                }
            }
            # cron_job = self.env['ir.cron'].search(
            #     [('name', '=', f'Resume Matching API Polling task - {applicant.task_id}')])
            # if cron_job:
            #     cron_job.write({'active': False})
            applicant.task_id = None
            if applicant.matching_score > 0 or applicant.matching_score is not None:
                applicant.is_scoring_triggered = "received"
            else:
                applicant.is_scoring_triggered = "never"

            return action
