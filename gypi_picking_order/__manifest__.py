# -*- coding: utf-8 -*-
{
    'name': "Custom Preparation Delivery",
    'summary': """
        Custom Preparation Delivery
    """,
    'author': "Asmaa KHALLOUT",
    'category': 'Custom Development',
    'version': '16.0.1.0.0',
    'description': """
        This module will add section preparation orders
    """,
    'depends': ['sale','stock','custom_addon'],
    'data': [
        'views/preparation_order_views.xml',
        'views/stock_picking_inherit.xml',
        'views/preparation_menu_views.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'report/report_preparation_order.xml',
        'report/preparation_report_views.xml',
    ],

    'installable': True,
    'application': False,
}
