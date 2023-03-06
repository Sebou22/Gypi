# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ProductList(models.Model):
    _name = 'product.list'
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity_done = fields.Float('Quantity Done',digits='Product Unit of Measure',)
    product_uom_qty = fields.Float('Demand',digits='Product Unit of Measure',default=0.0)
    reserved_availability = fields.Float('Quantity Reserved',digits='Product Unit of Measure',)
    preparation_id = fields.Many2one('preparation.order', 'Preparation', index=True, check_company=True)

