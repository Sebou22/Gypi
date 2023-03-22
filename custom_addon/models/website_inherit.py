from odoo import models, fields, api, _


class WebsiteInherit(models.Model):
    _inherit = 'website'

    def sale_product_domain(self):
        return ['&'] + super(WebsiteInherit, self).sale_product_domain() + [
            ('restrict_ok', '=', True)]
