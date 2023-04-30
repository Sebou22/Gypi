# -*- coding: utf-8 -*-

{
    'name': 'Inter-Company Stock transfer',
    'version': '1.0',
    'category': 'Inventory/Inventory',
    'author': 'Craftsync Technologies',
    'maintainer': 'Craftsync Technologies',
    'summary': 'Transfer stock from one company to other company without SO/PO',
    'website': 'https://www.craftsync.com',
    'description': """
Transfer stock from one company to other child company without creating SO & PO.
================================================================================
""",
    'depends': ['stock_account'],
    'data': [
        'data/stock_location_data.xml',
        'security/ir.model.access.csv',
        'wizard/inter_company_transfer_view.xml',
        'views/stock_picking_view.xml',
    ],
    'license': 'OPL-1',
    'support':'info@craftsync.com',
    'demo': [],
    'images': ['static/description/main_screen.png'],
    'price': 29.99,
    'currency': 'USD',
    'installable': True,
    'application': False,
    'auto_install': False,
}
