import json

from odoo import http
from odoo.http import request


class VerificationController(http.Controller):

    @http.route('/odi/subscription/verify', auth='public', methods=['GET'], csrf=False)
    def verify_api(self, **kwargs):
        auth_header = request.httprequest.headers.get('Authorization')

        if auth_header:
            if auth_header.startswith('Odi_Api '):
                # Decode and split the credentials
                credentials = auth_header[8:]  # Remove 'Odi_Api '
                if not credentials:
                    return json.dumps({
                        'status': 'error',
                        'error': 'API key was not provided! Please provide an API key.',
                    })

                # Validate user credentials
                found_api = request.env['odi.api.key'].sudo().search([('api_key', '=', credentials)], limit=1)
                # found_api = request.env['odi.api.key'].test(credentials)
                if found_api:
                    company = found_api.mapped('odi_customer_id')
                    # print(company.name)
                    curr_balance, warning = (request.env['odi.customer.credit']
                                             .sudo()
                                             .verify_balance(company.id))

                    response = {
                        "status": "success",
                        "balance": curr_balance,
                        "warning": warning
                    }

                    return json.dumps(response)

                else:
                    return json.dumps({
                        'status': 'error',
                        'error': 'Incorrect API key provided.',
                    })

        # If no authentication header is present
        return json.dumps({
            'status': 'error',
            'error': 'API key was not provided! Please provide an API key.',
        })
