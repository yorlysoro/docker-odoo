# -*- coding: utf-8 -*-
from odoo import models, api, fields
from odoo.exceptions import UserError
import datetime

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.model_create_multi
    def create(self, vals_list):
        """
        Intercepts POS order creation to validate if discounts applied in frontend
        match the backend active rules. We use batch processing.
        """
        # Fetch rules once for the whole batch
        active_rules = self.env['pos.discount.rule'].search([('active', '=', True)])
        
        for vals in vals_list:
            order_date = vals.get('date_order') or fields.Datetime.now()
            # Convert datetime to float hours in local time
            if isinstance(order_date, str):
                order_date = fields.Datetime.from_string(order_date)
            
            user_tz = self.env.user.tz or 'UTC'
            local_time = fields.Datetime.context_timestamp(self, order_date)
            current_hour = local_time.hour + (local_time.minute / 60.0)

            # Find applicable rule
            applicable_rule = active_rules.filtered(
                lambda r: r.hour_from <= current_hour < r.hour_to
            )

            # Check lines for unauthorized discounts
            if 'lines' in vals:
                for line in vals['lines']:
                    line_data = line[2] if len(line) == 3 else {}
                    applied_discount = line_data.get('discount', 0.0)
                    
                    if applied_discount > 0.0 and not applicable_rule:
                        # Log it, but don't crash the POS sync unless strict auditing is required.
                        # For this spec, we will enforce it strictly.
                        raise UserError("A discount was applied outside of the allowed Happy Hour timeframe. Nice try.")

        return super().create(vals_list)
