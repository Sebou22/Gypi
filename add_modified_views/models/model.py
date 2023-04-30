# Copyright 2016-2017 Akretion (http://www.akretion.com)
import uuid

from itertools import groupby
from datetime import datetime, timedelta
from werkzeug.urls import url_encode

from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT

from odoo.tools.misc import formatLang

from odoo.addons import decimal_precision as dp

import re
from markupsafe import Markup
from odoo import Command
from odoo.tools import float_round
from odoo.exceptions import ValidationError
from odoo.tools import email_split, float_is_zero, float_repr, float_compare, is_html_empty
from odoo.tools.misc import clean_context, format_date


class HrExpenseAdvance(models.Model):
    _name = 'hr.expense.advance'
    _description = 'Avance sur frais professionnels'
    
    name = fields.Char(string='Advance Reference', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hr.expense.advance') or _('New')
        result = super(HrExpenseAdvance, self).create(vals)
        return result

    employee_id = fields.Many2one('hr.employee', string="Employé", required=True)
    amount = fields.Float(string="Montant de l'avance", required=True)
    remaining_amount = fields.Float(string="Montant restant", compute='_compute_remaining_amount', readonly=True)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('paid', 'Payé'),
        ('closed', 'Clôturé')
    ], string="Statut", default='draft', required=True)

    expense_ids = fields.One2many('hr.expense', 'advance_id', string="Notes de frais")

    @api.depends('amount', 'expense_ids.state')
    def _compute_remaining_amount(self):
        remaining_amount = 0
        total_exp = 0
        for advance in self:
            for x in advance.expense_ids:
                if x.state == "done":
                    total_exp = total_exp + x.total_amount
            remaining_amount = advance.amount - total_exp
            advance.remaining_amount = remaining_amount

    def action_paid(self):
        for advance in self:
            if advance.remaining_amount <= 0:
                raise UserError("Le montant restant doit être supérieur à 0 pour effectuer un paiement.")
            advance.state = 'paid'

    def action_close(self):
        for advance in self:
            if advance.remaining_amount > 0:
                raise UserError("Le montant restant doit être égal à 0 pour clôturer une avance.")
            advance.state = 'closed'

            
            
            
class HrExpenseSheet(models.Model):
    _inherit = "hr.expense.sheet" 
    def action_sheet_move_create(self):
        samples = self.mapped('expense_line_ids.sample')
        if samples.count(True):
            if samples.count(False):
                raise UserError(_("You can't mix sample expenses and regular ones"))
            self.write({'state': 'post'})
            return

        if any(sheet.state != 'approve' for sheet in self):
            raise UserError(_("You can only generate accounting entry for approved expense(s)."))

        if any(not sheet.journal_id for sheet in self):
            raise UserError(_("Specify expense journal to generate accounting entries."))

        expense_line_ids = self.mapped('expense_line_ids')\
            .filtered(lambda r: not float_is_zero(r.total_amount, precision_rounding=(r.currency_id or self.env.company.currency_id).rounding))
        res = expense_line_ids.with_context(clean_context(self.env.context)).action_move_create()

        paid_expenses_company = self.filtered(lambda m: m.payment_mode == 'company_account' or m.payment_mode == 'advance')
        paid_expenses_company.write({'state': 'done', 'amount_residual': 0.0, 'payment_state': 'paid'})

        paid_expenses_employee = self - paid_expenses_company
        paid_expenses_employee.write({'state': 'post'})

        self.activity_update()
        return res
    
class HrExpense(models.Model):
    _inherit = 'hr.expense'
    
    
    def action_submit_expenses(self):
        for rec in self:
            if rec.payment_mode == "advance" and rec.total_amount > rec.amount_to_recover:
                raise UserError("Le montant restant dans l'avance n'est pas suffisant")
        context_vals = self._get_default_expense_sheet_values()
        if len(context_vals) > 1:
            sheets = self.env['hr.expense.sheet'].create(context_vals)
            return {
                'name': _('New Expense Reports'),
                'type': 'ir.actions.act_window',
                'views': [[False, "list"], [False, "form"]],
                'res_model': 'hr.expense.sheet',
                'domain': [('id', 'in', sheets.ids)],
                'context': self.env.context,
            }
        else:
            context_vals_def = {}
            for key in context_vals[0]:
                context_vals_def['default_' + key] = context_vals[0][key]
            return {
                'name': _('New Expense Report'),
                'type': 'ir.actions.act_window',
                'views': [[False, "form"]],
                'res_model': 'hr.expense.sheet',
                'target': 'current',
                'context': context_vals_def,
            }

   
    payment_mode = fields.Selection(
        selection_add=[('advance', 'Payé par avance')],
    )

    advance_id = fields.Many2one('hr.expense.advance', string="Avance",domain="[('state','=','paid'),('employee_id','=',employee_id)]")
    amount_advanced = fields.Float(compute='_compute_amounts', string='Montant de l\'avance')
    amount_to_recover = fields.Float(compute='_compute_amounts', string='Montant restant')
    
    @api.onchange('total_amount')
    def onchange_total1(self):
        for rec in self:
            if rec.payment_mode == "advance" and rec.total_amount > rec.amount_to_recover:
                raise UserError("Le montant restant dans l'avance n'est pas suffisant")
    @api.onchange('advance_id')
    def onchange_total2(self):
        for rec in self:
            if rec.payment_mode == "advance" and rec.total_amount > rec.amount_to_recover:
                raise UserError("Le montant restant dans l'avance n'est pas suffisant")
                
        

    @api.depends('advance_id.amount','advance_id.remaining_amount')
    def _compute_amounts(self):
        for expense in self:
            total_amount = 0.0
            amount_advanced = 0.0
            expense.amount_advanced = expense.advance_id.amount
            expense.amount_to_recover = expense.advance_id.remaining_amount

#     def _prepare_expense_line_vals(self, move_id, invoice_id, analytic_account_id, analytic_tag_ids, amount):
#         # Préparation des valeurs pour les lignes de note de frais
#         vals = super()._prepare_expense_line_vals(move_id, invoice_id, analytic_account_id, analytic_tag_ids, amount)

#         if self.payment_mode == 'advance':
#             advance = self.advance_id
#             remaining_amount = advance.remaining_amount
#             if remaining_amount < amount:
#                 vals['amount'] = remaining_amount
#                 advance.remaining_amount = 0.0
#             else:
#                 vals['amount'] = amount
#                 advance.remaining_amount -= amount
#         return vals
