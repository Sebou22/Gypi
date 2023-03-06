# -*- coding: utf-8 -*-
from odoo import models, fields,_


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    def action_open_picking_form(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'view_mode': 'form',
            'view_id': self.env.ref('stock.view_picking_form').id,
            'res_id': self.id,
        }

    def create_preparation_order(self):

        res = self.env['preparation.order'].create({'stock_picking_ids':[(6, 0, self.ids)]})
        return {
            'type': 'ir.actions.act_window',
            'res_id': res.id,
            'res_model': 'preparation.order',
            'views': [(self.env.ref('gypi_picking_order.view_preparation_order_form').id, 'form')],
        }
