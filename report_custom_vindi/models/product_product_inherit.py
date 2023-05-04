from odoo import fields, models, api


class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    reference_customer = fields.Char('Reference customer')