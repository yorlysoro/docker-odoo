from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # Prefetch is True by default, but we declare it for semantic clarity.
    stock_operation_tag_ids = fields.Many2many(
        comodel_name='stock.operation.tag',
        relation='product_stock_operation_tag_rel',
        column1='product_id',
        column2='tag_id',
        string='Operation Tags',
        help='Tags used for warehouse routing and picking priority'
    )

    @api.model
    def action_assign_operation_tags(self):
        """
        Server action to trigger a quick wizard or multi-edit.
        In Odoo 18, returning an action window to update records in batch is best.
        """
        # Security check: ensures user has rights before invoking action
        self.check_access('write')
        
        # Here we could call a specific wizard if complex logic is needed.
        # For standard tag management, the list view editable handles it.
        pass
