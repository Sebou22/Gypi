# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    payment_restricted_ids = fields.Many2many(
        'payment.provider',
        'customer_payment_id',
        'partner_id',
        'payment_id',
        'Payment restriction')