# -*- coding: utf-8 -*-
from odoo import models, fields, _


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'
    preparation_id = fields.Many2one('preparation.order', 'Transfer', index=True, check_company=True)
