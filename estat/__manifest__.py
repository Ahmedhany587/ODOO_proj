{
    'name': 'Real Estate Management',
    'version': '1.0',
    'summary': 'Manage properties, listings, and sales for real estate businesses',
    'description': """
        Real Estate Management Module
        =============================

        This module helps manage real estate properties, listings, sales, and leases. Features include:
        - Property listings
        - Property sales and leases
        - Customer and agent management
        - Property visits and appointments
    """,
    'category': 'Real Estate',
    'author': 'Quadova',
    'website': 'https://quadova.com/',
    'license': 'AGPL-3',
    'depends': ['base', 'sale', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_buyer_views.xml',
        'views/estate_seller_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_seller_views_inherited.xml',
        'views/estate_property_kanban_views.xml',

    ],
    'demo': [
        'demo/property_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
