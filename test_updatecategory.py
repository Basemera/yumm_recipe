import unittest
import re
from flask import session
from app import app

class viewcategorytestcase(unittest.TestCase):
    """ Test to test the view the categories"""
    def setUp(self):
        #creates  a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
#propagate exceptions to the test client
        self.app.testing = True

    def testupdatelistfunctionality(self):
        #Test the update functionality
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
            created = False
            for key in category:
                lists= category[key]
                if lists['categoryname']=='fish recipies':
                    lists['categoryname']='new'
                if lists['categoryname']== 'new' and lists['categoryname'] != 'fish recipies':
                    created = True
            

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
            self.assertEqual(created, True, 'List not created')

            #test that the username is in session
            self.assertNotEqual({}, category, 'category not in session')
            self.assertEqual(created, True, 'category not updated')
            
            
  
    def testcategorynamerequirred(self):
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
            username="phiona",
            email="phiona@gmail.com",
            password="123"
            ), follow_redirects=True)

            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)

            sl = client.post('/createcategory', data=dict(
                categoryname="fish"), follow_redirects=True)

            logged_in = session["logged_in"]
            category = session['recipe_category']
            updated = False
            for key in category:
                lists= category[key]
                if lists['categoryname']=='fish':
                    lists['categoryname']=''
                if lists['categoryname']=='fish':
                    updated = False
            self.assertNotEqual(None, logged_in,
                            "The user was not logged in")
            self.assertNotEqual({}, category, 'list created')
            self.assertNotEqual(updated, True, 'List erroneosly updated')

    
if __name__ == '__main__':
    unittest.main()