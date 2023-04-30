# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class AccountPaymentInherit(models.Model):
    _inherit = "account.payment"

    due_date = fields.Date(string="Due Date ", default=fields.Date.context_today, required=True)
    reference = fields.Char(string="Reference ")
    payment_mode_id = fields.Many2one("payment.mode", string="Payment Mode", required=True)
    bank_id = fields.Many2one("bank.bank", string="Bank")
    journal_type = fields.Char(string="Journal type", compute='_get_default_journal_type')
    agency = fields.Char('Agency')
    swift_code = fields.Char("Swift Code")

    @api.depends('journal_id')
    def _get_default_journal_type(self):
        self.ensure_one()
        for wizard in self:
            wizard.journal_type = wizard.journal_id.type

