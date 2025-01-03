from odoo import fields, models, api


class OdiSubscriptionPlan(models.Model):
    _name = 'odi.sub.plan'
    _description = 'Records all the plans that will be used by our organization'

    plan_name = fields.Char(required=True)
    plan_advertised_name = fields.Char(required=True, help="The name that will be shown on websites corresponding to this plan")
    credits_recharge = fields.Integer(required=True)

    def _compute_display_name(self):
        for record in self:
            record.display_name = f"{record.plan_advertised_name}"

