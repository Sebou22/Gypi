# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class PaymentModeAydoo(models.Model):
    _name = 'payment.mode'
    _description = 'Payment Mode'

    code = fields.Char(string="code")
    name = fields.Char(string="Name",translate=True)
    is_cash = fields.Boolean("Is cash")
