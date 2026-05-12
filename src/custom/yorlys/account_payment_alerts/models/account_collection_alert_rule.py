from odoo import fields, models


class AccountCollectionAlertRule(models.Model):
    _name = 'account.collection.alert.rule'
    _description = 'Collection Alert Rule'
    _order = 'amount_min desc, days_overdue desc'

    name = fields.Char(string='Rule Name', required=True, translate=True)
    days_overdue = fields.Integer(
        string='Days Overdue', 
        required=True, 
        help='Minimum days after the due date to trigger this rule.'
    )
    # Using currency_id for multicurrency support consistency
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )
    amount_min = fields.Monetary(
        string='Minimum Amount', 
        required=True,
        help='Minimum residual amount to trigger this rule.'
    )
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Risk Level', required=True, default='low')
