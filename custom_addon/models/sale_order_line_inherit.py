from odoo import models, fields, api, _


class SaleOrderLineInherit(models.Model):
    _inherit = "sale.order.line"
    comment_customer = fields.Text("Comment customer")

    def _prepare_invoice_line(self, **optional_values):

        values = super(SaleOrderLineInherit, self)._prepare_invoice_line(**optional_values)
        values['comment_customer'] = self.comment_customer

        return values