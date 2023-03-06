from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    comment_customer = fields.Text("Order N°")