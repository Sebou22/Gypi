# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _


class StockMoveInherit(models.Model):
    _inherit = "stock.move"

    reference_customer = fields.Text(
        string="Reference customer",
        compute='_compute_reference_customer',
        store=True, readonly=False,)


    @api.depends('product_id')
    def _compute_reference_customer(self):
        for move in self:
            move.reference_customer = move.sale_line_id.reference_customer