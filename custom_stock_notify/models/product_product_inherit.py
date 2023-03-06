from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
class ProductProduct(models.Model):
    _inherit = "product.product"

    def _send_availability_email(self):
        for product in self.search([('stock_notification_partner_ids', '!=', False)]):
            for partner in product.stock_notification_partner_ids:
                body_html = self.env['ir.qweb'].with_context(lang= partner.lang or self.env.lang)._render('website_sale_stock.availability_email_body',
                                                        {"product": product})
                msg = self.env["mail.message"].sudo().new(dict(body=body_html, record_name=product.name))
                full_mail = self.env["mail.render.mixin"]._render_encapsulate(
                    "mail.mail_notification_light",
                    body_html,
                    add_context=dict(message=msg, model_description=_("Product")),
                )
                mail_values = {
                    "subject": _("The product '%(product_name)s' is now available") % {'product_name': product.name},
                    "email_from": (product.company_id.partner_id or self.env.user).email_formatted,
                    "email_to": partner.email_formatted,
                    "body_html": full_mail,
                }

                mail = self.env["mail.mail"].sudo().create(mail_values)
                mail.send(raise_exception=False)
                product.stock_notification_partner_ids -= partner
