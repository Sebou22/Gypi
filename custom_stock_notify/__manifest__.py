# -*- coding: utf-8 -*-
{
    'name': "Stock Notification",
    'summary': """
        Custom Stock Notification
    """,
    'author': "Asmaa KHALLOUT",
    'category': 'Custom Development',
    'version': '16.0.1.0.0',
    'description': """
        This module will add feature on ecommerce 'notify me when product will be available.'
    """,
    'depends': ['website_sale_stock','custom_addon'],
    'data': [
        'views/website_template_inherit.xml',
        'views/availability_email_body_inherit.xml',
    ],
    'assets': {
        'web.assets_frontend': ['/custom_stock_notify/static/src/xml/website_sale_stock_product.xml',],
    },

    'installable': True,
    'application': False,
}
