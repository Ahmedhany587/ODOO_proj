{
    'name': "Employee Performance Review",
    'version': '1.0',
    'summary': "Manage employee performance reviews",
    'description': """Long description part""",
    'category': 'Human Resources',
    'author': "Quadova",
    'license': 'AGPL-3',
    'website': "https://www.Quadova.com",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'security/performance_review_security.xml',
        'views/performance_review_views.xml',
        'views/performance_review_menu.xml',
        'data\performance_review_data.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
