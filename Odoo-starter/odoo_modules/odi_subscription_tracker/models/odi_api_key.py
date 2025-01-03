from odoo import fields, models


class OdiApiKey(models.Model):
    _name = 'odi.api.key'
    _description = 'Stores the API keys of the customer/client'
    _order = 'write_date desc'

    api_key = fields.Char(string="API Key", readonly=True)
    odi_customer_id = fields.Many2one("odi.customer.credit", string="Customer", required=True)
    state = fields.Selection(
        [('active', 'Active'), ('expired', 'Expired'), ('pause', 'Pause')],
        string="Status",
        default='active'
    )

    # @api.model
    # def default_get(self, fields_list):
    #     defaults = super(OdiApiKey, self).default_get(fields_list)
    #     # print(">>>>>>>>>>>>>", self.env['odi.customer.credit'].browse(self.env.context['params']['id']))
    #     company_name: Any = False
    #     if self.env.context['params']['model'] == "odi.customer.credit":
    #         company_name = self.env['odi.customer.credit'].browse(self.env.context['params']['id'])
    #     defaults['api_key'] = self.generate_api_key(company_name.name if company_name else "zigzag")
    #     return defaults

    # @api.model
    # def generate_api_key(self, name, length=32):
    #     if not name:
    #         raise exceptions.ValidationError("Please save a name for the Customer before trying to set an API")
    #     # random bytes
    #     random_bytes = secrets.token_bytes(length)
    #     combined = name + base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    #     api_key = hashlib.sha256(combined.encode()).hexdigest()
    #
    #     ok = self.check_if_uniq_api(api_key)
    #     if not ok:
    #         self.generate_api_key(name, length)
    #
    #     return api_key[:length]