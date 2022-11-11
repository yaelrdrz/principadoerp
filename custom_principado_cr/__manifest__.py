# -*- encoding: utf-8 -*-

{
    "name": "Custom Principado",
    "version": "1.0",
    "author": 'Candidroot Solutions Pvt. Ltd.',
    "summary": """
    Custom Development for Principado
    """,
    "category": "website",
    "website": "",
    "depends": ['stock','point_of_sale','account'],
    'data': [
        'views/res_users.xml',
        'security/rule_picking_type.xml',
    ],
    'qweb': [],
    "active": True,
    "installable": True,
    'assets': {
        'web.assets_backend': [
            'custom_principado_cr/static/src/js/relational_fields.js',

        ],
        'point_of_sale.assets': [
            'custom_principado_cr/static/src/scss/custom_style.scss',
        ],
    },
    'license': 'LGPL-3',
}
