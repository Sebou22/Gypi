from odoo import fields, models, api


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    reference_customer = fields.Text(
        string="Reference customer",
        compute='_compute_reference_customer',
        store=True, readonly=False, required=True, precompute=True)


    @api.depends('product_id')
    def _compute_reference_customer(self):
        for line in self:
            line.reference_customer = line.product_id.reference_customer