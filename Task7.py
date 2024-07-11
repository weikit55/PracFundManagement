import unittest
import json
from app import app, init_db
from InvestmentFund import InvestmentFund

class InvestmentFundTest(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            init_db()

    def tearDown(self):
    
    def test_create_fund(self):
        new_fund = {
            "fund_id": "FD0001",
            "fund_name": "Testing Fund",
            "fund_manager_name": "Test Fund Manager",
            "fund_desc": "A test fund",
            "fund_nav": 1000.00,
            "performance": 10.0
        }
        response = self.app.post('/funds', data=json.dumps(new_fund), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        # Ensure the returned data matches what is inserted
        self.assertEqual(data['fund_id'], "FD0001")
        self.assertEqual(data['fund_name'], "Testing Fund")

    def test_retrieve_funds(self):
        response = self.app.get('/funds')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Ensure the returned data is a list
        self.assertIsInstance(data, list)

    def test_retrieve_fund_details(self):
        self.test_create_fund()
        response = self.app.get('/funds/FD0001')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        # Ensure the returned data belongs to the fund_id we want
        self.assertEqual(data['fund_id'], "FD0001")

    def test_update_fund_performance(self):
        self.test_create_fund()
        update_perf = {"performance": 15.0}
        response = self.app.put('/funds/FD0001', data=json.dumps(update_perf), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        response = self.app.get('/funds/FD0001')
        data = json.loads(response.data)
        # Ensure the performance got updated for the fund_id
        self.assertEqual(data['performance'], 15.0)

    def test_delete_fund(self):
        self.test_create_fund()
        response = self.app.delete('/funds/FUND123')
        self.assertEqual(response.status_code, 204)
        # Ensure the fund is really deleted
        response = self.app.get('/funds/FUND123')
        self.assertEqual(response.status_code, 404)