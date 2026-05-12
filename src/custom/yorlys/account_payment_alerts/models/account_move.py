from datetime import timedelta
from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    # Stored field to allow grouping in UI natively without killing the database
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Collection Risk Level', readonly=True, copy=False, index=True)

    @api.model
    def _cron_evaluate_collection_risk(self):
        """
        Scheduled action to evaluate and update risk levels using Batch Processing.
        Prevents N+1 queries by relying on ORM search and bulk write.
        """
        rules = self.env['account.collection.alert.rule'].search([])
        if not rules:
            return

        # Define priority map: We want to apply High risk rules first so they take precedence
        risk_weights = {'high': 3, 'medium': 2, 'low': 1}
        
        # Sort rules dynamically based on priority weight
        sorted_rules = sorted(
            rules, 
            key=lambda r: (risk_weights.get(r.risk_level, 0), r.days_overdue, r.amount_min), 
            reverse=True
        )

        today = fields.Date.context_today(self)
        
        # Fetch all candidate invoices (open, posted, customer invoices)
        candidate_domain = [
            ('state', '=', 'posted'),
            ('payment_state', 'in', ('not_paid', 'partial')),
            ('move_type', '=', 'out_invoice'),
        ]
        invoices_to_process = self.search(candidate_domain)
        
        # Reset current risk levels in batch
        invoices_to_process.write({'risk_level': False})

        assigned_invoice_ids = set()

        for rule in sorted_rules:
            # Calculate the target due date threshold
            target_date = today - timedelta(days=rule.days_overdue)
            
            # Use ORM to find matching invoices skipping those already assigned a higher risk
            rule_domain = [
                ('id', 'in', invoices_to_process.ids),
                ('id', 'not in', list(assigned_invoice_ids)),
                ('invoice_date_due', '<=', target_date),
                ('amount_residual', '>=', rule.amount_min)
            ]
            
            matching_invoices = self.search(rule_domain)
            
            if matching_invoices:
                # Bulk update to avoid N+1 issues
                matching_invoices.write({'risk_level': rule.risk_level})
                assigned_invoice_ids.update(matching_invoices.ids)
