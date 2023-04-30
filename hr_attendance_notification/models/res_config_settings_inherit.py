# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    hours_work = fields.Float("Hour Work")
    marge_retard = fields.Float("Marge Retard")

class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    hours_work = fields.Float(related='company_id.hours_work',readonly=False)
    marge_retard = fields.Float(related='company_id.marge_retard',readonly=False)

