# -*- coding: utf-8 -*-

from datetime import datetime, date
from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    hours_work = fields.Float("Hour Work",default = lambda self: self.env.company.hours_work)


