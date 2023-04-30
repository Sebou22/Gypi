from odoo import api, fields, models, _
from datetime import date, datetime
from dateutil.relativedelta import relativedelta


class BordereauPayment(models.TransientModel):

    _name = "bordereau.payment"
    _description = "Bordereau Paiment"

    date_start = fields.Date(string='Date From', required=True,
        default=lambda self: fields.Date.to_string(date.today().replace(day=1)))
    date_end = fields.Date(string='Date To', required=True,
        states={'draft': [('readonly', False)]},
        default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    slip_ids = fields.Many2many('hr.payslip', string='Payslips', readonly=True)
    company_id = fields.Many2one(
        'res.company', string='Company', copy=False, required=True,readonly=False,
        default=lambda self: self.env.company)
    taux_prestation_AF = fields.Float(string='AF %', compute='get_taux', default=0)
    taux_prestation_sociales = fields.Float(string='prestations sociales', compute='get_taux', default=0)
    taux_tfp = fields.Float(string='% TFP', compute='get_taux', default=0)
    taux_participation_amo = fields.Float(string='% part. AMO', compute='get_taux', default=0)
    taux_cot_amo = fields.Float(string='% cot. AMO', compute='get_taux', default=0)
    currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
    date_payment = fields.Date(string="Date Payment",default=lambda self: fields.Date.to_string((datetime.now() + relativedelta(months=+1, day=10)).date()))

    def get_taux(self):
        for rec in self:
            rec.taux_prestation_AF = 6.40
            rec.taux_prestation_sociales = 13.46
            rec.taux_tfp = 1.60
            rec.taux_participation_amo = 1.85
            rec.taux_cot_amo = 4.52


    @api.onchange('date_start')
    def _compute_date_end(self):
        next_month = relativedelta(months=+1, day=1, days=-1)
        payment_month = relativedelta(months=+1, day=10)
        self.date_end = self.date_start + next_month
        self.date_payment = self.date_start + payment_month

    def action_print_bordereau_payment(self):
        payslip_ids = self.env['hr.payslip'].search(
            [('date_from', '>=', self.date_start), ('date_from', '<=', self.date_end),('company_id', '=', self.company_id.id)])
        if (payslip_ids):
            self.slip_ids = [(6, 0, payslip_ids.ids)]
        return self.env.ref('custom_payroll_ma.bordereau_paiement_cnss_id').report_action(self)

