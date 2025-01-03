from odoo import models, fields, api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    is_within_geofence = fields.Boolean(string='Within Geofence', compute='_compute_within_geofence', store=True)

    @api.depends('employee_id')
    def _compute_within_geofence(self):
        for attendance in self:
            attendance.is_within_geofence = False
            if not attendance.employee_id or not attendance.in_latitude or not attendance.in_longitude:
                continue

            employee = attendance.employee_id.exists()
            if not employee:
                continue

            if not employee.geofence_ids:
                attendance.is_within_geofence = True
                continue

            for geofence in employee.geofence_ids:
                if geofence.check_point_in_geofence(attendance.in_latitude, attendance.in_longitude):
                    attendance.is_within_geofence = True
                    break

    @api.model
    def create(self, vals):
        employee_id = vals.get('employee_id')
        if employee_id:
            employee = self.env['hr.employee'].browse(employee_id).exists()
            if not employee:
                raise UserError("The selected employee does not exist.")
            # Check if employee's geofence is associated with their work location
            if employee.work_location_id and employee.work_location_id.geofence_ids:
                if not employee.geofence_ids or employee.geofence_ids != employee.work_location_id.geofence_ids:
                    # Update employee's geofence_ids to match work location's geofence_ids
                    employee.write({
                        'geofence_ids': [(6, 0, employee.work_location_id.geofence_ids.ids)]
                    })
                    _logger.info(f"Updated employee {employee.name}'s geofence to match work location.")
            _logger.info(f"Employee Geofence: {employee.geofence_ids}")
            if employee.geofence_ids:
                if not vals.get('in_latitude') or not vals.get('in_longitude'):
                    raise UserError("Location data is required for employees with assigned geofences.")
                
                attendance = self.new(vals)
                attendance._compute_within_geofence()
                if not attendance.is_within_geofence:
                    raise UserError("You are not within your assigned geofence. Attendance cannot be recorded.")

        return super(HrAttendance, self).create(vals)