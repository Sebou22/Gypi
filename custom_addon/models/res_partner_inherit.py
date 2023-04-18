from odoo import models, fields, api, _


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    @api.depends('parent_id.website_logo')
    def _default_logo(self):
        for rec in self:
            if(rec.company_type == 'person' and rec.parent_id):
                rec.website_logo = rec.parent_id.website_logo

    website_logo = fields.Binary('User Logo', compute=_default_logo,store=True)
    category_ids = fields.Many2many('product.public.category', string='Category')
    product_ids = fields.Many2many('product.template', string='Products')

    def write(self, values):
        res = super(ResPartnerInherit, self).write(values)
        if 'category_ids' in values or 'product_ids' in values:
            self.clear_caches()
        return res

    def get_restriction_categ(self):
        categories = self.env['product.public.category'].search([('restriction_type','=','all')])
        list_ids =[]
        partner_id = self.env.user.partner_id
        for cat in categories:
            if cat.id not in partner_id.category_ids.ids:
                list_ids.append(cat.id)
        return list_ids

