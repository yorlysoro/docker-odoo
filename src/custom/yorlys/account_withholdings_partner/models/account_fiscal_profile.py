# -*- coding: utf-8 -*-
from odoo import models, fields

class AccountFiscalProfile(models.Model):
    _name = 'account.fiscal.profile'
    _description = 'Fiscal Profile'

    name = fields.Char(string='Profile Name', required=True, translate=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string='Description')
