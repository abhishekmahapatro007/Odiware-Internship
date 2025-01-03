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
    'name': 'Recruitment Tracker',
    'version': '1.1.0',
    'category': 'Human Resources/Recruitment',
    'sequence': 10,
    'summary': 'Track your recruitment pipeline using several stages and send assessements to test them',
    'description': """
        This module adds several more fields essential for recruitment teams while
        they add applicants. It adds features like automatically sending Job Description
        to applicants and sending them assessement which applicants can fill to prove their
        expertise.
    """,
    'author': 'Odiware',
    'company': 'Odiware Technologies Pvt Ltd',
    'maintainer': 'Odiware',
    'website': 'https://www.odiware.com/',
    'depends': [
        'base',
        'hr',
        'hr_recruitment',
        'calendar',
        'utm',
        'attachment_indexation',
        'web_tour',
        'digest',
        'web',
        'survey',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sendmail_wizard.xml',
        'wizard/send_assessment.xml',
        'wizard/send_mail_tree_assessment.xml',
        'views/hr_applicant_views.xml',
        'views/hr_job_views.xml',
        'views/hrms_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'assets': {
        'web.assets_backend': [
            'hr_recruitment/static/src/**/*.js',
            'hr_recruitment/static/src/**/*.scss',
            'hr_recruitment/static/src/**/*.xml',
            'hr_recruitment/static/src/js/tours/hr_recruitment.js',
        ],
    },
    'license': 'LGPL-3',
    # 'images': ['static/img/filename_screenshot.png', 'static/img/filename2.png'],
    'price': '',
    'currency': 'USD'
}