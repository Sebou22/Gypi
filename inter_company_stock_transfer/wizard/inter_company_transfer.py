# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class InterCompanyTransfer(models.TransientModel):
    _name = 'inter.company.transfer'

    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda self: self.env.user.company_id)
    dest_company_id = fields.Many2one('res.company', string='Destination Company')
    location_id = fields.Many2one('stock.location', string='Source Location')
    dest_location_id = fields.Many2one('stock.location', string='Destination Location')
    line_ids = fields.One2many('inter.company.transfer.line', 'stock_transfer_id')

    @api.onchange('line_ids', 'location_id')
    def _onchange_line_ids(self):
        for line in self.line_ids:
            line.available_qty = self.env['stock.quant']._get_available_quantity(line.product_id, self.location_id)

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id and self.dest_company_id and \
                self.company_id.id == self.dest_company_id.id:
            raise ValidationError(_('Source and Destination Company must be '
                                    'different'))
        if self.company_id:
            self.location_id = False
            return {
                'domain': {
                    'location_id': [
                        ('company_id', '=', self.company_id.id),
                        ('usage', '=', 'internal')
                    ]
                }
            }

    @api.onchange('dest_company_id')
    def onchange_dest_company_id(self):
        if self.company_id and self.dest_company_id and \
                self.company_id.id == self.dest_company_id.id:
            raise ValidationError(_('Source and Destination Company must be '
                                    'different'))
        if self.dest_company_id:
            self.dest_location_id = False
            return {
                'domain': {
                    'dest_location_id': [
                        ('company_id', '=', self.dest_company_id.id),
                        ('usage', '=', 'internal')
                    ]
                }
            }

    @api.onchange('location_id', 'dest_location_id')
    def onchange_location(self):
        if self.location_id and self.dest_location_id and \
                self.location_id.id == self.dest_location_id.id:
            raise ValidationError(_('Source and Destination location must be '
                                    'different'))

    def _get_picking_type(self, picking_type, company_id):
        type_obj = self.env['stock.picking.type']
        types = type_obj.sudo().search([
            ('code', '=', picking_type),
            ('warehouse_id.company_id', '=', company_id)
        ])
        if not types:
            types = type_obj.sudo().search([
                ('code', '=', picking_type), ('warehouse_id', '=', False)])
        return types[:1]

    def button_transfer(self):
        self.ensure_one()
        StockPicking = self.env['stock.picking']
        out_picking_value = {}
        in_picking_value = {}
        out_picking_type_id = self._get_picking_type('outgoing', self.company_id.id)
        in_picking_type_id = self._get_picking_type('incoming', self.dest_company_id.id)
        if not out_picking_type_id:
            raise ValidationError(_('Operation type not Found for %s' %
                                    self.company_id.name))
        if not in_picking_type_id:
            raise ValidationError(_('Operation type not found for %s' %
                                    self.dest_company_id.name))
        transit_location_id = self.env['stock.location'].search([
            ('usage', '=', 'transit'), ('company_id', '=', False)
        ], limit=1)
        if not transit_location_id:
            raise ValidationError(_("Transit Location not found"))

        out_move_lines = []
        in_move_lines = []
        for line in self.line_ids:
            if float(line.available_qty) < line.product_uom_qty:
                raise ValidationError(
                    _(f'Initial Demand Can not be greater then available Quantity Check line Product {line.product_id.name}'))

            out_move_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom.id,
#                 'reserved_uom_qty': line.product_uom_qty,
#                 'reserved_qty': line.product_uom_qty,
                'qty_done': line.product_uom_qty,
                'company_id': self.company_id.id,
                'date': fields.Datetime.now(),
#                 'date': fields.Datetime.now(),
                'location_dest_id': transit_location_id.id,
                'location_id': self.location_id.id,
#                 'name': line.name,
#                 'procure_method': 'make_to_stock',
            }))

            in_move_lines.append((0, 0, {
                'product_id': line.product_id.id,
                'product_uom_id': line.product_uom.id,
#                 'reserved_uom_qty': line.product_uom_qty,
                'qty_done': line.product_uom_qty,
                'company_id': self.dest_company_id.id,
                'date': fields.Datetime.now(),
#                 'date': fields.Datetime.now(),
                'location_dest_id': self.dest_location_id.id,
                'location_id': transit_location_id.id,
#                 'name': line.name,
#                 'procure_method': 'make_to_stock',
            }))
        out_picking_value.update({
            'intercompany_transfer': True,
            'move_type': 'direct',
            'state': 'draft',
            'picking_type_id': out_picking_type_id.id,
            'company_id': self.company_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': transit_location_id.id,
            'origin': 'Inter-entreprises',
            'move_line_ids': out_move_lines,
        })
        out_picking_id = StockPicking.create(out_picking_value)
        _logger.error("AAAAAAAAAAAAAAAAAAAAAAAAAAA")
            
        out_picking_id.action_assign()
        _logger.error("BBBBBBBBBBBBBBBBBBBBBBBBBBB")
        for mm in out_picking_id.move_ids:
            mm.product_uom_qty = mm.quantity_done
        out_picking_id.action_set_quantities_to_reservation()
        _logger.error("CCCCCCCCCCCCCCCCCCCC")
        out_picking_id.button_validate()
        _logger.error("DDDDDDDDDDDDDDDDDDDDDD")

        in_picking_value.update({
            'intercompany_transfer': True,
            'move_type': 'direct',
            'state': 'draft',
            'picking_type_id': in_picking_type_id.id,
            'company_id': self.dest_company_id.id,
            'location_id': transit_location_id.id,
            'location_dest_id': self.dest_location_id.id,
            'origin': 'Inter-entreprises %s' % (out_picking_id and
                                                    out_picking_id.name or ''),
            'move_line_ids': in_move_lines,
        })
        in_picking_id = StockPicking.sudo().create(in_picking_value)
        _logger.error("1111111111111111111111111111111111111111")
        in_picking_id.sudo().action_confirm()
        _logger.error("222222222222222222222222222222")
        for nn in in_picking_id.move_ids:
            nn.product_uom_qty = nn.quantity_done
        in_picking_id.sudo().action_set_quantities_to_reservation()
        _logger.error("33333333333333333333333333333333")
#         in_picking_id.button_validate()
        _logger.error("444444444444444444444444444444444")
