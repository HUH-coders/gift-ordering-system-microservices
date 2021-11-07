import run
import unittest

class TestHelloWorld(unittest.TestCase):

    def setUp(self):
        self.app = run.app.test_client()
        self.app.testing = True

    def test_status_code(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_message(self):
        response = self.app.get('/')
        message = run.wrap_html('User Service Working')
        self.assertEqual(response.data, message)

if __name__ == '__main__':
    unittest.main()
