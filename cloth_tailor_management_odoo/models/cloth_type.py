# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ClothType(models.Model):
    _name = 'cloth.type'
    _description = 'Cloth Type'

    name = fields.Char(
        string="Name",
        required=True
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        string="Gender",
        default='male'
    )
    measurement_ids = fields.One2many(
        'cloth.measurement.type',
        'cloth_type_id',
        string="Measurement Types"
    )


class ClothImages(models.Model):
    _name = 'cloth.image'
    _description = 'Cloth Image'

    name = fields.Char(
        string="Name",
        required=True
    )

    image = fields.Binary("Image", help="Select image here")

    note = fields.Text(
        'Add an special note...', )


class ClothImagesLines(models.Model):
    _name = 'cloth.image.lines'
    _description = 'Cloth Image'

    cloth_image_id = fields.Many2one(
        'cloth.image',
        string="Cloth Image"
    )
    image = fields.Binary(related='cloth_image_id.image', string="Image", help="Select image here", store=True, )

    note = fields.Text(related='cloth_image_id.note', string="Image", store=True)
    cloth_request_id = fields.Many2one('cloth.request.details')
