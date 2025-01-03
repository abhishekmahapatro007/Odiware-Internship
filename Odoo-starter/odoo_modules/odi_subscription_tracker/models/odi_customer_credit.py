import base64
import hashlib
import logging
import secrets
from datetime import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class OdiCustomerCredit(models.Model):
    _name = "odi.customer.credit"
    _description = "Table holding all the records of customers and their credit limits"
    # _order = "id desc"

    name = fields.Char(required=True, string='Company Name')
    balance = fields.Integer(string='Credit Balance', required=True)
    # current_usage = fields.Integer(string='Credit Used', required=True, default=0)
    # last_topup = fields.Date(string='Last Credit Recharge', required=True)
    api_key_ids = fields.One2many("odi.api.key", "odi_customer_id", string='API Keys')
    recharge_history_ids = fields.One2many("sub.recharge.history", "customer_id", string='Recharge History')

    def action_on_click_generate_api_key(self):
        api_key_instance = self.env['odi.api.key']
        for rec in self:
            api_key_instance.create({
                "api_key": self.generate_api_key(rec.name),
                "odi_customer_id": rec.id,
                "state": 'active'
            })

    @api.model
    def generate_api_key(self, name, length=32):
        if not name:
            raise ValidationError("Please save a name for the Customer before trying to set an API")
        # random bytes
        random_bytes = secrets.token_bytes(length)
        combined = name + base64.urlsafe_b64encode(random_bytes).decode('utf-8')
        api_key = hashlib.sha256(combined.encode()).hexdigest()

        ok = self.check_if_uniq_api(api_key)
        if not ok:
            self.generate_api_key(name, length)

        return api_key[:length]

    @api.model
    def check_if_uniq_api(self, api_key):
        api_key_inst = self.env['odi.api.key']
        record = api_key_inst.search([('api_key', '=', api_key)])
        if record:
            return False

        return True

    @api.model
    def add_credit(self, plan, org_id: int):
        if not plan:
            return False, "Did not get any plans to recharge"
        success, err = self.match_recharge_plan(org_id, plan)
        return success, err
        # match plan:
        #     case "Basic":
        #
        #     case "Large":
        #         success, err = self.match_recharge_plan(org_id, 'large')
        #         return success, err
        #
        #     case _:
        #         _logger.warning(f'Suspicious behavior - Someone hit this endpoint looking for this plan -> {plan}')
        #         return False, "Plan doesn't exist"

    @api.model
    def match_recharge_plan(self, org_id, plan_name):
        plan_model = self.env['odi.sub.plan']
        recharge_history_model = self.env['sub.recharge.history']

        org = self.browse(org_id)
        _logger.debug(org)

        found_plan = plan_model.search([('plan_name', '=', plan_name)])
        if not found_plan:
            _logger.warning(f'Suspicious behavior - Someone hit this endpoint looking for this plan -> {plan_name}')
            return False, "Plan doesn't exist"

        credit_to_add = found_plan.credits_recharge

        recharge_history_model.create({
            'date_recharge': datetime.now(),
            'customer_id': org_id,
            'plan_id': found_plan.id
        })

        bal = org.balance
        org.balance = bal + credit_to_add

        return True, None

    def verify_deduct_balance(self, org_id, service):
        org = self.browse(org_id)
        service_cost_model = self.env['odi.service.cost']
        service_cost_inst = service_cost_model.search([('internal_name', '=', service)], limit=1)
        if len(service_cost_inst) < 1:
            _logger.error("Unable to find the service requested in the verify_deduct_balance method.", exc_info=True)
            return -1, "Internal server error"

        serv_cost = service_cost_inst[0].service_cost
        current_balance = org.balance
        new_balance = current_balance - serv_cost

        if current_balance <= 0:
            _logger.exception("Balance of an record in Odi Subscription Tracker may have went under ZERO. If under zero, it would be unexpected.", exc_info=True)
            return -1, "Out of credits"
        if new_balance < 0:
            return 0, "Not enough credits"
        if current_balance < 30:
            return new_balance, "Low Balance. Please recharge soon."

        return new_balance, ""

    def verify_balance(self, org_id):
        org = self.browse(org_id)
        current_balance = org.balance

        if current_balance < 0:
            _logger.exception("Balance of an record in Odi Subscription Tracker has went under ZERO. This is unexpected.")
            return current_balance, "Out of credits"
        if current_balance < 30:
            return current_balance, "Low Balance. Please recharge soon."

        return current_balance, ""
