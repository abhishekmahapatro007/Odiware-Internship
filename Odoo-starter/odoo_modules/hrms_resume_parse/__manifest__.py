# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Resume Parser for Recruitment',
    'version': '1.0',
    'category': 'Odiware/Resume Parser for Recruitment',
    'summary': 'Parse the Uploaded Resumes',
    'depends': [
        'base',
        'hr',
        'attachment_indexation',
        'hrms_recruitment',
        'odi_subscription_tracker',
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
            'hrms_resume_parse/static/src/**/*',
        ],
    },
    "external_dependencies": {"python": ["openai==0.28", "pymupdf", "python-docx"]},
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
