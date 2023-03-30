from odoo import models, fields, api, _

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"
    comment_customer = fields.Text("Order N°")


class StockMoveInherit(models.Model):
    _inherit = "stock.move"
    comment_customer = fields.Text("Order N°")


