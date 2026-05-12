# -*- coding: utf-8 -*-
{
    'name': 'Account Withholdings Partner',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Automatic tax withholdings based on partner fiscal profile',
    'author': 'Yorlys Oropeza',
    'website': 'https://yorlysoro.github.io/yorlysoro/',
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_fiscal_profile_views.xml',
        'views/account_withholding_rule_views.xml',
        'views/res_partner_views.xml',
    ],
    'installable': True,
    'application': False,
}