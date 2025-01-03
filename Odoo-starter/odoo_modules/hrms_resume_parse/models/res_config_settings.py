import json
import logging
import os
import requests

from odoo import api, fields, models, exceptions

_logger = logging.getLogger(__name__)

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(
        string="API Key",
        config_parameter='hrms_resume_parse.api_key',
        help="API key to authenticate the usage of Resume Parser in Recruitment module"
    )
    balance = fields.Float(
        string="Balance",
        help="Shows the amount of usage left on the parsing API",
        readonly=True
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res['balance'] = float(self.env['ir.config_parameter'].sudo().get_param('hrms_resume_parse.balance', '0'))
        # print("getting values in hrms resume parser")
        return res

    def set_values(self):
        try:
            current_value = self.env['ir.config_parameter'].sudo().get_param('hrms_resume_parse.api_key')
            api_key = self.api_key
            # print(current_value, "----------", api_key)

            if api_key and current_value != api_key:
                data, err = self._validate_api_key(api_key)
                if err != 200:
                    raise exceptions.ValidationError(err or "The API key couldn't be verified")
                
                self.env['ir.config_parameter'].sudo().set_param('hrms_resume_parse.balance', data['balance'])

            if not api_key:
                self.env['ir.config_parameter'].sudo().set_param('hrms_resume_parse.balance', 0)

            super().set_values()
        except ValueError as e:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Error",
                    'message': str(e),
                    'type': 'danger',  # 'danger', 'info', 'success', 'warning'
                    'sticky': True,
                }
            }
        except Exception as e:
            _logger.debug(e)
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': "Error",
                    'message': "Unexpected Error has occurred",
                    'type': 'danger',  # 'danger', 'info', 'success', 'warning'
                    'sticky': True,
                }
            }

    @api.model
    def _validate_api_key(self, api_key: str) -> [dict[str, float], int|str]:
        odi_server = os.environ.get("ODIWARE_SERVER_ADDR", "http://localhost:8069")
        response = requests.get(
            f"{odi_server}/odi/subscription/verify",
            headers={
                # "Content-Type": "application/json",
                "Authorization": f"Odi_Api {api_key}",
            }
        )

        _logger.debug("\n\n", response.text, response.status_code, "\n\n", exc_info=True)
        if response.status_code != 200:
            return {"balance": 0}, response.text or response.status_code

        # response_rpc = response.json().get("result")
        # _logger.debug(f"RESPONSE :::=========== \n{response_rpc}", exc_info=True)
        response_data = json.loads(response.text)
        # print(parsed_data.get("status"))
        if response_data.get("status") == "error":
            err = response_data.get("error", "Unable to verify the API")
            _logger.error(f"ERROR DURING VERIFICATION - {err}", exc_info=True)
            return {"balance": 0}, err or "Error during verification of API key"
        
        # self.balance = data.balance
        return {"balance": response_data.get("balance", 0)}, 200


