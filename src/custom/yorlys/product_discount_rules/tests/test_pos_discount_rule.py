# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestPosDiscountRule(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestPosDiscountRule, cls).setUpClass()
        cls.rule_model = cls.env['pos.discount.rule']

    def test_01_create_valid_rule(self):
        """ Happy Path: Create a valid rule """
        rule = self.rule_model.create({
            'name': 'Morning Discount',
            'hour_from': 8.0,
            'hour_to': 10.0,
            'discount_percentage': 10.0
        })
        self.assertTrue(rule.id, "Rule should be created successfully")

    def test_02_prevent_overlapping_rules(self):
        """ Negative Testing: Ensure overlapping rules raise an exception """
        self.rule_model.create({
            'name': 'Afternoon Discount',
            'hour_from': 14.0,
            'hour_to': 16.0,
            'discount_percentage': 15.0
        })

        # Overlaps completely inside
        with self.assertRaises(ValidationError):
            self.rule_model.create({
                'name': 'Overlap Inner',
                'hour_from': 14.5,
                'hour_to': 15.5,
                'discount_percentage': 20.0
            })

        # Overlaps on the edge
        with self.assertRaises(ValidationError):
            self.rule_model.create({
                'name': 'Overlap Edge',
                'hour_from': 13.0,
                'hour_to': 14.5,
                'discount_percentage': 5.0
            })
            
    def test_03_time_travel_prevention(self):
        """ Negative Testing: hour_from >= hour_to """
        with self.assertRaises(ValidationError):
            self.rule_model.create({
                'name': 'Paradox Discount',
                'hour_from': 18.0,
                'hour_to': 16.0,
                'discount_percentage': 10.0
            })
