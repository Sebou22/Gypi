from odoo import api, fields, models, SUPERUSER_ID, _
import requests
import logging
from datetime import datetime
from odoo.exceptions import UserError
import json
import re
import csv
import base64
from psycopg2.extensions import JSON
from odoo.tools.image import image_data_uri
from re import sub
from decimal import Decimal

_logger = logging.getLogger(__name__)


class LogisticsClass(models.Model):
    _name = "mirakl.logistics.class"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl Logistics ID", required=True)


class ProductTemplate(models.Model):
    _inherit = "product.product"

    sync_to_mirakl = fields.Boolean("Sync to Mirakl")
    mirakl_description = fields.Text("Description fr-FR")
    mirakl_color_id = fields.Many2one('mirakl.product.color', string="Color")
    mirakl_brand_id = fields.Many2one('mirakl.product.brand', string="Brand")
    mirakl_natureofwheel_id = fields.Many2one('mirakl.product.naturewheel', string="Product Type")
    mirakl_sport_ids = fields.Many2many('mirakl.product.sport', string="Sports")
    main_image_url = fields.Char("Mirakl Main Image URL", compute='_create_image_attachment')
    mirakl_product_title_fr = fields.Char("Product Title fr-FR")
    mirakl_size_21_id = fields.Many2one('mirakl.product.size', string="SIZE_21")
    mirakl_category_id = fields.Many2one('mirakl.product.categories', string="Mirakl Product Category")
    mirakl_Webcatchline = fields.Text("Webcatchline")
    mirakl_etat_id = fields.Many2one('mirakl.product.state', "CHARACTERISTIC_748")

    def _default_logistic_class(self):
        return self.env['mirakl.logistics.class'].search([('mirakl_id', '=', 'free shipping')], limit=1).id

    mirakl_logistic_class = fields.Many2one('mirakl.logistics.class', "Mirakl Logistic Class",
                                            default=_default_logistic_class)
    mirakl_delivery_time = fields.Integer(default=2, string="Mirakl Delivery Time")
    mirakl_quantity_alert = fields.Integer(default=2, string="Mirakl Quantity alert")

    def _create_image_attachment(self):
        for rec in self:
            if rec.image_1920:
                image = self.env['ir.attachment'].search(
                    [('name', '=', rec.name), ('res_model', '=', 'product.product'), ('res_id', '=', rec.id), ('datas', '=', rec.image_1920)], limit=1)
                if not image:
                    image = self.env['ir.attachment'].create(dict(
                        name=rec.name,
                        datas=base64.b64encode(rec.image_1920),
                        mimetype='image/png',
                        res_model='product.product',
                        res_id=rec.id,
                    ))
                self.env.cr.commit()
                rec.main_image_url = image.local_url

    def import_category_from_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        flag = False
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/hierarchies"
            response = requests.get(url, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                hierarchy = response_data['hierarchies']
                for rec in hierarchy:
                    if rec:
                        existing = self.env['mirakl.product.categories'].sudo().search(
                            [('mirakl_code', '=', rec['code'])])
                        if not existing:
                            flag = True
                            parent_code = self.env['mirakl.product.categories'].sudo().search(
                                [('mirakl_code', '=', rec['parent_code'])])
                            color = self.env['mirakl.product.categories'].sudo().create({
                                'mirakl_code': rec['code'],
                                'name': rec['label'],
                                'parent_code': parent_code.id if parent_code else None,
                                'display_name': rec['label'] if not parent_code else None
                            })
                            self.env.cr.commit()
                            if parent_code:
                                if parent_code.display_name:
                                    color.display_name = parent_code.display_name + "/" + color.name
                                else:
                                    color.display_name = color.name
                            _logger.info(
                                "\nCategories created successfully from MIRAKL" + " Created_id:" + str(
                                    color.id))
                if flag == False:
                    raise UserError(
                        _("There are no new Categories to sync from Mirakl, Existing  Categories are already synced."))

    def import_attribute_from_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        flag = False
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/values_lists"
            params = {
                'code': 'color',
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                value_list = response_data['values_lists']
                value = value_list[0]

                for rec in value['values']:
                    if rec:
                        existing = self.env['mirakl.product.color'].sudo().search(
                            [('mirakl_id', '=', rec['code'])])
                        if not existing:
                            flag = True
                            color = self.env['mirakl.product.color'].sudo().create({
                                'mirakl_id': rec['code'],
                                'name': rec['label'],
                            })
                            self.env.cr.commit()
                            _logger.info(
                                "\nColor Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                    color.id))
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/values_lists"
            params = {
                'code': 'brandName',
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                value_list = response_data['values_lists']
                value = value_list[0]
                for rec in value['values']:
                    if rec:
                        existing = self.env['mirakl.product.brand'].sudo().search(
                            [('mirakl_id', '=', rec['code'])])
                        if not existing:
                            flag = True
                            brand = self.env['mirakl.product.brand'].sudo().create({
                                'mirakl_id': rec['code'],
                                'name': rec['label'],
                            })
                            self.env.cr.commit()
                            _logger.info(
                                "\nBrand Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                    brand.id))
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/values_lists"
            params = {
                'code': 'sports-174'
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                value_list = response_data['values_lists']
                value = value_list[0]
                for rec in value['values']:
                    if rec:
                        existing = self.env['mirakl.product.sport'].sudo().search(
                            [('mirakl_id', '=', rec['code'])])
                        if not existing:
                            flag = True
                            brand = self.env['mirakl.product.sport'].sudo().create({
                                'mirakl_id': rec['code'],
                                'name': rec['label'],
                            })
                            self.env.cr.commit()
                            _logger.info(
                                "\nSports Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                    brand.id))
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/values_lists"
            params = {
                'code': 'size-21'
            }
            response = requests.get(url, params=params, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                value_list = response_data['values_lists']
                value = value_list[0]
                for rec in value['values']:
                    if rec:
                        existing = self.env['mirakl.product.size'].sudo().search(
                            [('mirakl_id', '=', rec['code'])])
                        if not existing:
                            flag = True
                            brand = self.env['mirakl.product.size'].sudo().create({
                                'mirakl_id': rec['code'],
                                'name': rec['label'],
                            })
                            self.env.cr.commit()
                            _logger.info(
                                "\nSize_21 Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                    brand.id))
        if api_url and api_key:
            headerss = {"Authorization": str(api_key)}
            a_url = api_url + "/api/products/attributes"
            responsee = requests.get(a_url, headers=headerss)
            ls = []
            if responsee.status_code == 201 or responsee.status_code == 200:
                response_data = responsee.json()
                response_attribute = response_data['attributes']
                for rec in response_attribute:
                    if rec['code'] == 'CHARACTERISTIC_748':
                        headers = {"Authorization": str(api_key)}
                        url = api_url + "/api/values_lists"
                        params = {
                            'code': rec['type_parameter']
                        }
                        response = requests.get(url, params=params, headers=headers)
                        if response.status_code == 201 or response.status_code == 200:
                            response_data = response.json()
                            value_li = response_data['values_lists']
                            dataa = value_li[0]
                            valuess = dataa['values']
                            for recs in valuess:
                                if recs:
                                    existing = self.env['mirakl.product.state'].sudo().search(
                                        [('mirakl_id', '=', recs['code'])])
                                    if not existing:
                                        flag = True
                                        wheel = self.env['mirakl.product.state'].sudo().create({
                                            'mirakl_id': recs['code'],
                                            'name': recs['label'],
                                        })
                                        self.env.cr.commit()
                                        _logger.info(
                                            "\nCHARACTERISTIC_748 Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                                wheel.id))
        if api_url and api_key:
            headerss = {"Authorization": str(api_key)}
            a_url = api_url + "/api/products/attributes"
            responsee = requests.get(a_url, headers=headerss)
            ls = []
            if responsee.status_code == 201 or responsee.status_code == 200:
                response_data = responsee.json()
                response_attribute = response_data['attributes']
                for rec in response_attribute:
                    if rec['code'] == 'PRODUCT_TYPE':
                        headers = {"Authorization": str(api_key)}
                        url = api_url + "/api/values_lists"
                        params = {
                            'code': rec['type_parameter']
                        }
                        response = requests.get(url, params=params, headers=headers)
                        if response.status_code == 201 or response.status_code == 200:
                            response_data = response.json()
                            value_li = response_data['values_lists']
                            dataa = value_li[0]
                            valuess = dataa['values']
                            for recs in valuess:
                                if recs:
                                    existing = self.env['mirakl.product.naturewheel'].sudo().search(
                                        [('mirakl_id', '=', recs['code'])])
                                    if not existing:
                                        flag = True
                                        wheel = self.env['mirakl.product.naturewheel'].sudo().create({
                                            'mirakl_id': recs['code'],
                                            'name': recs['label'],
                                        })
                                        self.env.cr.commit()
                                        _logger.info(
                                            "\nPRODUCT_TYPE Attribute created successfully from MIRAKL" + " Created_id:" + str(
                                                wheel.id))

        if flag == False:
            raise UserError(
                _("There are no Attributes to sync from Mirakl."))

    def export_all_products_to_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        lst = []
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            products = self
            if not products:
                products = self.env['product.product'].search([])
            prod_mapped = products.mapped('barcode')
            for rec in prod_mapped:
                if rec:
                    res = "EAN|" + rec
                    lst.append(res)
            prod_id = []
            for i in range(0, len(lst), 100):
                x = lst[i:i + 100]
                lst1 = '[%s]' % ','.join(map(str, x))
                resul = str(lst1)[1:-1]
                url = api_url + "/api/products?product_references=" + resul
                response = requests.get(url, headers=headers)
                existing_rec = response.json()
                prod_id.append(existing_rec['products'])
            prod_lis = []
            for prod_data in prod_id:
                for rec in prod_data:
                    prod_lis.append(rec['product_id'])
            non_existing_products = products.filtered(lambda l: l.barcode not in prod_lis)
            flag = False
            with open('product.csv', mode='w') as file:
                writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow(
                    ['mainTitle', 'price', 'sku', 'ean_codes', 'main_image', 'category', 'ProductIdentifier',
                     'longDescription-fr_FR', 'color', 'brandName', 'PRODUCT_TYPE', 'SPORT_29', 'productTitle-fr_FR',
                     'SIZE_21', 'webcatchline-fr_FR', 'CHARACTERISTIC_748'])
                for pr in products:
                    if pr.sync_to_mirakl == True:
                        flag = True
                        Sports_list = pr.mirakl_sport_ids.mapped('mirakl_id')
                        lst2 = '[%s]' % ' / '.join(map(str, Sports_list))
                        resul = str(lst2)[1:-1]
                        unique_id = pr.main_image_url
                        if unique_id:
                            split = unique_id.split('?')[1]
                        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                        image_model_url = '/web/image?model=product.product&id=' + str(pr.id) +'&field=image_1920&'
                        if base_url and image_model_url and split:
                            image_url = base_url + image_model_url + split
                        name = pr.name
                        price = pr.lst_price
                        sku = pr.default_code
                        ean = pr.barcode
                        main_image = image_url
                        category = pr.mirakl_category_id.mirakl_code
                        product_identifier = pr.default_code
                        description = pr.mirakl_description
                        color = pr.mirakl_color_id.mirakl_id
                        brand_name = pr.mirakl_brand_id.mirakl_id
                        PRODUCT_TYPE = pr.mirakl_natureofwheel_id.mirakl_id
                        Sports = resul
                        producttitlefr = pr.mirakl_product_title_fr
                        size_21 = pr.mirakl_size_21_id.mirakl_id
                        webcatchline = pr.mirakl_Webcatchline
                        characteristic_748 = pr.mirakl_etat_id.mirakl_id
                        writer.writerow(
                            [name, price, sku, ean, main_image, category, product_identifier, description, color,
                             brand_name, PRODUCT_TYPE, Sports, producttitlefr, size_21, webcatchline,
                             characteristic_748])
            with open('product.csv', 'r', encoding="utf-8") as f2:
                # file encode and store in a variable ‘data’
                data = str.encode(f2.read(), 'utf-8')
            if flag == True:
                if api_url and api_key:
                    headers = {"Authorization": str(api_key)}
                    url = api_url + "/api/products/imports"
                    files = {
                        'file': ('product.csv', open('product.csv', 'rb'))
                    }
                    params = {
                        "shop_id": 7860
                    }
                    response = requests.post(url, headers=headers, params=params, files=files)
                    _logger.info("\nProduct Export Status Code" + str(response.status_code))
                    if response.status_code == 201 or response.status_code == 200:
                        response_data = response.json()




class ProductSport(models.Model):
    _name = "mirakl.product.sport"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl Sport ID", required=True)


class ProductProductColor(models.Model):
    _name = "mirakl.product.color"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl Color ID", required=True)


class ProductNatureofwheel(models.Model):
    _name = "mirakl.product.naturewheel"

    mirakl_id = fields.Char("Mirakl Code", required=True)
    name = fields.Char("Name", required=True)


class ProductProductBrand(models.Model):
    _name = "mirakl.product.brand"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl Brand ID", required=True)


class ProductProductSize(models.Model):
    _name = "mirakl.product.size"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl Size ID", required=True)


class ProductProductState(models.Model):
    _name = "mirakl.product.state"

    name = fields.Char("Name", required=True)
    mirakl_id = fields.Char("Mirakl ID", required=True)


class ProductProductCategories(models.Model):
    _name = "mirakl.product.categories"
    _rec_name = "display_name"

    display_name = fields.Char("Display Name")
    name = fields.Char("Name", required=True)
    mirakl_code = fields.Char("Mirakl Code", required=True)
    parent_code = fields.Many2one('mirakl.product.categories')


class SaleOrder(models.Model):
    _inherit = "sale.order"

    mirakl_order_id = fields.Char("Mirakl Order ID", store=True, readonly=True)
    mirakl_create_date = fields.Datetime("Mirakl Order Create Date", readonly=True)

    def import_orders_from_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        property_account_receivable_id = Param.get('property_account_receivable_id')
        property_account_payable_id = Param.get('property_account_payable_id')
        if not property_account_receivable_id:
            property_account_receivable_id = False
        if not property_account_payable_id:
            property_account_payable_id = False
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/orders"
            params = {
                "max": 100,
                "offset": 0,
                "paginate": 'false',
            }
            response = requests.get(url, params=params, headers=headers)
            sale_order = self.env['sale.order']
            if response.status_code == 201 or response.status_code == 200:
                header_response = response.headers
                response_data = response.json()
                data = response_data['orders']
                no_order_flag = False
                for rec in data:
                    customer_rec = rec['customer']
                    shipping_add = customer_rec['shipping_address']
                    shipping = self.env['res.partner'].sudo().search(
                        [('name', '=', shipping_add['firstname'] + ' ' + shipping_add['lastname']),
                         ('zip', '=', shipping_add['zip_code']),
                         ('country_id.code', '=', shipping_add['country'])])
                    if not shipping:
                        shipping = self.env['res.partner'].sudo().create({
                            'name': shipping_add['firstname'] + ' ' + shipping_add['lastname'],
                            'type': 'contact',
                            'zip': shipping_add['zip_code'],
                            'street': shipping_add['street_1'],
                            'street2': shipping_add['street_2'],
                            'city': shipping_add['city'],
                            'mobile': shipping_add['phone'],
                            'country_id': self.env['res.country'].search(
                                [('code', '=', shipping_add['country'])]).id,
                            'state_id': self.env['res.country.state'].search(
                                [('code', '=', shipping_add['state'])]).id,
                            'property_account_receivable_id': property_account_receivable_id,
                            'property_account_payable_id': property_account_payable_id,
                            'email': rec['customer_notification_email'],
                            'lang': 'fr_FR'
                        })
                        self.env.cr.commit()
                        _logger.info(
                            "\nCustomer Address created successfully from MIRAKL" + " Created_id:" + str(
                                shipping.id))
                    date_mirakl = rec['created_date']
                    order_id = rec['order_id']
                    order_date = date_mirakl.split("T")
                    datemirakl = datetime.strptime(order_date[0] + ' ' + order_date[1], '%Y-%m-%d %H:%M:%SZ')
                    date_mirakl = datemirakl
                    sale_order = self.env['sale.order'].sudo().search([])
                    order_filter = sale_order.filtered(lambda l: l.mirakl_order_id == order_id)
                    if not order_filter:
                        no_order_flag = True
                        salesperson = Param.get('user_id')
                        salesteam = Param.get('team_id')
                        if salesperson:
                            pass
                        else:
                            salesperson = False
                        if salesteam:
                            pass
                        else:
                            salesteam = False
                        dict = {'partner_id': shipping.id,
                                'partner_invoice_id': shipping.id,
                                'partner_shipping_id': shipping.id,
                                'mirakl_create_date': date_mirakl,
                                'mirakl_order_id': order_id,
                                'user_id': salesperson,
                                'team_id': salesteam
                                }
                        order = self.env['sale.order'].sudo().create(dict)
                        self.env.cr.commit()
                        _logger.info(
                            "\nSale Order created successfully from MIRAKL" + " Created_id:" + str(
                                order.id))
                        lines = rec['order_lines']
                        for res in lines:
                            mirakl_product_sku = res['offer_sku']
                            product = self.env['product.product'].sudo().search(
                                [('default_code', '=', mirakl_product_sku)])
                            if product:
                                product = self.env['product.product'].sudo().search(
                                    [('default_code', '=', mirakl_product_sku)])
                            else:
                                product = self.env['product.product'].sudo().create({
                                    'name': res['product_title'],
                                    'detailed_type': 'product',
                                    'list_price': res['price'],
                                    'default_code': res['offer_sku'],
                                })
                                self.env.cr.commit()
                            if product:
                                order_lines_dict = {
                                    'product_id': product.id,
                                    'product_template_id': self.env['product.template'].sudo().search(
                                        [('product_variant_ids', 'in', product.ids)]).id,
                                    'product_uom_qty': res['quantity'],
                                    'order_id': order.id,
                                    'customer_lead': rec['leadtime_to_ship']
                                }
                                order_line = self.env['sale.order.line'].sudo().create(order_lines_dict)
                                self.env.cr.commit()
                                _logger.info(
                                    "\nSale Order line created successfully from MIRAKL for OrderID" + str(
                                        order.id) + " Created_id Line ID:" + str(
                                        order_line.id))
                        if rec['order_state'] == 'SHIPPING':
                            order.sudo().action_confirm()

                if no_order_flag == False:
                    raise UserError(
                        _("There are no new orders to sync from Mirakl, Existing orders are already synced."))


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    api_url = fields.Char(string="Mirakl Api URL", store=True)
    api_key = fields.Char(string="Mirakl Api Key", store=True)
    user_id = fields.Many2one('res.users', string='Salesperson', store=True)
    team_id = fields.Many2one('crm.team', string='Sales Team', store=True)
    property_account_receivable_id = fields.Many2one('account.account', string='Receivable Account')
    property_account_payable_id = fields.Many2one('account.account', string='Payable Account')

    def call_import_offer_attributes(self):
        self.env['product.pricelist'].sudo().import_offers_attributes()

    def call_export_shipping_details(self):
        self.env['stock.picking'].sudo().send_shipping_details_to_mirakl()

    def call_function_sale_order(self):
        self.env['sale.order'].sudo().import_orders_from_mirakl()

    def call_function_product_category(self):
        self.env['product.product'].sudo().import_category_from_mirakl()

    def call_function_product_attribute(self):
        self.env['product.product'].sudo().import_attribute_from_mirakl()

    def call_export_product_product(self):
        self.env['product.product'].sudo().export_all_products_to_mirakl()

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.api_url', self.api_url)
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.api_key', self.api_key)
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.user_id', self.user_id.id)
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.team_id', self.team_id.id)
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.property_account_receivable_id', self.property_account_receivable_id.id)
        self.env['ir.config_parameter'].set_param(
            'odoo_mirakl_integration.property_account_payable_id', self.property_account_payable_id.id)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_url=params.get_param('odoo_mirakl_integration.api_url'),
            api_key=params.get_param('odoo_mirakl_integration.api_key'),
            user_id=int(params.get_param('odoo_mirakl_integration.user_id')),
            team_id=int(params.get_param('odoo_mirakl_integration.team_id')),
            property_account_receivable_id=int(
                params.get_param('odoo_mirakl_integration.property_account_receivable_id')),
            property_account_payable_id=int(params.get_param('odoo_mirakl_integration.property_account_payable_id')),
        )
        return res


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mirakl_order_id = fields.Char("Mirakl Order ID", related='sale_id.mirakl_order_id')
    mirakl_tracking_url = fields.Char("Mirakl Tracking URL")

    def send_shipping_details_to_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        url = api_url + "/api/shipments"
        if api_url and api_key:
            if self:
                stock_picking = self
            else:
                stock_picking = self.env['stock.picking'].search([])
            shipping = []
            for rec in stock_picking:
                if rec.state == 'done':
                    tracking = {
                        "carrier_code": rec.carrier_id.name,
                        "carrier_name": rec.carrier_id.name,
                        "tracking_number": rec.carrier_tracking_ref,
                        "tracking_url": rec.mirakl_tracking_url,
                    }
                    shipment_lines = []
                    for res in rec.move_line_ids:
                        line = {
                            "offer_sku": res.product_id.default_code,
                            "quantity": res.qty_done
                        }
                        shipment_lines.append(line)
                    shipments = {
                        "order_id": rec.mirakl_order_id,
                        "tracking": tracking,
                        "shipment_lines": shipment_lines,
                        "shipped": 'true'
                    }
                    shipping.append(shipments)
                else:
                    raise UserError("Please Validate the Delivery Order")

            tmp = {"shipments": shipping}
            headers = {"Authorization": str(api_key), "Content-Type": "application/json"}
            response = requests.post(url, json.dumps(tmp), headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()
                if response_data['shipment_errors']:
                    shippment_error = response_data['shipment_errors'][0]
                    raise UserError(
                        "Shipping Export Failed Error Message: " + str(shippment_error['message']) + "Order ID: " + str(
                            shippment_error['order_id']))


class Pricelist(models.Model):
    _inherit = "product.pricelist"

    is_sync_to_mirakl = fields.Boolean("Sync to Mirakl")

    def import_offers_attributes(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        flag = False
        if api_url and api_key:
            headers = {"Authorization": str(api_key)}
            url = api_url + "/api/shipping/logistic_classes"
            response = requests.get(url, headers=headers)
            if response.status_code == 201 or response.status_code == 200:
                response_data = response.json()

                if response_data:
                    classses = response_data['logistic_classes']
                    flag = False
                    for rec in classses:
                        if rec:
                            existing = self.env['mirakl.logistics.class'].sudo().search(
                                [('mirakl_id', '=', rec['code'])])
                            if not existing:
                                flag = True
                                wheel = self.env['mirakl.logistics.class'].sudo().create({
                                    'mirakl_id': rec['code'],
                                    'name': rec['label'],
                                })
                                self.env.cr.commit()
                                _logger.info(
                                    "\nLogistics Class created successfully from MIRAKL" + " Created_id:" + str(
                                        wheel.id))
                    if flag == False:
                        raise UserError(
                            _("There are no new Logistics Class to sync from Mirakl."))

    def export_price_list_to_mirakl(self):
        Param = self.env['res.config.settings'].sudo().get_values()
        api_url = Param.get('api_url')
        api_key = Param.get('api_key')
        url = api_url + "/api/offers"
        if api_url and api_key:
            headers = {"Authorization": str(api_key), "Content-Type": "application/json"}
            if self.is_sync_to_mirakl == True:
                for rec in self.item_ids:
                    price = str(rec.price).replace(',', '.')
                    lst_price = str(rec.product_id.lst_price).replace(',', '.')
                    price_value = Decimal(sub(r'[^\d.]', '', price))
                    price_value_1 = Decimal(sub(r'[^\d.]', '', lst_price))
                    tmp_dict = {
                        "offers": [
                            {
                                "allow_quote_requests": False,
                                "description": "Offer for product" + rec.name,
                                "price": str(price_value),
                                "all_prices": [
                                    {
                                        "channel_code": "FR",
                                        "volume_prices": [
                                            {
                                                "quantity_threshold": rec.min_quantity,
                                                "unit_discount_price": str(price_value),
                                                "unit_origin_price": str(price_value_1)
                                            }
                                        ]
                                    }
                                ],
                                "product_id": rec.product_id.barcode,
                                "product_id_type": "EAN",
                                "shop_sku": rec.product_id.default_code,
                                "quantity": rec.product_id.qty_available,
                                "state_code": "11",
                                "update_delete": "update",
                                "leadtime_to_ship": rec.product_id.mirakl_delivery_time,
                                "logistic_class": str(rec.product_id.mirakl_logistic_class.mirakl_id)

                            }
                        ]
                    }
                    response = requests.post(url, json.dumps(tmp_dict), headers=headers)
                    if response.status_code == 201 or response.status_code == 200:
                        _logger.info(
                            "\nOffer exported Successfully" + str(response.json()))
