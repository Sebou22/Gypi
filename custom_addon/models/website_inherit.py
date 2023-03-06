from odoo import models, fields, api, _


class WebsiteInherit(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        return ['&'] + super(WebsiteInherit, self).sale_product_domain() + [
            ('id', 'not in', self.env.user.product_ids.ids),
            ('public_categ_ids', 'not in', self.env.user.category_ids.ids)]
