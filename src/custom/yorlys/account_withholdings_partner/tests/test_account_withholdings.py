# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestAccountWithholdings(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        
        # Setup Test Data
        cls.company = cls.env.user.company_id
        cls.profile = cls.env['account.fiscal.profile'].create({'name': 'Retaining Agent'})
        cls.partner_with_profile = cls.env['res.partner'].create({
            'name': 'Test Partner With Profile',
            'fiscal_profile_id': cls.profile.id
        })
        cls.partner_without_profile = cls.env['res.partner'].create({
            'name': 'Test Partner Without Profile'
        })
        
        # Create a mock withholding tax (-10%)
        cls.tax_withholding = cls.env['account.tax'].create({
            'name': 'Withholding Tax 10%',
            'amount': -10,
            'type_tax_use': 'sale',
            'amount_type': 'percent',
        })
        
        cls.product = cls.env['product.product'].create({'name': 'Consulting Service'})

    def _create_invoice(self, partner):
        return self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.product.id,
                    'price_unit': 1000.0,
                })
            ]
        })

    def test_01_invoice_without_profile(self):
        """ Test that an invoice for a partner without profile posts normally. """
        invoice = self._create_invoice(self.partner_without_profile)
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')
        self.assertFalse(any(t.amount < 0 for t in invoice.invoice_line_ids.tax_ids), "Should not have withholding taxes")

    def test_02_invoice_with_profile_missing_rule(self):
        """ Test boundary case: Profile exists but no rule defined. Should raise UserError. """
        invoice = self._create_invoice(self.partner_with_profile)
        with self.assertRaisesRegex(UserError, "there is no withholding rule configured"):
            invoice.action_post()

    def test_03_invoice_with_profile_and_rule(self):
        """ Test automatic tax application upon posting. """
        # Create Rule
        self.env['account.withholding.rule'].create({
            'profile_id': self.profile.id,
            'company_id': self.company.id,
            'tax_ids': [(6, 0, [self.tax_withholding.id])]
        })
        
        invoice = self._create_invoice(self.partner_with_profile)
        invoice.action_post()
        
        self.assertEqual(invoice.state, 'posted')
        self.assertIn(self.tax_withholding, invoice.invoice_line_ids.tax_ids, "Withholding tax must be automatically applied.")
