import json
import logging

from odoo import http
from odoo.http import request
from ..utils.gpt3_resume_parser import main as resume_parser

_logger = logging.getLogger(__name__)

class VerificationController(http.Controller):

    @http.route(['/odi/action/resume/parse'], type='json', auth='public', methods=['POST'], csrf=False)
    def pay_api(self, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')
        data = request.get_json_data()
        # print(">>>>>>>>>>>>> ",data, auth_header)
        if auth_header:
            if auth_header.startswith('Odi_Api '):
                # Decode and split the credentials
                try:
                    credentials = auth_header[8:]  # Remove 'Odi_Api '
                    if not credentials:
                        return json.dumps({
                            'status': 'error',
                            'error': 'API key was not provided! Please provide an API key.',
                        })

                    found_api_key = request.env['odi.api.key'].sudo().search([('api_key', '=', credentials)], limit=1)
                    if found_api_key:
                        company = found_api_key.mapped('odi_customer_id')
                        new_balance, warning = request.env['odi.customer.credit'].sudo().verify_deduct_balance(
                            company.id, "resume_parsing")

                        if new_balance < 0:
                            response = {
                                "status": "error",
                                "data": "",
                                "error": warning
                            }
                            return json.dumps(response)

                        resume_data, parse_err = resume_parser(data.get("resume"))
                        _logger.debug(f"\n{resume_data}\n\n")

                        if parse_err:
                            if parse_err == "Unknown file type received":
                                return json.dumps({
                                    'status': 'error',
                                    'error': 'Incorrect file type received'
                                })
                            else:
                                # company.balance = new_balance
                                return json.dumps({
                                    'status': 'error',
                                    # 'balance': new_balance,
                                    'error': parse_err
                                })
                                ###############################################################################

                        company.balance = new_balance  # setting the new deducted balance to company instance.
                        return json.dumps({
                            'status': 'success',
                            'data': resume_data,
                            'balance': new_balance,
                            'warning': warning
                        })
                    else:
                        return json.dumps({
                            'status': 'error',
                            'error': 'Incorrect API key provided.',
                        })
                except ValueError as e:
                    return json.dumps({
                        'status': 'error',
                        'error': str(e),
                    })
                except Exception as e:
                    _logger.error(f"Error occurred in parse controller: {e}")
                    return json.dumps({
                        'status': 'error',
                        'error': 'Unexpected Error has occurred. Unable to parse resume.',
                    })
            else:
                err_data = json.dumps({
                    'status': 'error',
                    'error': 'Incorrect API Authorization used'
                })
                return err_data
                # return request.make_json_response(err_data, status=401)
        # If no authentication header is present
        # return request.make_json_response(json.dumps({
        #     'status': 'error',
        #     'error': 'API key was not provided! Please provide an API key.',
        # }), status=401)
        return json.dumps({
            'status': 'error',
            'error': 'API key was not provided! Please provide an API key.',
        })
        # return Response('Unauthorized', status=401)

    @http.route(['/internal/action/resume/parse'], type='json', auth='public', methods=['POST'], csrf=False)
    def pay_api_internal(self, **kwargs):
        try:
            data = request.get_json_data()

            response_data, parse_err = resume_parser(data.get("resume"))
            _logger.debug(f"\n{response_data},\n{parse_err}")

            if parse_err:
                raise ValueError(parse_err)

            # compatible_data = compatibility_layer_gippity(response_data)
            return json.dumps({
                'status': 'success',
                'data': response_data,
                'warning': ''
            })
        except ValueError as e:
            return json.dumps({
                'status': 'error',
                'error': str(e),
            })
        except Exception as e:
            _logger.error(f"Couldn't parse the resume \n{e}")

            return json.dumps({
                'status': 'error',
                'error': "Unable to parse the resume",
            })

