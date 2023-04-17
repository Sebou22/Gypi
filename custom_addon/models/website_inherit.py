from odoo import models, fields, api, _


class WebsiteInherit(models.Model):
    _inherit = 'website'


    def sale_product_domain(self):
        categories = self.env['product.public.category'].search([('restriction_type','=','all')])
        list_ids =[]
        partner_id = self.env.user.partner_id
        for cat in categories:
            if cat.id not in partner_id.category_ids.ids:
                list_ids.append(cat.id)

        return ['&'] + super(WebsiteInherit, self).sale_product_domain() + [
            ('id', 'not in', self.env.user.partner_id.product_ids.ids),
            ('public_categ_ids', 'not in', list_ids)]
