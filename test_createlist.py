import unittest
import re
from flask import session
from app import app

class createlisttestcase(unittest.TestCase):
    """ Test to test the create recipe category"""
    def setUp(self):
        #creates  a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
#propagate exceptions to the test client
        self.app.testing = True

    def testcreaterecipecategoryfunctionality(self):
        #Test the create recipe catergory functionality
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                email="bsmrrachel@gmail.com",
                password="123"
                ), follow_redirects=True)

            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)
            
            sl = client.post('/createcategory', data=dict(
                categoryname="fish recipies"), follow_redirects=True)

            logged_in = session["logged_in"]
            category = session['recipe_category']
            categories = False
            for key in category:
                lists= category[key]
                if lists['categoryname']=='fish recipies':
                    categories = True
            

            #test that when post request is successful
            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv1.status_code, 200,
                "The login page was not loaded as expected")
                #test that the user is added to the session
            self.assertEqual(
                sl.status_code, 200,
                "The createcategory page was not loaded as expected")   
            self.assertNotEqual(None, logged_in,
                                "The user was not logged in")
            self.assertEqual(categories, True, 'List not created')

            #test that the categoryname is in session
            self.assertNotEqual({}, category, 'category not in session')
            
            
  
    def testcategorynamerequirred(self):
        #test that the category name is requirred
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
            username="phiona",
            email="bsmrrachel@gmail.com",
            password="123"
            ), follow_redirects=True)

            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)

            sl = client.post('/createcategory', data=dict(
                categoryname=""), follow_redirects=True)

            logged_in = session["logged_in"]
            category = session['recipe_category']
            categories = False
            for key in category:
                lists= category[key]
                if lists['categoryname']=='':
                    categories = False
            self.assertNotEqual(None, logged_in,
                                "The user was not logged in")
            self.assertEqual(categories, False, 'List not created')

            #test that the categoryname is in session
            self.assertEqual({}, category, 'category not in session')

    
if __name__ == '__main__':
    unittest.main()