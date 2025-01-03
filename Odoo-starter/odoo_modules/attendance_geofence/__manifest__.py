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
#############################################################################
{
    'name': 'Geofence Attendance',
    'version': "17.0.1.0.0",
    'category': 'Human Resources/Attendance',
    'summary': 'Add geofencing to attendance check-ins',
    'description': """
        This module adds geofencing functionality to the Attendance module.
        Administrators can configure geofences and assign employees to them.
        Employees' locations are checked against their assigned geofence when checking in or out.
    """,
    'author': 'Odiware Technologies',
    'company': 'Odiware Technologies',
    'maintainer': 'Odiware Technologies',
    'website': 'https://www.odiware.com',
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/geofence_views.xml',
        'views/hr_attendance_views.xml',
    ],
    'external_dependencies': {
        'python': ['geopy'],
    },
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}