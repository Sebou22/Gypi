from odoo import fields, models, api


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    collection_id = fields.Many2one('product.collection',string="Collection")
    supplier_id = fields.Many2one('res.partner',string="Supplier")
    season_id = fields.Many2one('product.season',string="Season")
    style_id = fields.Many2one("product.style", string="Style name")
    product_line = fields.Many2one('product.line_ca', string="Product line")
    article_group = fields.Many2one('article.group', string="Article group")
    product_group = fields.Many2one('product.group', string="Product group")
    supplier_fabric = fields.Char('Supplier Fabric')
    reference_customer = fields.Char('Reference customer', compute='_compute_reference_customer',inverse='_set_reference_customer', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.reference_customer')
    def _compute_reference_customer(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.reference_customer = template.product_variant_ids.reference_customer
        for template in (self - unique_variants):
            template.reference_customer = False

    def _set_reference_customer(self):
        for template in self:
            if len(template.product_variant_ids) == 1:
                template.product_variant_ids.reference_customer = template.reference_customer