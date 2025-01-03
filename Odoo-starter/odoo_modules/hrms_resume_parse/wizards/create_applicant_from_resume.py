import json
import logging
import os
from typing import Any
import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)

class HrApplicantFromResume(models.TransientModel):
    _name = 'applicant.record.wizard'
    _description = 'Create new record from a resume upload'

    resume = fields.Binary("Resume Upload", required=True)
    file_name = fields.Char(string='File Name')
    parse_success = fields.Boolean(default=False)

    job_id = fields.Integer()
    application_name = fields.Char("Application Name", required=True)
    name = fields.Char("Applicant's Name")
    email = fields.Char("Applicant's Email")
    phone = fields.Char("Applicant's Phone")
    total_experience = fields.Char("Total Experience")
    linkedin_profile = fields.Char("Linkedin Profile URL")
    current_organization = fields.Char("Current Organization")
    current_city_ids = fields.Char("Current City")
    type_id = fields.Integer()

    def action_on_click_parse_btn(self):
        # x = True
        #
        user_res = self.env.user
        if not user_res:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Error",
                    'message': "Couldn't acquire correct user. Action aborted.",
                    'type': 'danger',  # 'danger', 'info', 'success', 'warning'
                    'sticky': True,  # Set to True to show it until dismissed
                }
            }
        # # if user_res:
        # #     _logger.debug(user_res.id)
        #
        #
        # if x:
        #     return {
        #         'type': 'ir.actions.client',
        #         'tag': 'display_notification',
        #         'params': {
        #             'title': "Error",
        #             'message': "TESTTEST TEST",
        #             'type': 'danger',  # 'danger', 'info', 'success', 'warning'
        #             'sticky': True,  # Set to True to show it until dismissed
        #         }
        #     }
        parsed_data, ok = self.parse_pdf(self.resume)

        if not ok:
            err = parsed_data
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Error",
                    'message': err,
                    'type': 'danger',  # 'danger', 'info', 'success', 'warning'
                    'sticky': True,  # Set to True to show it until dismissed
                }
            }

        # print(parsed_data)
        new_balance = parsed_data.get("balance")
        self.name = parsed_data.get("name", "")
        self.email = parsed_data.get('email', "")
        self.total_experience = f"{parsed_data.get('total_exp', '0')}"
        self.phone = parsed_data.get('contact', "")
        self.current_city_ids = parsed_data.get('current_city', "")
        self.current_organization = parsed_data.get("curr_org", "")
        self.linkedin_profile = parsed_data.get("linkedin_url", "")

        degree_parsed = parsed_data.get("edu", None)
        recruitment_deg_model = self.env['hr.recruitment.degree']
        if degree_parsed is not None:
            deg_in_db = recruitment_deg_model.search([('name', '=', degree_parsed)])
            if len(deg_in_db) < 1:
                new_deg_created = recruitment_deg_model.create({
                    'name': degree_parsed
                })
                self.type_id = new_deg_created.id
            else:
                self.type_id = deg_in_db[0].id

        skills_parsed: Any = parsed_data.get("cluster", {})

        applicant_model = self.env['hr.applicant']

        applicant_record = applicant_model.create({
            'job_id': self.job_id,
            'name': self.application_name,
            'partner_name': self.name,
            'email_from': self.email,
            'total_experience': self.total_experience,
            'partner_phone': self.phone,
            'current_city_ids': self.current_city_ids,
            'current_organization': self.current_organization,
            'linkedin_profile': self.linkedin_profile,
            'type_id': self.type_id,
            'priority': "0",
            'user_id': user_res.id
        })

        applicant_id = applicant_record.id

        self.env['ir.attachment'].create({
            'name': self.file_name,
            'type': 'binary',
            'datas': self.resume,
            'res_model': 'hr.applicant',
            'res_id': applicant_id,
        })
        # print("\n\n\n\n", skills_parsed)

        # if applicant_record and self.job_id:
        #     applicant_record.job_id = self.job_id

        for skill_group in skills_parsed:
            # print(skill_group.get("cluster", "Nothing found"))

            skill_type_parsed: str|None = skill_group.get("cluster", None)
            if skill_type_parsed is None:
                # raise ValidationError("There was a parsing error. Unable to parse skills.")
                continue
            # endif

            # skill_type_parsed = string.capwords(skill_type_parsed)
            skill_list: list[str] = skill_group.get("skills", [])
            # skill_list = list(map(lambda item: string.capwords(item), skill_list))
            if len(skill_list) < 1:
                continue
            # endif

            self.search_in_skill_cluster_and_add(applicant_id, skill_type_parsed, skill_list)

        self.parse_success = True
        self.env['ir.config_parameter'].sudo().set_param('hrms_resume_parse.balance', new_balance)
        return {
            'name': 'Add Applicant from Resume',
            'type': 'ir.actions.act_window',
            'res_model': 'hr.applicant',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'res_id': applicant_id,
        }

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

            # print("/////////////////////////\n//////////////////", domain)
            skills_record = skill_model.search(domain)

            if len(skills_record) < 1:
                print(f"None of the skills in the skill list found under cluster name ${cluster_name}")
            # endif

            parsed_skill_ids = skills_record.mapped('id')
            parsed_skill_names: list[str] = skills_record.mapped('name')
            parsed_skill_names_lowercase = list(map(lambda v: v.lower(), parsed_skill_names))
            skill_lvl_record = skill_lvl_model.search(
                [('skill_type_id', '=', skill_type_found_id), ('default_level', '=', True)], limit=1)

            # print("<<<<<<<<<<<<<<<<<<<\n\n", parsed_skill_names, parsed_skill_names_lowercase, skill_list)
            # still need to extract out skills that are not entered in db and process them as required
            parsed_unlisted_skill: list[str] = list(
                filter(lambda v: v.lower() not in parsed_skill_names_lowercase, skill_list))

            # print("<<<<<<<<<", parsed_unlisted_skill, parsed_skill_names)

            if len(parsed_unlisted_skill) > 0:
                try:
                    self.add_hr_skill_to_existing_type(applicant_id, skill_type_found_id,
                                                       parsed_unlisted_skill, skill_lvl_record[0].id)
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

    def parse_pdf(self, pdf_file):
        # print(list(parsed_data.keys()))
        api_key = self.env['ir.config_parameter'].sudo().get_param('hrms_resume_parse.api_key', '0')
        _logger.debug(api_key)
        if api_key == '0':
            # raise UserError("You do not have API key entered the settings.") # This did not work for unknown reasons
            return "You do not have Resume Parser API key entered in the settings. Go to Settings > Recruitment. You can find the section to enter the API key provided by Odiware Technologies.", False
            # return {
            #     'type': 'ir.actions.client',
            #     'tag': 'display_notification',
            #     'params': {
            #         'title': "Error",
            #         'message': "You do not have Resume Parser API key entered in the settings. Go to Settings > Recruitment. You can find the section to enter the API key provided by Odiware Technologies.",
            #         'type': 'danger',  # 'danger', 'info', 'success', 'warning'
            #         'sticky': True,  # Set to True to show it until dismissed
            #     }
            # }

        # allowed =  requests.get("https://your-api-endpoint.com/validate", headers={"Authorization": f"Bearer {api_key}"})
        """
            Status Code
                200 -> Success. Allowed to proceed.
                400 -> Failed or denied. Response has more details.
                401 -> Unauthorized.
        """
        try:

            # skill = self.env['hr.skill']
            # applicant_skill_model = self.env['hr.applicant.skill']
            # skill_type_model = self.env['hr.skill.type']
            # skill_lvl_model = self.env['hr.skill.level']

            if self.resume:
                # attachment = applicant.attachment_ids[0]
                # print(attachment.datas)
                # print(attachment.res_name, attachment.store_fname, attachment.local_url)
                # ~~~~~~
                # DAXTRA PARSING
                # dax_tkn = get_access_tkn()
                # parsed_data = submit_resume(dax_tkn, attachment.datas)
                # ~~~~~~
                try:
                    odi_server = os.environ.get("ODIWARE_SERVER_ADDR", "http://localhost:8069")
                    json_data_to_send = pdf_file.decode('utf-8')
                    parsing_api = requests.post(
                        f"{odi_server}/odi/action/resume/parse",
                        headers={
                            "Content-Type": "application/json",
                            'Authorization': f"Odi_Api {api_key}"
                        },
                        data=json.dumps({"resume": json_data_to_send})
                    )
                    # print("\n\n\n",parsing_api.status_code, "\n", parsing_api.json())
                    parsed_result = parsing_api.json().get("result")
                    # print(parsed_result, parsed_result.status, parsed_result.text)
                    response_data = json.loads(parsed_result)

                    if response_data.get("status") == "error":
                        err = response_data.get("error", "Failed to parse resume.")
                        return err, False
                        # action = {
                        #     'type': 'ir.actions.client',
                        #     'tag': 'display_notification',
                        #     'params': {
                        #         'title': 'Warning!',
                        #         'message': err,
                        #         'sticky': True,  # Set to True if you want the notification to be sticky
                        #         'type': 'danger'
                        #     }
                        # }
                        #
                        # return action

                except Exception as e:
                    _logger.error(e)
                    return "Unexpected error occurred while parsing the resume", False
                    # action = {
                    #     'type': 'ir.actions.client',
                    #     'tag': 'display_notification',
                    #     'params': {
                    #         'title': 'Warning!',
                    #         'message': "Unexpected error occurred while parsing the resume",
                    #         'sticky': True,
                    #         'type': 'danger'
                    #     }
                    # }
                    #
                    # return action

                if response_data is None:
                    return "Unable to parse the resume", False
                    # action = {
                    #     'type': 'ir.actions.client',
                    #     'tag': 'display_notification',
                    #     'params': {
                    #         'title': 'Warning!',
                    #         'message': "Unable to parse the resume",
                    #         'sticky': True,
                    #     }
                    # }
                    #
                    # return action
                # endif
                parsed_data = response_data.get("data", {})
                new_bal = response_data.get("balance", 0)
                parsed_data["balance"] = new_bal
                return parsed_data, True
            # endif
            else:
                return "No resume was attached", False
        # endtry
        except Exception as e:
            _logger.error(f"This error has occurred: {e}")
            return "Unexpected error occurred, cannot parse resume", False

        # endexcept

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
            raise e

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
            raise e