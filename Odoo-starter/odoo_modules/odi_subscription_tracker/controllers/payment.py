from odoo import http
from odoo.http import request, Response
import logging, json

_logger = logging.getLogger(__name__)

class VerificationController(http.Controller):

    @http.route('/odi/subscription/add-credit', type='json', auth='public', methods=['POST'], csrf=False)
    def pay_api(self, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')

        data = request.get_json_data()
        _logger.debug(data)

        if auth_header:
            # Basic Authentication
            if auth_header.startswith('Odi_Api '):
                # Decode and split the credentials
                credentials = auth_header[8:]
                if not credentials:
                    return json.dumps({
                        'status': 'error',
                        'error': 'API key was not provided! Please provide an API key.',
                    })

                found_api_key = request.env['odi.api.key'].sudo().search([('api_key', '=', credentials)], limit=1)
                if found_api_key:
                    company = found_api_key.mapped('odi_customer_id')
                    _logger.debug(company.name)
                    res_check, err  = request.env['odi.customer.credit'].sudo().add_credit(data.get("plan", None), company.id)
                    if not res_check:
                        # print(">>>>>>>>>>>", err)
                        return json.dumps({
                            'status': 'error',
                            'error': err,
                        })

                    return json.dumps({
                        'status': 'success',
                        'data': "Successfully added credit amount.",
                        'warning': ''
                    })

                else:
                    return json.dumps({
                        'status': 'error',
                        'error': 'Incorrect API key provided.',
                    })

        return json.dumps({
            'status': 'error',
            'error': 'API key was not provided! Please provide an API key.',
        })

    # def add_credit(self, req: request, plan):
    #     auth_header = request.httprequest.headers.get('Authorization')
    #     credit_model = req.env['odi.customer.credit']
    #
    #     credit_model.sudo().add_credit(plan, )
