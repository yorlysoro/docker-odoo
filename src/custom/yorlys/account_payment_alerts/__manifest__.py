{
    'name': 'Account Payment Alerts',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Collection risk evaluation and dashboards for overdue invoices',
    'author': 'Yorlys Oropeza',
    'website': 'https://yorlysoro.github.io/yorlysoro/',
    'license': 'AGPL-3',
    'depends': ['account'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_cron.xml',
        'views/account_collection_alert_rule_views.xml',
        'views/account_move_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}