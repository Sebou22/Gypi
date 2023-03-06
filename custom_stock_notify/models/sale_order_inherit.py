from odoo import models, fields, api, _

class SaleOrderInherit(models.Model):
    _inherit = "sale.order"

    def _get_stock_warning(self, clear=True):
        self.ensure_one()
        warn = self.warning_stock
        if clear:
            self.warning_stock = ''
        return warn
