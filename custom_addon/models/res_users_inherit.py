from odoo import models, fields, api, _


class ResUsersInherit(models.Model):
    _inherit = "res.users"

    category_ids = fields.Many2many('product.public.category', string='Products')
    product_ids = fields.Many2many('product.template', string='Products')

    # def write(self, values):
    #     res = super(ResUsersInherit, self).write(values)
    #     if 'category_ids' in values or 'product_ids' in values:
    #         self.clear_caches()
    #     return res

    # @api.model_create_multi
    # def create(self, vals_list):
    #     users = super(ResUsersInherit, self).create(vals_list)
    #     for user in users:
    #         category_ids = self.env['product.public.category'].search([('restriction_type','=','all')])
    #         user.partner_id.category_ids = [(6, 0, category_ids.ids)]
    #     return users
