from odoo import api, fields, models, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class BordereauCnss(models.TransientModel):

    _name = "bordereau.cnss"
    _description = "Bordereau CNSS"

    date_start = fields.Date(string='Date From', required=True,
        default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_end = fields.Date(string='Date To', required=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    slip_ids = fields.Many2many('hr.payslip', string='Payslips', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', copy=False, required=True,readonly=False,
        default=lambda self: self.env.company)


    @api.onchange('date_start')
    def _compute_date_end(self):
        next_month = relativedelta(months=+1, day=1, days=-1)
        self.date_end = self.date_start + next_month

    def action_print_bordereau_cnss(self):
        for rec in self:
            payslip_ids = self.env['hr.payslip'].search([('date_from','>=',rec.date_start),('date_from','<=',rec.date_end),('company_id', '=', self.company_id.id)])
            if(payslip_ids):
                rec.slip_ids = [(6,0,payslip_ids.ids)]
        return self.env.ref('custom_payroll_ma.etat_cnss_id').report_action(self)


