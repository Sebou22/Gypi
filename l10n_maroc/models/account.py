# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Account(models.Model):
    _inherit = "account.account"

    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("asset_cash", "Bank and Cash"),
            ("asset_current", "Current Assets"),
            ("asset_non_current", "Non-current Assets"),
            ("asset_prepayments", "Prepayments"),
            ("asset_fixed", "Fixed Assets"),
            ("liability_payable", "Payable"),
            ("liability_credit_card", "Credit Card"),
            ("liability_current", "Current Liabilities"),
            ("liability_non_current", "Non-current Liabilities"),
            ("equity", "Equity"),
            ("equity_unaffected", "Current Year Earnings"),
            ("income", "Income"),
            ("income_other", "Other Income"),
            ("expense", "Expenses"),
            ("expense_depreciation", "Depreciation"),
            ("expense_direct_cost", "Cost of Revenue"),
            ("off_balance", "Off-Balance Sheet"),
            ("tres_actif", "Trésorerie actif"),
            ("tres_passif", "Trésorerie passif"),
        ],
        string="Type", tracking=True,
        required=True,
        compute='_compute_account_type', store=True, readonly=False, precompute=True,
        help="Account Type is used for information purpose, to generate country-specific legal reports, and set the rules to close a fiscal year and generate opening entries."
    )

    # @api.model
    # def create(self, vals):
    #     print('vals', vals['group_id'])
    #     if not vals['group_id']:
    #         digits = vals['code'][0:3]
    #         group_id = self.env['account.group'].search([('code_prefix_start', '=', digits)])
    #         vals['group_id'] = group_id.id
    #     res = super(Account, self).create(vals)

    #     return res
    
class AccountAccountTemplate(models.Model):
    _inherit = "account.account.template"

    account_type = fields.Selection(
        selection=[
            ("asset_receivable", "Receivable"),
            ("asset_cash", "Bank and Cash"),
            ("asset_current", "Current Assets"),
            ("asset_non_current", "Non-current Assets"),
            ("asset_prepayments", "Prepayments"),
            ("asset_fixed", "Fixed Assets"),
            ("liability_payable", "Payable"),
            ("liability_credit_card", "Credit Card"),
            ("liability_current", "Current Liabilities"),
            ("liability_non_current", "Non-current Liabilities"),
            ("equity", "Equity"),
            ("equity_unaffected", "Current Year Earnings"),
            ("income", "Income"),
            ("income_other", "Other Income"),
            ("expense", "Expenses"),
            ("expense_depreciation", "Depreciation"),
            ("expense_direct_cost", "Cost of Revenue"),
            ("off_balance", "Off-Balance Sheet"),
            ("tres_actif", "Trésorerie actif"),
            ("tres_passif", "Trésorerie passif"),
        ],
        string="Type",
        help="These types are defined according to your country. The type contains more information "\
        "about the account and its specificities."
    )
