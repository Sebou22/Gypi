# -*- coding: utf-8 -*-
from odoo import models, fields, _


class ProductList(models.Model):
    _name = 'product.list'
    product_id = fields.Many2one('product.product', 'Product', required=True)
    quantity_done = fields.Float('Quantity Done',digits='Product Unit of Measure',)
    product_uom_qty = fields.Float('Demand',digits='Product Unit of Measure',default=0.0)
    reserved_availability = fields.Float('Quantity Reserved',digits='Product Unit of Measure',)
    preparation_id = fields.Many2one('preparation.order', 'Preparation', index=True, check_company=True)
    location_barcode = fields.Char("Locations",compute="_get_location_barcode")


    def _get_location_barcode(self):
        for record in self:
            stock = self.env["stock.quant"].search([('product_id','=',record.product_id.id),('quantity','>',0)])
            if(stock):
                location_ids = stock.mapped('location_id').filtered(lambda r : r.barcode)
                record.location_barcode = ','.join(l.barcode  for l in location_ids)
