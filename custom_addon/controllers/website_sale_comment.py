
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo import http,_
from odoo.http import request

class WebsiteSaleComment(WebsiteSale):
    @http.route(['/shop/cart/update_comment'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_comment(self, line_id=None, comment=None):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order()
        if order.state != 'draft':
            request.website.sale_reset()
            return {}
        line_id = request.env['sale.order.line'].search([('id','=',line_id),('order_id','=',order.id)])
        if(line_id and comment):
            line_id.write({'comment_customer':comment})
        return True
    @http.route(['/shop/cart/update_order_comment'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_order_comment(self, comment=None):
        """This route is called when changing quantity from the cart or adding
        a product from the wishlist."""
        order = request.website.sale_get_order()
        if(order):
            order.write({'comment_customer':comment})
        return True

