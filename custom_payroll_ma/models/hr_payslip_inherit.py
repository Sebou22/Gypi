# -*- coding:utf-8 -*-
from odoo import api, fields, models, tools, _, Command
from odoo.exceptions import UserError, ValidationError

# class HrPayslipRunInherit(models.Model):
#     _inherit = 'hr.payslip.run'
#     taux_prestation_AF = fields.Float(string='AF %', compute='get_taux', default=0)
#     taux_prestation_sociales = fields.Float(string='prestations sociales', compute='get_taux', default=0)
#     taux_tfp = fields.Float(string='% TFP', compute='get_taux', default=0)
#     taux_participation_amo = fields.Float(string='% part. AMO', compute='get_taux', default=0)
#     taux_cot_amo = fields.Float(string='% cot. AMO', compute='get_taux', default=0)
#     currency_id = fields.Many2one(string="Currency", related='company_id.currency_id', readonly=True)
#
#     def get_taux(self):
#         for rec in self:
#             rec.taux_prestation_AF = 6.40
#             rec.taux_prestation_sociales = 13.46
#             rec.taux_tfp = 1.60
#             rec.taux_participation_amo = 1.85
#             rec.taux_cot_amo = 4.52




class HrPayslipInherit(models.Model):
    _inherit = 'hr.payslip'

    def get_avs(self):
        return 1

    @api.depends('employee_id','employee_id.loans_ids', 'contract_id', 'struct_id', 'date_from', 'date_to', 'struct_id')
    def _compute_input_line_ids(self):
        for slip in self:
            if(slip.employee_id.loans_ids):
                loans = slip.employee_id.loans_ids.filtered(lambda r : r.date >= slip.date_from and r.date<= slip.date_to)
                if(loans):
                    total = sum(loans.mapped("amount"))
                    slip.input_line_ids.unlink()
                    slip.update({'input_line_ids':[(0, 0, {'input_type_id':self.env.ref("l10n_ma_hr_payroll.AVS").id ,'amount':total})]})


    # def compute_sheet2(self,salary_global):
    #
    #     for payslip in self:
    #         #number = payslip.number or self.env['ir.sequence'].next_by_code('salary.slip')
    #         # delete old payslip lines
    #         payslip.line_ids.unlink()
    #         # set the list of contract for which the rules have to be applied
    #         # if we don't give the contract, then the rules to apply should be for all current contracts of the employee
    #         contract_ids = payslip.contract_id.ids or \
    #                        self.get_contract(payslip.employee_id, payslip.date_from, payslip.date_to)
    #         lines = [(0, 0, line) for line in self._get_payslip_lines()]
    #         payslip.write({'line_ids': lines})
    #     return True



    def compute_sheet2(self):
        # delete old payslip lines

        # this guarantees consistent results
        self.env.flush_all()
        today = fields.Date.today()
        for payslip in self:
            payslip.line_ids.unlink()
            payslip.write({
                'compute_date': today
            })
        self.env['hr.payslip.line'].create(self._get_payslip_lines())
        return True



