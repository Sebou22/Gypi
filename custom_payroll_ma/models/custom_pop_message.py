from odoo import api, fields, models, _


class CustomPopupMessage(models.TransientModel):

    _name = "custom.pop.message"
    _description = "Alert"

    name = fields.Html('Message')
