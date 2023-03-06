try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO
from odoo import models, fields, api, _
from odoo.exceptions import UserError
class ProductProductInherit(models.Model):
    _inherit = "product.product"
    price_with_tax = fields.Float(compute='_compute_price_with_tax')
    @api.depends('lst_price', 'product_tmpl_id', 'taxes_id')
    def _compute_price_with_tax(self):
        for record in self:
            record.price_with_tax = record.product_tmpl_id._construct_price_with_tax(record.lst_price)



class ProductTemplateInherit(models.Model):
    _inherit = "product.template"
    qr_code = fields.Binary('QRcode', compute="_generate_qr")

    def _construct_price_with_tax(self, price):
        res = self.taxes_id.sudo().compute_all(price, product=self, partner=self.env['res.partner'])
        included = res['total_included']
        return included

    def _generate_qr(self):
        "method to generate QR code"
        for rec in self:
            if qrcode and base64:

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data("Product : ")
                qr.add_data(rec.name)
                qr.add_data(", Reference : ")
                qr.add_data(rec.default_code)
                qr.add_data(", Price : ")
                qr.add_data(rec.list_price)
                qr.add_data(", Quantity : ")
                qr.add_data(rec.qty_available)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
            else:
                raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))