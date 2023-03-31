from odoo import models, fields, api, _


class WebsiteInherit(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        return ['&'] + super(WebsiteInherit, self).sale_product_domain() + [
            ('id', 'not in', self.env.user.partner_id.product_ids.ids),
            ('public_categ_ids', 'not in', self.env.user.partner_id.category_ids.ids)]
