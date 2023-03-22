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
                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url') or ''
                url = "%s%s" %(base_url,rec.website_url)

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(url)
                qr.make(fit=True)
                img = qr.make_image()
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())
                rec.update({'qr_code': qr_image})
            else:
                raise UserError(_('Necessary Requirements To Run This Operation Is Not Satisfied'))

    restriction_type = fields.Selection(selection=[('neither','Neither'),('all', 'All'),('section', 'Section')],string='Contact Restriction',default='neither',required=True)
    restriction_contacts = fields.Many2many('res.users', string='Contact')
    restrict_ok = fields.Boolean('Restriction state', compute="_get_state_restriction",search="_value_search")


    def write(self, values):
        res = super(ProductTemplateInherit, self).write(values)
        if 'restriction_type' in values or 'restriction_contacts' in values:
            self.clear_caches()
        return res

    def _get_state_restriction(self):
        user = self.env.user.id
        for rec in self:
            flag = True
            if(rec.restriction_type=='all' or (rec.restriction_type=='section' and user in rec.restriction_contacts.ids)):
                flag = False
            elif(all([x.restriction_type=='all' or (x.restriction_type=='section' and user in x.restriction_contacts.ids) for x in rec.public_categ_ids])):
                flag = False
            rec.restrict_ok = flag

    def _value_search(self, operator, value):
        recs = self.search([]).filtered(lambda x: x.restrict_ok is False)
        if recs:
            return [('id', 'in', [x.id for x in recs])]
