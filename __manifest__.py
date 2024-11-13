{
    'name': "veterinary application",
    'version': '1.0',
    'author': "Zeva Muhammad",
    'depends': ['base', 'contacts', 'hr'],
    'category': 'App',
    'description': """application for veterinary""",
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/pet_views.xml',
        'views/service_views.xml',
        'views/appointment_views.xml',
        'views/hr_employee_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],
    },
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}