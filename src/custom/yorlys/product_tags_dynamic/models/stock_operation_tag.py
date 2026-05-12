from odoo import fields, models


class StockOperationTag(models.Model):
    _name = 'stock.operation.tag'
    _description = 'Stock Operation Tag'
    _order = 'name'

    # Using translate=True for standard i18n support
    name = fields.Char(string='Name', required=True, translate=True)
    color = fields.Integer(string='Color Index', default=0)
    description = fields.Text(string='Description', translate=True)
    
    # Selection field avoids unnecessary M2O joins for standard operation types, improving performance
    operation_type = fields.Selection([
        ('receipt', 'Receipt'),
        ('delivery', 'Delivery'),
        ('internal', 'Internal Transfer'),
        ('mrp', 'Manufacturing')
    ], string='Operation Type', required=True, default='internal', index=True)

    product_tmpl_ids = fields.Many2many(
        comodel_name='product.template',
        relation='product_stock_operation_tag_rel',
        column1='tag_id',
        column2='product_id',
        string='Products'
    )
