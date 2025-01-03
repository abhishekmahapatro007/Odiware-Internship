# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Odiware Subscription Tracker',
    'version': '0.1',
    'category': 'Odiware/Odiware Subscription Tracker',
    'summary': 'Manage all the customer subscription and track their credit limit and assign/change their API keys.',
    'description': """
    The Module will be used to add/remove any customer/client who uses our product/service. Each customer will have a credit
    limit that will be tracked in this module and API keys can be generated in order to let the customer use our API
    endpoint when they use our services.
    """,
     'depends': [
        'base_setup',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/odi_service_cost_views.xml',
        'views/odi_customer_credit_views.xml',
        'views/odi_api_key_views.xml',
        'views/odi_sub_plan_views.xml',
        'views/customer_menus.xml',
    ],
    'application': True,
    'license': 'LGPL-3',
}
