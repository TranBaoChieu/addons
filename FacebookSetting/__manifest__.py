# -*- coding: utf-8 -*-
{
    'name': 'Facebook Setting',
    'category': 'Tutorials',
    'summary': 'Custom product',
    'sequence': -1,
    'description': '',
    'images': ['static/description/icon.jpg'],
    "author": "",
    "website": "https://www.mysite.com",
    "version": "17.0.0.1",
    "depends": ["base","website_sale","product"],
    'data': [
        'security/FacebookSetting_security.xml',
        'security/ir.model.access.csv',
        'views/facebook-setting.xml',
        'views/root_menu.xml',
        'views/success.xml',
        'views/error.xml',
        'views/view_partner.xml',
        'views/view_product.xml'
    ],
    'license': 'AGPL-3',
    'application': True
}
