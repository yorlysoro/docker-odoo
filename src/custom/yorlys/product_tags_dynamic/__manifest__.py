{
    'name': 'Dynamic Product Tags',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Operational tags classification for products to optimize logistics',
    'author': 'Yorlys Oropeza',
    'website': 'https://yorlysoro.github.io/yorlysoro/',
    'license': 'AGPL-3',
    'depends': ['stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_operation_tag_views.xml',
        'views/product_template_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}