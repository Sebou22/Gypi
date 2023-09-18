# -*- encoding: utf-8 -*-
{
    'name': 'Odoo Mirakl Integration',
    'category': 'Integration',
    'version': '16.0',
    'description': "",
    'installable': True,
    'depends': ['sale_management','product','base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/view.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
