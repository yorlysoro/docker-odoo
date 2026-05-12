# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountWithholdingRule(models.Model):
    _name = 'account.withholding.rule'
    _description = 'Withholding Rule'

    profile_id = fields.Many2one(
        comodel_name='account.fiscal.profile', 
        string='Fiscal Profile', 
        required=True, 
        ondelete='cascade'
    )
    company_id = fields.Many2one(
        comodel_name='res.company', 
        string='Company', 
        default=lambda self: self.env.company, 
        required=True
    )
    tax_ids = fields.Many2many(
        comodel_name='account.tax', 
        string='Withholding Taxes',
        domain=[('amount', '<=', 0)], # Sanity check: Withholdings are usually negative taxes
        help="Taxes that will be automatically applied to the invoice lines."
    )
    
    _sql_constraints = [
        ('profile_company_uniq', 'unique(profile_id, company_id)', 'Only one rule per profile and company is allowed!')
    ]
