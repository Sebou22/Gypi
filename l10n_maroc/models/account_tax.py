from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.exceptions import UserError, ValidationError

import math
import logging


class InheritTAX(models.Model):
    _inherit = 'account.tax'
    
    
    def _check_repartition_lines(self, lines):
        self.ensure_one()

        base_line = lines.filtered(lambda x: x.repartition_type == 'base')
        base_line=base_line[0]
        print(base_line)
        if len(base_line) != 1:
            raise ValidationError(_("Invoice and credit note distribution should each contain exactly one line for the base."))
        
class InhertitAccountChartTemplate(models.Model):
    _inherit = 'account.chart.template'

    def _load(self, company):
        """ Installs this chart of accounts on the current company, replacing
        the existing one if it had already one defined. If some accounting entries
        had already been made, this function fails instead, triggering a UserError.

        Also, note that this function can only be run by someone with administration
        rights.
        """
        self.ensure_one()
        # do not use `request.env` here, it can cause deadlocks
        # Ensure everything is translated to the company's language, not the user's one.
        self = self.with_context(lang=company.partner_id.lang).with_company(company)
        if not self.env.is_admin():
            raise AccessError(_("Only administrators can load a chart of accounts"))

        existing_accounts = self.env['account.account'].search([('company_id', '=', company.id)])
        if existing_accounts:
            # we tolerate switching from accounting package (localization module) as long as there isn't yet any accounting
            # entries created for the company.
            if self.existing_accounting(company):
                raise UserError(_('Could not install new chart of account as there are already accounting entries existing.'))

            # delete accounting properties
            prop_values = ['account.account,%s' % (account_id,) for account_id in existing_accounts.ids]
            existing_journals = self.env['account.journal'].search([('company_id', '=', company.id)])
            if existing_journals:
                prop_values.extend(['account.journal,%s' % (journal_id,) for journal_id in existing_journals.ids])
            self.env['ir.property'].sudo().search(
                [('value_reference', 'in', prop_values)]
            ).unlink()

            # delete account, journal, tax, fiscal position and reconciliation model
            models_to_delete = ['account.reconcile.model', 'account.fiscal.position', 'account.move.line', 'account.move', 'account.journal', 'account.tax', 'account.group']
            for model in models_to_delete:
                res = self.env[model].sudo().search([('company_id', '=', company.id)])
                if len(res):
                    res.with_context(force_delete=True).unlink()
            existing_accounts.unlink()

        company.write({'currency_id': self.currency_id.id,
                       'anglo_saxon_accounting': self.use_anglo_saxon,
                       'account_storno': self.use_storno_accounting,
                       'bank_account_code_prefix': self.bank_account_code_prefix,
                       'cash_account_code_prefix': self.cash_account_code_prefix,
                       'transfer_account_code_prefix': self.transfer_account_code_prefix,
                       'chart_template_id': self.id
        })

        #set the coa currency to active
        self.currency_id.write({'active': True})

        # When we install the CoA of first company, set the currency to price types and pricelists
        if company.id == 1:
            for reference in ['product.list_price', 'product.standard_price', 'product.list0']:
                try:
                    tmp2 = self.env.ref(reference).write({'currency_id': self.currency_id.id})
                except ValueError:
                    pass

        # Set the fiscal country before generating taxes in case the company does not have a country_id set yet
        if self.country_id:
            # If this CoA is made for only one country, set it as the fiscal country of the company.
            company.account_fiscal_country_id = self.country_id
        elif not company.account_fiscal_country_id:
            company.account_fiscal_country_id = self.env.ref('base.us')

        # Install all the templates objects and generate the real objects
        acc_template_ref, taxes_ref = self._install_template(company, code_digits=self.code_digits)

        # Set default cash discount write-off accounts
        if not company.account_journal_early_pay_discount_loss_account_id:
            company.account_journal_early_pay_discount_loss_account_id = self._create_cash_discount_loss_account(
                company, self.code_digits)
        if not company.account_journal_early_pay_discount_gain_account_id:
            company.account_journal_early_pay_discount_gain_account_id = self._create_cash_discount_gain_account(
                company, self.code_digits)

        # Set default cash difference account on company
        if not company.account_journal_suspense_account_id:
            company.account_journal_suspense_account_id = self._create_liquidity_journal_suspense_account(company, self.code_digits)

        if not company.account_journal_payment_debit_account_id:
            company.account_journal_payment_debit_account_id = self.env['account.account'].create({
                'name': _("Outstanding Receipts"),
                'code': self.env['account.account']._search_new_account_code(company, self.code_digits, company.bank_account_code_prefix or ''),
                'reconcile': True,
                'account_type': 'asset_current',
                'company_id': company.id,
            })

        if not company.account_journal_payment_credit_account_id:
            company.account_journal_payment_credit_account_id = self.env['account.account'].create({
                'name': _("Outstanding Payments"),
                'code': self.env['account.account']._search_new_account_code(company, self.code_digits, company.bank_account_code_prefix or ''),
                'reconcile': True,
                'account_type': 'asset_current',
                'company_id': company.id,
            })

        if not company.default_cash_difference_expense_account_id:
            company.default_cash_difference_expense_account_id = self.env['account.account'].create({
                'name': _('Cash Difference Loss'),
                'code': self.env['account.account']._search_new_account_code(company, self.code_digits, '999'),
                'account_type': 'expense',
                'tag_ids': [(6, 0, self.env.ref('account.account_tag_investing').ids)],
                'company_id': company.id,
            })

        if not company.default_cash_difference_income_account_id:
            company.default_cash_difference_income_account_id = self.env['account.account'].create({
                'name': _('Cash Difference Gain'),
                'code': self.env['account.account']._search_new_account_code(company, self.code_digits, '999'),
                'account_type': 'income',
                'tag_ids': [(6, 0, self.env.ref('account.account_tag_investing').ids)],
                'company_id': company.id,
            })

        # Set the transfer account on the company
        company.transfer_account_id = self.env['account.account'].search([
            ('code', '=like', self.transfer_account_code_prefix + '%'), ('company_id', '=', company.id)], limit=1)

        # Create Bank journals
        self._create_bank_journals(company, acc_template_ref)

        # Create the current year earning account if it wasn't present in the CoA
        company.get_unaffected_earnings_account()

        # set the default taxes on the company
        company.account_sale_tax_id = self.env['account.tax'].search([('type_tax_use', 'in', ('sale', 'all')), ('company_id', '=', company.id)], limit=1).id
        company.account_purchase_tax_id = self.env['account.tax'].search([('type_tax_use', 'in', ('purchase', 'all')), ('company_id', '=', company.id)], limit=1).id

        return {}