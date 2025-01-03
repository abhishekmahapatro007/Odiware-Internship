from odoo import fields, models, api


class SubHistory(models.Model):
    _name = 'sub.recharge.history'
    _description = 'Records the history of a customer/client recharges'

    date_recharge = fields.Date(required=True)
    customer_id = fields.Many2one('odi.customer.credit', required=True)
    plan_id = fields.Many2one('odi.sub.plan', required=True)