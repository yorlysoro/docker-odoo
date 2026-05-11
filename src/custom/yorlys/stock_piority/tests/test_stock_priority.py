# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestStockPriority(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockPriority, cls).setUpClass()
        cls.product = cls.env['product.template'].create({
            'name': 'Test CPU',
            'type': 'consu',
            'replenishment_priority': 'high',
            'target_stock': 50.0,
            'is_storable': True,
        })
        # Simulate inventory level
        cls.env['stock.quant']._update_available_quantity(cls.product.product_variant_id, cls.env.ref('stock.stock_location_stock'), 10.0)

    def test_01_activity_creation(self):
        """ Test that activities are created when stock is below target """
        self.env['product.template']._cron_evaluate_replenishment_priority()
        
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'product.template'),
            ('res_id', '=', self.product.id)
        ])
        
        self.assertTrue(activities, "An activity should have been created for the product.")
        self.assertEqual(len(activities), 1, "Only one activity should be created per user.")
        self.assertTrue(self.product.needs_replenishment, "Product should be marked as needing replenishment.")

    def test_02_prevent_duplicate_activities(self):
        """ Test that duplicate activities are prevented """
        # Run cron twice
        self.env['product.template']._cron_evaluate_replenishment_priority()
        self.env['product.template']._cron_evaluate_replenishment_priority()
        
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'product.template'),
            ('res_id', '=', self.product.id)
        ])
        
        # It should still be exactly 1 despite running the cron twice
        self.assertEqual(len(activities), 1, "Duplicate activities were generated. Fix your domain!")
