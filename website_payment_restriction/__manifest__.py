# -*- coding: utf-8 -*-
{
    'name': "Website Payment Restriction",
    'summary': """
        Website Payment Restriction
    """,
    'author': "Asmaa KHALLOUT",
    'category': 'Custom Development',
    'version': '16.0.1.0.0',
    'description': """
        This module will add feature on ecommerce 'restrict payment method of customers'
    """,
    'depends': ['website_sale','base'],
    'data': [
        'views/res_partner_views_inherit.xml',
        'templates/payment_checkout_inherit_template.xml',
    ],

    'installable': True,
    'application': False,
}
