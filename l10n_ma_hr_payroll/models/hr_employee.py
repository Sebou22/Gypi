from odoo import models, fields

class HrEmployee(models.AbstractModel):
    _inherit = 'hr.employee.base'

    cin = fields.Char(string="Numéro CIN", required=False)
    matricule_cnss = fields.Char(string="Numéro CNSS", required=False)
    matricule_cimr = fields.Char(string="Numéro CIMR", required=False)
    matricule_mut = fields.Char(string="Numéro MUTUELLE", required=False)