from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
class ProductPublicCategoryInherit(models.Model):
    _inherit = "product.public.category"

    restriction_type = fields.Selection(selection=[('neither','Neither'),('all', 'All'),('section', 'Section')],string='Contact Restriction',default='neither',required=True)
    restriction_contacts = fields.Many2many('res.users', string='Contact')

    def write(self, values):
        res = super(ProductPublicCategoryInherit, self).write(values)
        if 'restriction_type' in values or 'restriction_contact' in values:
            if (self.restriction_type == "neither"):
                self.restriction_contacts = False
            self.clear_caches()
        return res

