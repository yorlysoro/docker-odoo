# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    replenishment_priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Replenishment Priority', default='low', 
       help="Defines the operational criticality for restocking this product.")

    target_stock = fields.Float(
        string='Target Stock', 
        default=0.0,
        help="If available quantity falls below this threshold, an activity is triggered."
    )

    needs_replenishment = fields.Boolean(
        string='Needs Replenishment',
        readonly=True,
        store=True,
        help="Technical field updated by cron to optimize list views."
    )

    @api.model
    def _cron_evaluate_replenishment_priority(self):
        """
        Batch processing method to evaluate stock levels and generate activities.
        Avoids N+1 queries by pre-fetching data and grouping creations.
        """
        # Fetch only products that actually have a target stock to optimize memory
        products = self.search([
            ('type', '=', 'consu'), 
            ('target_stock', '>', 0)
        ])
        
        if not products:
            return

        activity_model = self.env['mail.activity']
        res_model_id = self.env.ref('product.model_product_template').id
        
        # Get Stock Managers. Fallback to admin if group is empty.
        stock_manager_group = self.env.ref('stock.group_stock_manager', raise_if_not_found=False)
        managers = stock_manager_group.users if stock_manager_group and stock_manager_group.users else self.env.user

        # Fetch existing open activities for these products to prevent duplicates
        existing_activities = activity_model.search([
            ('res_model_id', '=', res_model_id),
            ('res_id', 'in', products.ids),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
        ])
        products_with_activity = existing_activities.mapped('res_id')

        activities_to_create = []
        products_to_mark = self.env['product.template']
        products_to_unmark = self.env['product.template']

        # Evaluate logic in memory
        for product in products:
            if product.qty_available < product.target_stock:
                products_to_mark |= product
                if product.id not in products_with_activity:
                    for manager in managers:
                        activities_to_create.append({
                            'res_id': product.id,
                            'res_model_id': res_model_id,
                            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                            'summary': f'Critical Replenishment: {product.name}',
                            'note': f'<p>Priority: <strong>{product.replenishment_priority.upper()}</strong></p>'
                                    f'<p>Current stock ({product.qty_available}) is below target ({product.target_stock}).</p>',
                            'user_id': manager.id,
                        })
            else:
                products_to_unmark |= product

        # Batch create activities and update markers
        if activities_to_create:
            activity_model.create(activities_to_create)
            _logger.info("Created %s replenishment activities.", len(activities_to_create))

        if products_to_mark:
            products_to_mark.write({'needs_replenishment': True})
        if products_to_unmark:
            products_to_unmark.write({'needs_replenishment': False})
