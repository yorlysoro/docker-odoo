from odoo.tests.common import TransactionCase
from odoo.exceptions import AccessError

class TestStockOperationTag(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super(TestStockOperationTag, cls).setUpClass()
        # Setup environment and test records
        cls.tag_model = cls.env['stock.operation.tag']
        cls.product_model = cls.env['product.template']
        
        cls.test_tag = cls.tag_model.create({
            'name': 'Fragile',
            'operation_type': 'delivery',
            'color': 2
        })
        
        cls.test_product = cls.product_model.create({
            'name': 'Glass Vase',
            'type': 'consu',
            'is_storable': True
        })

    def test_01_tag_creation(self):
        """ Test if the tag is created correctly and values match """
        self.assertTrue(self.test_tag, "Tag was not created")
        self.assertEqual(self.test_tag.operation_type, 'delivery')

    def test_02_assign_tag_to_product(self):
        """ Test the M2M assignment to avoid cache/ORM issues """
        # Assign tag
        self.test_product.write({
            'stock_operation_tag_ids': [(4, self.test_tag.id)]
        })
        # Check relation
        self.assertIn(self.test_tag, self.test_product.stock_operation_tag_ids)

    def test_03_kanban_grouping_read_group(self):
        """ Simulate the kanban group by to ensure no N+1 traceback """
        # Assign tag
        self.test_product.write({
            'stock_operation_tag_ids': [(4, self.test_tag.id)]
        })
        
        # Test read_group which Kanban uses under the hood
        result = self.product_model.read_group(
            domain=[('id', '=', self.test_product.id)],
            fields=['stock_operation_tag_ids'],
            groupby=['stock_operation_tag_ids']
        )
        self.assertTrue(len(result) > 0, "read_group failed on M2M field")
