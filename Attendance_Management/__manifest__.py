{
    'name': 'Attendance Management',
    'version': '2.0',
    'summary': 'Manage Employee Attendance',
    'description': """
        Custom module to manage employee attendance in Odoo. This module allows HR managers to:
        - Record attendance
        - Track employee working hours
        - Generate attendance reports
    """,
    'category': 'Human Resources',
    'author': 'Quadova',
    'website': 'https://www.yourcompany.com',
    'license': 'AGPL-3',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_attendance_views.xml',
        'views/employee_attendance_menu.xml',
        'report/employee_attendance_report.xml'




    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
