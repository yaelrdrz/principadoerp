# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Import Products From Excel File",

    'summary': """ Import Products From Excel File """,
    'version': '15.0.0.1',
    'description': """
Description
-----------
    - Import Products From Excel File
    """,
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': "https://candidroot.com/",
    'category': 'Tools',
    'depends': ['product','product_unspsc'],
    "data": [
        'security/ir.model.access.csv',
        'wizard/product_xls_import.xml',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False
}
