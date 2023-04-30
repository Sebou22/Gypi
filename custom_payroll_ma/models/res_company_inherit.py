# -*- coding:utf-8 -*-

from odoo import api, fields, models,exceptions, _


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'
    agence = fields.Char('Agence')
    n_affilie = fields.Char("N° Affilié")
    reference_structure = fields.Char('Référence structure')