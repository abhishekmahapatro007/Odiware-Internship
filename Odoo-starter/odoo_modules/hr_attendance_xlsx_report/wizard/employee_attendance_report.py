# -*- coding: utf-8 -*-
#############################################################################
#
#    Odiware Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Odiware Technologies(<https://www.odiware.com>)
#    Author: Odiware Technologies(<https://www.odiware.com>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
import io
import json
from datetime import datetime, date
from dateutil.rrule import rrule, DAILY

from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils
from datetime import datetime, date

try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter


class EmployeeAttendanceReport(models.TransientModel):
    """ Wizard for Employee Attendance Report """
    _name = 'employee.attendance.report'
    _description = 'Employee Attendance Report Wizard'

    from_date = fields.Date('From Date', help="Starting date for report")
    to_date = fields.Date('To Date', help="Ending date for report")
    employee_ids = fields.Many2many('hr.employee', string='Employee',
                                    help='Name of Employee')

    def action_print_xlsx(self):
        """
        Returns report action for the XLSX Attendance report
        Raises: ValidationError: if From Date > To Date
        Raises: ValidationError: if there is no attendance records
        Returns:
            dict:  the XLSX report action
        """
        if not self.from_date:
            self.from_date = date.today()
        if not self.to_date:
            self.to_date = date.today()
        if self.from_date > self.to_date:
            raise ValidationError(_('From Date must be earlier than To Date.'))
        attendances = self.env['hr.attendance'].search(
            [('employee_id', 'in', self.employee_ids.ids)])
        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'employee_ids': self.employee_ids.ids
        }
        if self.employee_ids and not attendances:
            raise ValidationError(
                _("There is no attendance records for the employee"))
        if self.from_date and self.to_date:
            return {
                'type': 'ir.actions.report',
                'data': {'model': 'employee.attendance.report',
                         'options': json.dumps(
                             data, default=date_utils.json_default),
                         'output_format': 'xlsx',
                         'report_name': 'Attendance Report',
                         },
                'report_type': 'xlsx',
            }

    def get_xlsx_report(self, data, response):
        """
        Print the XLSX report
        Returns: None
        """
        global average_hours_per_day
        query = """select hr_e.id AS employee_id, hr_e.name,date(hr_at.check_in),
            SUM(hr_at.worked_hours) from hr_attendance hr_at LEFT JOIN
            hr_employee hr_e ON hr_at.employee_id = hr_e.id"""

        if not data['employee_ids']:
            query += """ GROUP BY hr_e.id, hr_e.name, date(check_in)"""

        else:
            query += """ WHERE hr_e.id in (%s) GROUP BY hr_e.id,hr_e.name, date(check_in)
            """ % (', '.join(str(employee_id)
                             for employee_id in data['employee_ids']))
        self.env.cr.execute(query)
        docs = self.env.cr.dictfetchall()
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        start_date = datetime.strptime(data['from_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['to_date'], '%Y-%m-%d').date()
        date_range = rrule(DAILY, dtstart=start_date, until=end_date)
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)
        border = workbook.add_format({'border': 1})
        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        date_size = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'center'})
        sheet.merge_range('C3:K6', 'Attendance Report', head)
        sheet.merge_range('B8:C9', 'From Date: ' + data['from_date'], date_size)
        sheet.merge_range('B10:C11', 'To Date: ' + data['to_date'], date_size)
        sheet.write(2, 12, 'P-Present')
        sheet.write(3, 12, 'A-Absent')
        sheet.write(4, 12, '0.5P-Half Day')
        sheet.write(5, 12, 'WE-Weekend')
        sheet.write(6, 12, 'H-Holidays')
        sheet.write(7, 12, 'L-Leave')
        sheet.merge_range('B16:B17', 'Sl.No', border)
        sheet.merge_range('C16:C17', 'Employee', border)

        calendar_id = self.env['resource.calendar'].search([('name', '=', 'Standard 40 hours/week')], limit=1)
        weekend_columns = []
        if calendar_id:
            # Get the working days from the calendar
            working_days = calendar_id.attendance_ids.mapped('dayofweek')

            all_days = {'0', '1', '2', '3', '4', '5', '6'}
            weekend_days = all_days - set(working_days)

            weekend_days = [int(day) for day in weekend_days]

        row = 15
        col = 2
        for date_data in date_range:
            col += 1
            day_number = date_data.weekday()
            if day_number in weekend_days:
                weekend_columns.append(col)
            sheet.write(row, col, date_data.strftime('%Y-%m-%d'), border)
        row = 16
        col = 2
        for date_data in date_range:
            col += 1
            sheet.write(row, col, date_data.strftime('%a'), border)

        employee_names = []
        attendance_list = []
        for doc in docs:
            query = """
                SELECT 
                    hr_leave.employee_id,
                    hr_leave.holiday_status_id,
                    hr_leave.request_date_from,
                    hr_leave.request_date_to,
                    hr_leave.state
                FROM 
                    hr_leave
                WHERE 
                    hr_leave.state = 'validate' AND hr_leave.employee_id = %s
            """
            self.env.cr.execute(query, (doc['employee_id'],))
            leave_records = self.env.cr.fetchall()

            if doc['name'] not in employee_names:
                date_sum_list = []
                employee_names.append(doc['name'])
                for date_data in date_range:
                    date_out = date_data.strftime('%Y-%m-%d')
                    is_leave = False
                    for leave in leave_records:
                        leave_start = leave[2]  # `request_date_from`
                        leave_end = leave[3]  # `request_date_to`

                        if leave_start <= date_data.date() <= leave_end:
                            # If the date is within an approved leave period, mark it as 'L'
                            date_sum_list.append({
                                'name': doc['name'],
                                'date': date_out,
                                'sum': 'L'  # Indicator for Leave
                            })
                            is_leave = True
                            break
                    if not is_leave:
                        record_list = list(
                            filter(
                                lambda x: x['name'] == doc['name'] and x[
                                    'date'].strftime(
                                    '%Y-%m-%d') == date_out, docs))
                        if record_list:
                            date_sum_list.append(record_list[0])
                        else:
                            date_sum_list.append({
                                'name': '',
                                'date': '',
                                'sum': 0
                            })
                attendance_list.append(
                    {'name': doc['name'], 'items': date_sum_list, 'employee_id': doc.get('employee_id')})

        holidays_columns = []
        public_holidays = self.env['resource.calendar.leaves'].search([('holiday_id', '=', False)])
        date_range_list = list(date_range)
        for holiday in public_holidays:
            holiday_start = holiday.date_from.date()  # Ensure date format
            holiday_end = holiday.date_to.date()  # Ensure date format
            for date_data in date_range_list:
                if holiday_start <= date_data.date() <= holiday_end:  # Convert date_data to date
                    holidays_columns.append(date_range_list.index(date_data) + 3)

        work = self.env.ref('resource.resource_calendar_std')
        row = 17
        i = 0
        if calendar_id:
            average_hours_per_day = calendar_id.hours_per_day

        work.hours_per_day = average_hours_per_day

        for rec in attendance_list:
            row += 1
            col = 1
            i += 1
            sheet.write(row, col, i, border)
            col += 1
            sheet.write(row, col, rec['name'], border)

            for item in rec['items']:
                col += 1

                if col in weekend_columns:
                    sheet.write(row, col, 'WE', border)
                elif col in holidays_columns:
                    sheet.write(row, col, 'H', border)
                else:
                    if isinstance(item['sum'], str):
                        if item['sum'] == 'L':
                            sheet.write(row, col, 'L', border)
                        else:
                            sheet.write(row, col, 'A', border)
                    else:
                        if item['sum'] >= work.hours_per_day:
                            sheet.write(row, col, 'P', border)
                        elif 1 <= item['sum'] <= 4 or 4 <= item['sum'] <= work.hours_per_day:
                            sheet.write(row, col, '0.5P', border)
                        else:
                            sheet.write(row, col, 'A', border)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()






