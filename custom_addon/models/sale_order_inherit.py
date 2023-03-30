from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = "sale.order"
    comment_customer = fields.Text("Order N°")

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrderInherit, self)._prepare_invoice()
        invoice_vals['comment_customer'] = self.comment_customer
        return invoice_vals