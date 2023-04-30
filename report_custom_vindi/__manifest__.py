# -*- encoding: utf-8 -*-
{
    'name': 'Report Vindi',
    'author': 'KHALLOUT Asmaa',
    "license": "AGPL-3",
    "version": "16.0.1",
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_features_views.xml',
        'views/product_template_views_inherit.xml',
        'templates/report_delivery_document_inherit.xml',
        'templates/report_saleorder_document_inherit.xml',
        'templates/report_purchaseorder_document_inherit.xml',
        'templates/report_invoice_document_inherit.xml',
        'views/payment_mode_views.xml',
        'views/account_payment_view_inherit.xml',
        'wizard/account_payment_register_views_inherit.xml',

    ],
     'installable': True,
}
