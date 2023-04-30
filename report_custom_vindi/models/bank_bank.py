# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class BankAydoo(models.Model):
    _name = 'bank.bank'
    _description = 'Bank'

    code = fields.Char(string="code")
    name = fields.Char(string="Name")
