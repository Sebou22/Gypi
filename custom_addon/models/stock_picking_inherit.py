from odoo import models, fields, api, _

class StockPickingInherit(models.Model):
    _inherit = "stock.picking"
    comment_customer = fields.Text("Order N°",related="sale_id.comment_customer")


class StockMoveInherit(models.Model):
    _inherit = "stock.move"
    comment_customer = fields.Text("Order N°",related="sale_line_id.comment_customer")


