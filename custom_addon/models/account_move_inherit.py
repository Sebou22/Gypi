from odoo import models, fields, api, _

class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    comment_customer = fields.Text("Order N°")



class AccountMoveLineInherit(models.Model):
    _inherit = "account.move.line"

    comment_customer = fields.Text(string="Comment customer")