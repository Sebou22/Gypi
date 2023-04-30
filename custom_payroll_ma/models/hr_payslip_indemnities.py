# Copyright 2021 Ayouris
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)

class HrPayslipIndemnities(models.Model):
    _name = "hr.payslip.indemnities"
    _description = "indemnité"



    # @api.onchange('name','total')
    # def _check_total2(self):
    #     if(self.name):
    #         names= [r.name.name for r in self.contract_id.indemnities_ids if r.name.id == self.name.id]
    #         if(len(names)>2):
    #             raise ValidationError(_("%s existe déja !" %(self.name.name)))
    #         if(self.total> self.name.max_total):
    #             raise ValidationError(_("%s ! Vous avez dépassé le maximum %s de %s" %(self.total,self.name.max_total,self.name.name)))

    name = fields.Char("Nom")
    max_total = fields.Float("Max total")
    contract_id = fields.Many2one('hr.contract')
    note = fields.Text("Note")
    code = fields.Char("Code")

    amount_select = fields.Selection([
        ('fix', 'Fixed Amount'),
        ('code', 'Python Code'),
    ], string='Amount Type', index=True, required=True, default='fix', help="The computation method for the rule amount.")
    amount_fix = fields.Float(string='Fixed Amount', digits='Payroll')
    amount_percentage = fields.Float(string='Percentage (%)', digits='Payroll Rate',
        help='For example, enter 50.0 to apply a percentage of 50%')
    amount_python_compute = fields.Text(string='Python Code',
        default='''
                    # Available variables:
                    #----------------------
                    # rules: object containing the rules code (previously computed)

                    # Note: returned value have to be set in the variable 'result'

                    result = contract_id.wage * 0.10''')
    amount_percentage_base = fields.Char(string='Percentage based on', help='result will be affected to a variable')
    quantity = fields.Char(default='1.0',
        help="It is used in computation for percentage and fixed amount. "
             "E.g. a rule for Meal Voucher having fixed amount of "
             u"1€ per worked day can have its quantity defined in expression "
             "like worked_days.WORK100.number_of_days.")

    def _raise_error(self, localdict, error_type, e):
        raise UserError(_("""%s:
    - Indeminité: %s (%s)
    - Error: %s""") % (
            error_type,
            self.name,
            self.code,
            e))


    def _compute_rule(self, localdict):

        """
        :param localdict: dictionary containing the current computation environment
        :return: returns a tuple (amount, qty, rate)
        :rtype: (float, float, float)
        """
        self.ensure_one()
        if self.amount_select == 'fix':
            try:
                return self.amount_fix or 0.0, float(safe_eval(self.quantity, localdict)), 100.0
            except Exception as e:
                self._raise_error(localdict, _("Wrong quantity defined for:"), e)
        else:  # python code
            try:
                safe_eval(self.amount_python_compute or 0.0, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), localdict.get('result_qty', 1.0), localdict.get('result_rate', 100.0)
            except Exception as e:
                self._raise_error(localdict, _("Wrong python code defined for:"), e)

class HrPayslipIndemnitiesLignes(models.Model):
    _name = "hr.payslip.indemnities.lignes"
    _description = "indemnité"



    # @api.onchange('name','total')
    # def _check_total2(self):
    #     if(self.name):
    #         names= [r.name.name for r in self.contract_id.indemnities_ids if r.name.id == self.name.id]
    #         if(len(names)>2):
    #             raise ValidationError(_("%s existe déja !" %(self.name.name)))
    #         if(self.total> self.name.max_total):
    #             raise ValidationError(_("%s ! Vous avez dépassé le maximum %s de %s" %(self.total,self.name.max_total,self.name.name)))
    @api.depends('name')
    def default_max_total(self):
        for rec in self:
            localdict = {
                'result': None,
                'result_qty': 1.0,
                'result_rate': 100,
                'result_name': False,
                'contract_id': rec.contract_id,
            }
            amount, qty, rate = rec.name._compute_rule(localdict)
            rec.max_total = amount

    def _compute_diff_total(self):
        for rec in self:
            if(rec.total>rec.max_total):
                rec.diff_total = rec.total- rec.max_total
            else:
                rec.diff_total=0.0

    def _compute_total_ex(self):
        for rec in self:
            if(rec.total<=rec.max_total):
                rec.exo_total = rec.total
            else:
                rec.exo_total=rec.max_total





    name = fields.Many2one("hr.payslip.indemnities")
    max_total = fields.Float(store=True)
    total = fields.Float("total")
    diff_total = fields.Float("Total Taxable",compute="_compute_diff_total")
    exo_total = fields.Float("Total Exonéré",compute="_compute_total_ex")
    contract_id = fields.Many2one('hr.contract')
    note = fields.Text("Note")
    code = fields.Char(related="name.code",string="Code")






