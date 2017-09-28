import unittest
from app import app


class pagesthatloadminussignin(unittest.TestCase):
    """Test to make sure the homepage is accessible without logging in"""
    def setUp(self):
        self.app = app.test_client()
    def testindex(self):
        """Test that homepage shows up even when not signed in"""
        rv = self.app.get('/')
        self.assertEqual(rv.status_code, 302, "homepage didnot load")
    def testsignin(self):
        """Test that log in shows up even when not signed in"""
        rv = self.app.get('/signin')
        self.assertEqual(rv.status_code, 200, "log in page didnot load as expected")
    def testsignup(self):
        """Test that signup shows up even when not signed in"""
        rv = self.app.get('/signup')
        self.assertEqual(rv.status_code, 200, "signup page did not load as expected")

    def testviewlist(self):
        """Test that viewlist does not show when not signed in"""
        rv = self.app.get('/viewcategory')
        self.assertEqual(rv.status_code, 302, "viewlist page should not load unless signed in")

    def testcreatelist(self):
        """Test that createlist does not show when not signed in"""
        rv = self.app.get('/createcategory')
        self.assertEqual(rv.status_code, 302, "createlist page should not load unless signed in")


if __name__ == '__main__':
    unittest.main()

