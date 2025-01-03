from odoo import fields, models, api
import secrets, base64, hashlib


class OdiServiceCost(models.Model):
    _name = 'odi.service.cost'
    _description = 'Stores the cost of using a odiware service each time. The amount will be in terms of credits.'
    # _order = 'write_date desc'

    name = fields.Char("Service Name", required=True)
    internal_name = fields.Char("Internal Service Name", required=True)
    service_cost = fields.Float("Service Cost", required=True)
    # odi_customer_id = fields.Many2one("odi.customer.credit", string="Customer", required=True)
    # state = fields.Selection(
    #     [('active', 'Active'), ('expired', 'Expired'), ('pause', 'Pause')],
    #     string="Status",
    #     default='active'
    # )

    # @api.model
    # def default_get(self, fields_list):
    #     defaults = super(OdiApiKey, self).default_get(fields_list)
    #     defaults['api_key'] = self.generate_api_key("zigzag")
    #     return defaults