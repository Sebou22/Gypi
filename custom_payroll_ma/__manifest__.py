# -*- encoding: utf-8 -*-
{
    'name': 'Paie - Maroc',
    'category': 'Human Resources',
    'author': 'KHALLOUT Asmaa',
    "license": "AGPL-3",
    "version": "16.0.1",
    'depends': ['hr_payroll','l10n_ma_hr_payroll'],

    'description': """Moroccan Payroll Custom.  """,
    'data': [
        'views/res_company_views_inherit.xml',
        'views/hr_payslip_indemnities_views.xml',
        'views/hr_contract_views_inherit.xml',
        'views/custom_pop_message_views.xml',
        'views/hr_employee_views_inherit.xml',
        'security/ir.model.access.csv',
        'report/etat_cnss.xml',
        'report/bordereau_paiement_cnss.xml',
        'report/livre_paie.xml',
        'report/reports_views.xml',
        'views/etat_9421_view.xml',
        #'report/etat_9421.xml',
        'views/report_payslip_template_inherit.xml',
        'views/bordereau_cnss.xml',
        'views/bordereau_payment.xml',
        'views/livre_paie_views.xml',

    ],
     'installable': True,
}
