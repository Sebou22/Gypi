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

