# -*- coding: utf-8 -*-

{
    "name": "Ajout champs divers dans la fiche partenaire",
    "version": "1.0",
    "depends": ['base', 'sale', 'account'],
    "author": "Mehdi Hajji",
    "summary": "IF, RC, CNSS, ICE, TP, ...",
    'website': 'http://www.dkdigital.fr',
    "category": "BASE",
    "description": "Ajouter des infos sup",
    "init_xml": [],
    'data': [
        'views/partner_extend_view.xml',
        # 'views/report_saleorder_document.xml',
        # 'views/sale_order_extend_view.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
