from odoo import models, fields, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"
    comment_customer = fields.Text("Comment customer")