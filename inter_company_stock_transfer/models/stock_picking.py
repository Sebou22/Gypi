# -*- encoding: utf-8 -*-

from odoo import models, fields


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    intercompany_transfer = fields.Boolean('Intercompany Transfer')
