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

class ProductPublicCategoryInherit(models.Model):
    _inherit = "product.public.category"

    restriction_type = fields.Selection(selection=[('neither','Neither'),('all', 'All'),('section', 'Section')],string='Contact Restriction',default='neither',required=True)
    restriction_contact = fields.Many2many('res.users', string='Contact')

    def write(self, values):
        res = super(ProductPublicCategoryInherit, self).write(values)
        if 'restriction_type' in values or 'restriction_contact' in values:
            self.clear_caches()
        return res

