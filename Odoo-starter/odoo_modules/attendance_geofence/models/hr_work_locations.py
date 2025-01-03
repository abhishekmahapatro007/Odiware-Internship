from odoo import models, fields, api

class HrWorkLocation(models.Model):
    _inherit = 'hr.work.location'

    geofence_ids = fields.Many2many('hr.geofence', string='Geofences')