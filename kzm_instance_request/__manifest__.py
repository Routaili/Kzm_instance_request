# -*- coding: utf-8 -*-
{
    'name': "kzm_instance_request",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'contacts', 'sale_management', 'hr', 'sale'],

    # always loaded
    'data': [
        'data/activity.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/seq_data.xml',
        'data/instance_data.xml',
        'data/odoo_version_data.xml',
        'data/perimetre_data.xml',
        'views/employee_view.xml',
        'views/devis_view.xml',
        'views/perimetre_view.xml',
        'views/odoo_version_view.xml',
        'views/instance_request_view.xml',
        'wizards/bons_commande.xml',
        'report/report_instance.xml',
        'report/report_action.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
