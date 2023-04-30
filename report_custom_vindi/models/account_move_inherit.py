# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.tools import formatLang


class AccountMoveInherit(models.Model):
    _inherit = "account.move"

    net_weight = fields.Float("Brut Weight", compute="_compute_weight")
    brut_weight = fields.Float("Brut Weight", compute="_compute_weight")
    package_count = fields.Integer("Number of boxes", compute="_compute_weight")
    weight_uom_name = fields.Char(string='Weight unit of measure label', compute='_compute_weight_uom_name')
    qty_count = fields.Float(compute="_compute_qty")

    def _compute_weight_uom_name(self):
        weight_uom_id = self.env['product.template']._get_weight_uom_id_from_ir_config_parameter()
        for move in self:
            move.weight_uom_name = weight_uom_id.name

    def _compute_qty(self):
        for move in self:
            move.qty_count = sum(move.invoice_line_ids.mapped('quantity'))



    def _compute_weight(self):
        for move in self:
            move.net_weight = sum(move.invoice_line_ids.sale_line_ids.order_id.picking_ids.mapped('weight'))
            move.brut_weight = sum(move.invoice_line_ids.sale_line_ids.order_id.picking_ids.mapped('shipping_weight'))
            move.package_count = len(move.invoice_line_ids.sale_line_ids.order_id.picking_ids.package_ids)


    @api.depends('move_type', 'line_ids.amount_residual')
    def _compute_payments_widget_reconciled_info(self):
        for move in self:
            payments_widget_vals = {'title': _('Less Payment'), 'outstanding': False, 'content': []}

            if move.state == 'posted' and move.is_invoice(include_receipts=True):
                reconciled_vals = []
                reconciled_partials = move._get_all_reconciled_invoice_partials()
                for reconciled_partial in reconciled_partials:
                    counterpart_line = reconciled_partial['aml']
                    if counterpart_line.move_id.ref:
                        reconciliation_ref = '%s (%s)' % (counterpart_line.move_id.name, counterpart_line.move_id.ref)
                    else:
                        reconciliation_ref = counterpart_line.move_id.name
                    if counterpart_line.amount_currency and counterpart_line.currency_id != counterpart_line.company_id.currency_id:
                        foreign_currency = counterpart_line.currency_id
                    else:
                        foreign_currency = False

                    reconciled_vals.append({
                        'name': counterpart_line.name,
                        'journal_name': counterpart_line.journal_id.name,
                        'amount': reconciled_partial['amount'],
                        'currency_id': move.company_id.currency_id.id if reconciled_partial['is_exchange'] else reconciled_partial['currency'].id,
                        'date': counterpart_line.date,
                        'partial_id': reconciled_partial['partial_id'],
                        'account_payment_id': counterpart_line.payment_id.id,
                        'payment_method_name': counterpart_line.payment_id.payment_method_line_id.name,
                        'move_id': counterpart_line.move_id.id,
                        'ref': reconciliation_ref,
                        # these are necessary for the views to change depending on the values
                        'is_exchange': reconciled_partial['is_exchange'],
                        'amount_company_currency': formatLang(self.env, abs(counterpart_line.balance), currency_obj=counterpart_line.company_id.currency_id),
                        'amount_foreign_currency': foreign_currency and formatLang(self.env, abs(counterpart_line.amount_currency), currency_obj=foreign_currency),
                        'payment_mode_code': counterpart_line.payment_id.payment_mode_id.code ,
                        'payment_mode_name': counterpart_line.payment_id.payment_mode_id.name ,
                        'bank_name' : counterpart_line.payment_id.bank_id.name,
                        'payment_ref': counterpart_line.payment_id.reference,
                        'journal_type': counterpart_line.journal_id.type,
                        'agency': counterpart_line.payment_id.agency,
                        'swift_code': counterpart_line.payment_id.swift_code,

                    })
                payments_widget_vals['content'] = reconciled_vals

            if payments_widget_vals['content']:
                move.invoice_payments_widget = payments_widget_vals
            else:
                move.invoice_payments_widget = False