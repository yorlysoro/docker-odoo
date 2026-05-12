from datetime import timedelta
from odoo import fields
from odoo.tests.common import TransactionCase

class TestCollectionAlert(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestCollectionAlert, cls).setUpClass()
        cls.rule_model = cls.env['account.collection.alert.rule']
        cls.move_model = cls.env['account.move']
        cls.partner = cls.env['res.partner'].create({'name': 'Test Partner'})

        # Create Rules
        cls.rule_high = cls.rule_model.create({
            'name': 'High Risk',
            'days_overdue': 30,
            'amount_min': 1000.0,
            'risk_level': 'high'
        })
        cls.rule_low = cls.rule_model.create({
            'name': 'Low Risk',
            'days_overdue': 10,
            'amount_min': 100.0,
            'risk_level': 'low'
        })

    def test_01_evaluate_risk_levels(self):
        """ Test the evaluation logic for risk levels """
        today = fields.Date.context_today(self.env.user)
        
        # Create an invoice matching the HIGH risk rule (35 days overdue, amount 1500)
        invoice_high = self.move_model.create({
            'move_type': 'out_invoice',
            'partner_id': self.partner.id,
            'invoice_date': today - timedelta(days=65),
            'invoice_date_due': today - timedelta(days=35),
            'invoice_line_ids': [(0, 0, {
                'name': 'Service',
                'quantity': 1,
                'price_unit': 1500.0,
            })]
        })
        invoice_high.action_post()

        # Run the cron action manually
        self.move_model._cron_evaluate_collection_risk()

        # Assertions
        self.assertEqual(invoice_high.risk_level, 'high', "Invoice should be marked as High Risk")
