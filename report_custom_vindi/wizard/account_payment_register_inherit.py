from odoo import models, fields, api, _
from odoo import _, models


class AccountPaymentRegisterAydooInherit(models.TransientModel):
    _inherit = "account.payment.register"

    due_date = fields.Date(string="Due Date", required=True,
                           default=fields.Date.context_today)
    reference = fields.Char(string="Reference")
    bank_id = fields.Many2one("bank.bank", string="Bank")
    payment_mode_id = fields.Many2one("payment.mode", string="Payment Mode", required=True,
                                                      domain = "[('is_cash','=',False)]")
    journal_type = fields.Char(string="Journal type", compute='_get_default_journal_type')
    agency = fields.Char('Agency')
    swift_code = fields.Char("Swift Code")

    @api.depends('journal_id')
    def _get_default_journal_type(self):
        
        self.ensure_one()
        for wizard in self:
            wizard.journal_type = wizard.journal_id.type
            
    @api.onchange('journal_type')
    def _onchange_journal_type(self):
        
        if self.journal_type =='cash':
            self.payment_mode_id = self.env['payment.mode'].search([('is_cash', '=',True)], limit=1)

    def _create_payment_vals_from_wizard(self, batch_result):
        payment_vals = super()._create_payment_vals_from_wizard(batch_result)
        payment_vals['due_date'] = self.due_date
        payment_vals['reference'] = self.reference
        payment_vals['bank_id'] = self.bank_id.id
        payment_vals['payment_mode_id'] = self.payment_mode_id.id
        payment_vals['agency'] = self.agency
        payment_vals['swift_code'] = self.swift_code

        return payment_vals
