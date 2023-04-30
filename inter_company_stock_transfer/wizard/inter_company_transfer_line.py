# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InterCompanyTransferLine(models.TransientModel):
    _name = 'inter.company.transfer.line'

    name = fields.Char('Description', index=True)
    stock_transfer_id = fields.Many2one('inter.company.transfer')
    product_id = fields.Many2one('product.product')
    product_uom = fields.Many2one('uom.uom')
    product_uom_qty = fields.Float('Initial Demand')
    available_qty = fields.Char("Available Quantity")

    @api.onchange('product_id')
    def onchange_product_id(self):
        product = self.product_id.with_context(lang=self.env.user.lang)
        self.product_uom = product.uom_id.id
        self.name = product.partner_ref or ''
        return {
            'domain': {
                'product_uom': [
                    ('category_id', '=', product.uom_id.category_id.id)
                ]
            }
        }
