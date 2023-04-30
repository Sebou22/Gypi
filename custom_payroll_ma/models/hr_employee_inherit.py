# -*- coding:utf-8 -*-

from odoo import api, fields, models,exceptions, _


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'
    loans_ids = fields.One2many('hr.loans.line','employee_id')