from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
class ProductPublicCategoryInherit(models.Model):
    _inherit = "product.public.category"

    restriction_type = fields.Selection(selection=[('neither','Neither'),('all', 'All')],string='Contact Restriction',default='neither',required=True)

    def write(self, values):
        res = super(ProductPublicCategoryInherit, self).write(values)
        if 'restriction_type' in values:
            self.clear_caches()
        return res



