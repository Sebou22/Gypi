from odoo import models, fields, api, _


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    category_ids = fields.Many2many('product.public.category', string='Products')
    product_ids = fields.Many2many('product.template', string='Products')

    def write(self, values):
        res = super(ResUsersInherit, self).write(values)
        if 'category_ids' in values or 'product_ids' in values:
            self.clear_caches()
        return res
