# -*- coding: utf-8 -*-
{
    'name': 'Stock Priority Replenishment',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Prioritize product replenishment and automate activity generation',
    'author': 'Yorlys Oropeza',
    'website': 'https://yorlysoro.github.io/yorlysoro/',
    'license': 'AGPL-3',
    'depends': ['stock', 'mail'],
    'data': [
        'data/ir_cron_data.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
}