odoo.define('custom_addon.user_comment', function (require) {
'use strict';

var Dialog = require('web.Dialog');
var publicWidget = require('web.public.widget');

publicWidget.registry.HelloWorldPopup = publicWidget.Widget.extend({
    selector: '.oe_website_sale .oe_cart',

    events: {
        'change .js_add_comment': '_onAddcomment',
        'change .js_add_order_comment': '_onAddOrdercomment',
    },
    _onAddcomment: function (ev) {
        var $input = $(ev.currentTarget);
        var line_id = parseInt($input.data('line-id'), 10);
        this._rpc({
            route: "/shop/cart/update_comment",
            params: {
                line_id: line_id,
                comment: $input.val(),
            },
        })
    },

     _onAddOrdercomment: function (ev) {
        var $input = $(ev.currentTarget);
        this._rpc({
            route: "/shop/cart/update_order_comment",
            params: {
                comment: $input.val(),
            },
        })
    },

})
});