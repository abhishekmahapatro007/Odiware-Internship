from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    geofence_ids = fields.Many2many('hr.geofence', string='Assigned Geofences')