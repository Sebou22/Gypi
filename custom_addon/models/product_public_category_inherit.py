from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
class ProductPublicCategoryInherit(models.Model):
    _inherit = "product.public.category"

    restriction_type = fields.Selection(selection=[('neither','Neither'),('all', 'All')],string='Contact Restriction',default='neither',required=True)


    # def write(self, values):
    #     res = super(ProductPublicCategoryInherit, self).write(values)
    #     if 'restriction_type' in values :
    #         users = self.env['res.partner'].search(['|', ('user_ids', '!=', False), ('id', '=', 4)])
    #         if (self.restriction_type == 'neither'):
    #             users.write({'category_ids': [(3, self.id)]})
    #         elif (self.restriction_type == 'all'):
    #             users.write({'category_ids': [(4, self.id)]})
    #     return res

    def write(self, values):
        res = super(ProductPublicCategoryInherit, self).write(values)
        if 'restriction_type' in values:
            self.clear_caches()
        return res



