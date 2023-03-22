# See LICENSE file for full copyright and licensing details.

{
    "name": "Custom Addon",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Custom Addon",
    "author": "Asmaa KHALLOUT, DKgroup",
    "website": "https://dkgroup.fr",
    "maintainer": "DK group",
    "images": [],
    "depends": ['base','product','website_sale','website_sale_stock'],
    "data": [
        "views/product_template_inherit_views.xml",
        "templates/website_sale_product_inherit_template.xml",
        "views/product_public_category_inherit_views.xml",
        "data/website_sale_access.xml",
        'views/cart_lines_inherit.xml',
        'views/sale_order_inherit_views.xml',
        'templates/option_header_brand_logo_inherit.xml',
        'views/stock_picking_inherit_views.xml',
        'views/res_partner_inherit_views.xml',
    ],
    "installable": True,
    'assets': {
        'web.assets_frontend': [
            'custom_addon/static/src/js/add_comment.js',
        ],
    },
}
