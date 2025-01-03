# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resume Reader for Recruitment',
    'version': '0.8',
    'category': 'Odiware/Resume Reader for Recruitment',
    'summary': 'Read the Uploaded Resumes',
    'depends': [
        # 'base',
        # 'hr',
        # 'attachment_indexation',
        'hrms_recruitment'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizards/create_applicant_wizard_view.xml',
        'views/hr_job_views.xml',
        'views/hr_applicant_views.xml',
        'views/res_config_settings_views.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'hrms_resume_reader/static/src/**/*',
        ],
    },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
