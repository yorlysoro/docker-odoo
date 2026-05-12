# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    fiscal_profile_id = fields.Many2one(
        comodel_name='account.fiscal.profile', 
        string='Fiscal Profile',
        help="Determines the automatic withholdings applied to this partner."
    )
