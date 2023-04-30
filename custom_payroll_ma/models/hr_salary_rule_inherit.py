# -*- coding:utf-8 -*-
from odoo import api, fields, models, tools, _
from odoo.tools.safe_eval import safe_eval
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class HrSalaryRuleInheritAydoo(models.Model):
    _inherit = 'hr.salary.rule'


    def _compute_rule_ma(self, localdict,salary_base):

        """
        :param localdict: dictionary containing the current computation environment
        :return: returns a tuple (amount, qty, rate)
        :rtype: (float, float, float)
        """
        self.ensure_one()
        amount_python_compute = self.amount_python_compute
        if(self.code=='BASIC'):
            amount_python_compute = salary_base
        if self.amount_select == 'fix':
            try:
                return self.amount_fix or 0.0, float(safe_eval(self.quantity, localdict)), 100.0
            except Exception as e:
                self._raise_error(localdict, _("Wrong quantity defined for:"), e)
        if self.amount_select == 'percentage':
            try:
                return (float(safe_eval(self.amount_percentage_base, localdict)),
                        float(safe_eval(self.quantity, localdict)),
                        self.amount_percentage or 0.0)
            except Exception as e:
                self._raise_error(localdict, _("Wrong percentage base or quantity defined for:"), e)
        else:  # python code
            try:
                safe_eval(amount_python_compute or 0.0, localdict, mode='exec', nocopy=True)
                return float(localdict['result']), localdict.get('result_qty', 1.0), localdict.get('result_rate', 100.0)
            except Exception as e:
                self._raise_error(localdict, _("Wrong python code defined for:"), e)