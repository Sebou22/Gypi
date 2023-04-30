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