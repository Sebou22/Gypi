# -*- coding: utf-8 -*-

from datetime import datetime, timedelta, time, date
from odoo import api, fields, models, _
from odoo import SUPERUSER_ID
from odoo.http import request
import logging
import math

_logger = logging.getLogger(__name__)


class HrAttendanceSend(models.TransientModel):
    _name = 'hr.attendance.send'


    @api.model
    def _cron_attendance_notification(self):
        current_date = datetime.now()
        employees = self.env['hr.employee'].search([])
        data_list1 = []
        data_list2 = []
        for employee in employees:
            state ="Absence"
            emp_attendance = self.env['hr.attendance'].sudo().search(
                [
                    ('employee_id', '=', employee.id),
                    ('check_in', '>=', current_date.strftime(
                        '%Y-%m-%d 00:00:00')),
                    ('check_out', '<=', current_date.strftime(
                        '%Y-%m-%d 23:59:59')),
                ])
            if not emp_attendance:
                emp_holiday = self.env['hr.leave'].sudo().search([
                    ('employee_id', '=', employee.id),
                    ('state', '=', 'validate'),
                    ('date_to', '>=',
                     current_date.strftime('%Y-%m-%d 00:00:00')),
                ])
                if(emp_holiday):
                    state = "Congé"
                data_list1.append({'employee':employee.name,'state':state})

        template_id = request.env.ref('hr_attendance_notification.mail_template_edi_attendance_notification',raise_if_not_found=False)
        if template_id:
            local_context = {'employee_ids': data_list1}
            template_id.with_context(local_context).send_mail(self.id,force_send=True,)

    @api.model
    def _cron_retard_notification(self):
        current_date = datetime.now()
        list_employee = []
        company_marge = self.env.user.company_id.marge_retard
        marge = timedelta(minutes=company_marge)
        attendance_ids = self.env['hr.attendance'].sudo().search([
                        ('check_in', '>=', current_date.strftime(
                            '%Y-%m-%d 00:00:00'))
                    ])
        for attendance in attendance_ids:
            hours, minutes = divmod(int(abs(attendance.employee_id.hours_work) * 60), 60)
            datetime_work = datetime.combine(current_date, time(hours, minutes))
            check_in = attendance.check_in
            diff = abs(check_in - datetime_work)-marge
            if(diff.total_seconds()>0):
                list_employee.append({'employee':attendance.employee_id.name,'check_in':check_in.time(),'origin_in':datetime_work.time(),'retard':diff,'marge':math.floor(company_marge)})

        template_id = request.env.ref(
            'hr_attendance_notification.mail_template_edi_retard_notification',
            raise_if_not_found=False)
        if template_id:
            local_context = {'retard_ids': list_employee}
            template_id.with_context(local_context).send_mail(
                self.id,
                force_send=True,
            )








