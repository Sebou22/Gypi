# -*- coding: utf-8 -*-

from odoo import models, fields, api, _, SUPERUSER_ID
from odoo.tools import float_compare, float_round, float_is_zero, format_datetime


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    custom_tailor_request_id = fields.Many2one(
        'cloth.request.details',
        string="Tailor Request"
    )
    cloth_request_ref = fields.Char(
        string="Reference",
        related='custom_tailor_request_id.name'
    )
    employee_id = fields.Many2one(
        'hr.employee',
        related='custom_tailor_request_id.employee_id'
    )
    deposit = fields.Float(
        related='custom_tailor_request_id.deposit'
    )
    total = fields.Float(
        related='custom_tailor_request_id.total'
    )
    reminder = fields.Float(
        related='custom_tailor_request_id.reminder'
    )
    fabric_color = fields.Char(
        string="Fabric Color",
        related='custom_tailor_request_id.fabric_color'
    )
    quantity = fields.Float(
        string="Quantity",
        related='custom_tailor_request_id.quantity'

    )
    uom_id = fields.Many2one(
        'uom.uom',
        string="Unit of Measure",
        related='custom_tailor_request_id.uom_id'
    )
    user_id = fields.Many2one(
        'res.users',
        string="Responsible",
        related='custom_tailor_request_id.user_id'
    )
    company_id = fields.Many2one(
        'res.company',
        'Company',
        related='custom_tailor_request_id.company_id'
    )
    partner_id = fields.Many2one(
        'res.partner',
        string="Customer",
        related='custom_tailor_request_id.partner_id'
    )
    request_date = fields.Date(
        string="Request Date",
        related='custom_tailor_request_id.request_date'

    )
    deadline_date = fields.Date(
        string="Deadline Date",
        related='custom_tailor_request_id.deadline_date'
    )
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')],
        string="Gender",
        default='male',
        related='custom_tailor_request_id.gender'
    )
    cloth_measurement_details_line_ids = fields.One2many(
        'cloth.measurement.details.line',
        'mrp_production_id',
        readonly=True
    )
    cloth_image_line_ids = fields.One2many(
        'cloth.image.lines',
        'mrp_production_id',
        readonly=True
    )
    internal_note = fields.Text(
        'Add an internal note...',
        related='custom_tailor_request_id.internal_note'

    )
    special_note = fields.Text(
        'Add an special note...',
        related='custom_tailor_request_id.special_note'
    )


class ClothMeasurementDetailsLine(models.Model):
    _inherit = 'cloth.measurement.details.line'

    mrp_production_id = fields.Many2one(
        'mrp.production',
    )


class ClothImagesLines(models.Model):
    _inherit = 'cloth.image.lines'

    mrp_production_id = fields.Many2one(
        'mrp.production'
    )
