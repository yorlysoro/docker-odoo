# -*- coding: utf-8 -*-
{
    'name': 'POS Discount Rules',
    'version': '18.0.1.0.0',
    'category': 'Sales/Point of Sale',
    'summary': 'Automatic POS discounts based on time slots',
    'author': 'Yorlys Oropeza',
    'website': 'https://yorlysoro.github.io/yorlysoro/',
    'license': 'AGPL-3',
    'depends': ['point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/pos_discount_rule_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'product_discount_rules/static/src/js/discount_rule.js',
        ],
    },
    'installable': True,
    'application': False,
}