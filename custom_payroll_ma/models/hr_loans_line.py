# -*- coding:utf-8 -*-

from odoo import api, fields, models, _

class HrPayslipLoansLine(models.Model):
    _name = 'hr.loans.line'
    _description = 'Ligne Avance/Prêt'
    date = fields.Date("Date")
    amount = fields.Float("Montant")
    employee_id = fields.Many2one("hr.employee")