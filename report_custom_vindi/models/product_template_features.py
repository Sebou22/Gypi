from odoo import fields, models, api

class ProductTemplateCollection(models.Model):
    _name = 'product.collection'

    name = fields.Char("Collection",required=True)

class ProductTemplateSeason(models.Model):
    _name = 'product.season'

    name = fields.Char("Season",required=True)

class ProductTemplateStyle(models.Model):
    _name = 'product.style'

    name = fields.Char("Style",required=True)

class ProductTemplateLinaCa(models.Model):
    _name = 'product.line_ca'

    name = fields.Char("Product line",required=True)

class ProductTemplateArticleGroup(models.Model):
    _name = 'article.group'

    name = fields.Char("Article group",required=True)

class ProductTemplateProductGroup(models.Model):
    _name = 'product.group'

    name = fields.Char("Product group",required=True)