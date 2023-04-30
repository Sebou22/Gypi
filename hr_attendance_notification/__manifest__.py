# -*- encoding: utf-8 -*-
{
    'name': 'HR Attendance Notification',
    'category': 'Human Resources',
    'author': 'KHALLOUT Asmaa',
    "license": "AGPL-3",
    "version": "16.0.1",
    'depends': ['hr'],

    'data': [
        'security/ir.model.access.csv',
        'views/hr_employee_views_inherit.xml',
        'data/attendance_notification_cron.xml',
        'data/attendance_notification_data.xml',
        'views/res_config_settings_views.xml',

    ],
     'installable': True,
}
