# -*- coding: utf-8 -*-
#############################################################################
#
#    Odiware Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Odiware Technologies(<https://my.odiware.com>)
#    Author: Odiware Technologies (<https://my.odiware.com>)
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
{
    'name': 'Job Feed Manager',
    'summary': "Basic module for managing the job feed that will be distributed with various Job Posting websites.",
    'description': """The modules primary objective is to manage
    the job feed for users to add jobs into the XML file and remove it as needed,
    and have the XML file be publically available for various Job Posting sites to parse and process.""",
    'category': 'Odiware/Job Feed Manager',
    'version': "0.1",
    'depends': ['hrms_recruitment'],
    'author': 'Odiware',
    'company': 'Odiware Technologies',
    'maintainer': 'Odiware',
    'website': "https://my.odiware.com",
    'data': [
        'security/ir.model.access.csv',
        'views/hr_job_views.xml',
        'wizard/linkedinpost_wizard.xml',
        'wizard/postjobfree_wizard.xml',
    ],
    'external_dependencies':
        {
        'python': [],
        },
    'images': [],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
#
#############################################################################