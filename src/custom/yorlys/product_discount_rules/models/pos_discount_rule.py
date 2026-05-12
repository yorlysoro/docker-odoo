# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PosDiscountRule(models.Model):
    _name = 'pos.discount.rule'
    _description = 'POS Time-based Discount Rule'
    _order = 'hour_from asc'

    name = fields.Char(string='Rule Name', required=True)
    hour_from = fields.Float(string='Hour From', required=True, help="Start time in 24h format (e.g., 14.5 for 14:30).")
    hour_to = fields.Float(string='Hour To', required=True, help="End time in 24h format.")
    discount_percentage = fields.Float(string='Discount (%)', required=True)
    active = fields.Boolean(string='Active', default=True)

    @api.constrains('hour_from', 'hour_to', 'active', 'discount_percentage')
    def _check_valid_rule(self):
        """
        Validates time logic and prevents overlapping rules using batch queries.
        This ensures O(1) complexity per save operation instead of O(N).
        """
        for rule in self.filtered('active'):
            if rule.hour_from >= rule.hour_to:
                raise ValidationError("The 'Hour From' must be strictly less than 'Hour To'. We can't travel back in time.")
            
            if not (0.0 <= rule.discount_percentage <= 100.0):
                raise ValidationError("Discount percentage must be between 0 and 100.")

            # Search for active overlaps in DB
            domain = [
                ('id', '!=', rule.id),
                ('active', '=', True),
                ('hour_from', '<', rule.hour_to),
                ('hour_to', '>', rule.hour_from)
            ]
            if self.search_count(domain):
                raise ValidationError(f"Rule '{rule.name}' overlaps with an existing active discount rule. Overlapping is strictly forbidden.")
