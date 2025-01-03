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
    'name': "Recruitment Dashboard",
    'summary': """At-a-glance View for Recruitment Module""",
    'description': """
        This module adds a dashboard in recruitment module. Users can
        view at-a-glance various information about the recruitment stages
        and the progress. Other related metrics time to hire, time to fill are also shown.
    """,
    'category': 'Human Resources/Recruitment',
    'version': '1.0.8',
    'author': 'Odiware',
    'company': 'Odiware Technologies Pvt Ltd',
    'maintainer': 'Odiware',
    'website': "https://www.odiware.com/",
    'depends': ['base', 'web', 'hrms_recruitment', 'hr_recruitment'],
    'data': [
        'views/dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'recruitment_dashboard/static/src/js/recruitment_dashboard.js',
            # 'recruitment_dashboard/static/src/css/lib/nv.d3.css',
            'recruitment_dashboard/static/src/css/dashboard.css',
            # 'recruitment_dashboard/static/src/css/style.scss',
            # 'recruitment_dashboard/static/src/js/lib/d3.min.js',
            'recruitment_dashboard/static/src/xml/payroll_dashboard.xml'
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/img/filename_screenshot.png', 'static/img/filename2.png'],
    'price': '',
    'currency': 'USD'
}
