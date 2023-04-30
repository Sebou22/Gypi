from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)
class HrContractInherit(models.Model):
    _inherit = 'hr.contract'

    wage_net = fields.Monetary('Salaire Net', help="Salaire mensuel NET du salarié .")
    indemnities_ids = fields.One2many('hr.payslip.indemnities.lignes', 'contract_id')
    reasons_leaving = fields.Char("Justification du départ")


    def _get_line_salary(self, wage_compute, slip):
        salary_global = "result=%s" % (wage_compute)
        slip.compute_sheet2()
        net = slip.line_ids.filtered(lambda r: r.code == 'NET').total
        # net=round(net,2)
        brut = slip.line_ids.filtered(lambda r: r.code == 'BRUT').total
        # brut = round(brut, 2)
        amo = slip.line_ids.filtered(lambda r: r.code == 'AMOE').total
        # amo = round(amo, 2)
        cnss = slip.line_ids.filtered(lambda r: r.code == 'CNSS').total
        # cnss = round(cnss, 2)
        base = slip.line_ids.filtered(lambda r: r.code == 'BASIC').total
        date1 = slip.date_from
        date2 = slip.date_to
        nbre_jour = sum(slip.worked_days_line_ids.mapped('number_of_days')) if slip.worked_days_line_ids else 0
        #            raise ValidationError(_(wage_compute+(net.total)))
        return net, brut, amo, cnss, date1, date2, nbre_jour, base

    def get_wage_net_brut(self):
        struc = self.structure_type_id.default_struct_id
        contract = self.copy()
        slip = self.env['hr.payslip'].create({'name':'contract_1','employee_id': self.employee_id.id, 'contract_id': contract.id, 'struct_id': struc.id})
        salary = self.wage_net
        currency_id = slip.currency_id
        lines= False
        wage_compute = salary * 1.5
        flag = False
        j = 1
        flaa=False
        for i in range(1000):
            contract.wage= wage_compute
            net, brut, amo, cnss, date1, date2, nbre_jour, base = self._get_line_salary(wage_compute, slip)
            _logger.info("le net %s | %s | %s iteration %s avec wage compute %s" %(net,brut,base,i,wage_compute))
            if (net == salary):
                contract.wage = int(wage_compute)
                net2, brut2, amo2, cnss2, date12, date22, nbre_jour2, base2 = self._get_line_salary(int(wage_compute), slip)
                if(net2==salary):
                    _logger.info("ouuuiiiiii %s base %s" %(int(wage_compute),base2))
                    lines = slip.line_ids
                    net, brut, amo, cnss, date1, date2, nbre_jour, base = net2, brut2, amo2, cnss2, date12, date22, nbre_jour2, base2
                    # net=net2
                    # brut = brut2
                    # amo = amo2
                    # cnss = cnss2
                    # date1 = date12
                    # date2 = date22
                    # nbre_jour = nbre_jour2
                    # base = base2

                break
            min = (salary - net) / 2
            wage_compute += min
            j += 1
        if not lines:
            lines = slip.line_ids
        l = "<ul>"
        for i in lines:
            l += "<li>" + str(i.name) + " :   " + str(i.total) + " </li>"
        l += "</ul>"
        # raise ValidationError(_(slip.line_ids.mapped('name')))
        self.env.cr.rollback()
        details = '<a class="btn btn-primary" data-bs-toggle="collapse" href="#collapseExample" role="button" aria-expanded="false" aria-controls="collapseExample" style="margin-top:5px;"> Voir Détails </a><br/>'
        details += '<div class="collapse show" id="collapseExample"><div class="card card-body" style="height:200px;overflow-y: auto;"> %s </div></div>' % (l)

        message = "<ul><li>BASE : %s</li><li> BRUT : %s </li><li> NET :%s</li> <li> AMO : %s</li> <li> CNSS : %s</li>  <li> Pendant la période : %s - %s</li> %s </ul>" % (base, brut, net, amo, cnss, date1, date2, details)
        return {
            'name': 'Résultat',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'custom.pop.message',
            'target': 'new',
            'context': {'default_name': message}
        }




