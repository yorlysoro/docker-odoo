# -*- coding: utf-8 -*-
from odoo import models

class PosSession(models.Model):
    _inherit = 'pos.session'

    def _pos_data_process(self, loaded_data):
        """
        Injects the discount rules into the POS loading process.
        """
        super()._pos_data_process(loaded_data)
        rules = self.env['pos.discount.rule'].search_read(
            [('active', '=', True)], 
            ['name', 'hour_from', 'hour_to', 'discount_percentage']
        )
        loaded_data['pos.discount.rule'] = rules

    def _pos_ui_models_to_load(self):
        """1. Le decimos al POS que cargue nuestro nuevo modelo"""
        result = super()._pos_ui_models_to_load()
        result.append('pos.discount.rule')
        return result

    def _loader_params_pos_discount_rule(self):
        """2. Definimos qué campos y dominio queremos traer"""
        return {
            'search_params': {
                'domain': [('active', '=', True)],
                'fields': ['name', 'hour_from', 'hour_to', 'discount_percentage'],
            }
        }

    def _get_pos_ui_pos_discount_rule(self, params):
        """3. Ejecutamos la consulta y enviamos la data al frontend"""
        return self.env['pos.discount.rule'].search_read(**params['search_params'])
