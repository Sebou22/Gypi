# -*- coding: utf-8 -*-
from odoo import models, fields, _, api
import logging

_logger = logging.getLogger(__name__)
class PreprationOrder(models.Model):
    _name = 'preparation.order'

    name = fields.Char(
        'Reference', default='/',
        copy=False, index=True, readonly=True)
    state = fields.Selection([
        ('progress', 'In Progress'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        )

    @api.depends("stock_picking_ids")
    def _get_list_product(self):
        for rec in self:
            rec.stock_move_ids=[(5,)]
            data_list = []
            ligne_ids = rec.stock_picking_ids.mapped('move_ids_without_package')
            products_ids = ligne_ids.mapped('product_id')
            for product in products_ids:
                list = ligne_ids.filtered(lambda r :r.product_id.id == product.id)
                quanty_done = sum([line.quantity_done for line in list])
                product_uom_qty = sum([line.product_uom_qty for line in list])
                reserved_availability = sum([line.reserved_availability for line in list])
                data_list.append((0, 0, {
                    'product_id': product.id,
                    'quantity_done': quanty_done,
                    'reserved_availability': reserved_availability,
                    'product_uom_qty': product_uom_qty,
                }))
            rec.stock_move_ids = data_list
            rec.ftest = True

    ftest = fields.Boolean("test",compute="_get_list_product",store=True)
    stock_move_ids = fields.One2many('product.list', 'preparation_id', string="Stock moves in preparation",readonly=True)
    stock_picking_ids = fields.Many2many('stock.picking', string="Stock moves in preparation")
    sale_ids = fields.Many2many('sale.order',compute="_get_sale",store=True)
    count_sale_ids = fields.Integer('Count sale order',compute="_get_sale",store=True)
    show_mark_as_todo = fields.Boolean(compute='_compute_show_mark_as_todo',help='Technical field used to compute whether the button "Mark as Todo" should be displayed.')
    show_check_availability = fields.Boolean(compute='_compute_show_check_availability',help='Technical field used to compute whether the button "Check Availability" should be displayed.')

    _sql_constraints = [
        ('name_uniq', 'unique(name, company_id)', 'Reference must be unique per company!'),
    ]

    @api.depends('stock_picking_ids')
    def _get_sale(self):
        for rec in self:
            if(rec.stock_picking_ids):
                sale_ids = rec.stock_picking_ids.mapped('sale_id').ids
                rec.sale_ids = [(6, 0, sale_ids)]
                rec.count_sale_ids = len(sale_ids)



    @api.model
    def create(self, vals):
        sequence_id = self.env.ref('gypi_picking_order.seq_preparation_out')
        vals['name'] = sequence_id.next_by_id()
        res = super(PreprationOrder, self).create(vals)
        return res



    @api.depends('stock_picking_ids','stock_picking_ids.state')
    def _compute_state(self):
        for rec in self:
            state= "progress"
            if (all([x.state == "assigned" for x in rec.stock_picking_ids])):
                state="assigned"
            elif (all([x.state == "done" for x in rec.stock_picking_ids])):
                state="done"
            rec.state=state



    def action_assign(self):
        for record in self:
            record.stock_picking_ids.action_assign()


    def action_confirm(self):
        for record in self:
            record.stock_picking_ids.action_confirm()


    @api.depends('stock_picking_ids')
    def _compute_show_mark_as_todo(self):
        for record in self:
            if any(pk.show_mark_as_todo for pk in record.stock_picking_ids):
                record.show_mark_as_todo = True
            else:
                record.show_mark_as_todo = False


    @api.depends('stock_picking_ids')
    def _compute_show_check_availability(self):
        for record in self:
            if any(pk.show_check_availability for pk in record.stock_picking_ids):
                record.show_check_availability = True
            else:
                record.show_check_availability = False









