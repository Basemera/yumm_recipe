import unittest
import re
from flask import session
from app import app

class logintestcase(unittest.TestCase):
    """ Test to test the login"""
    def setUp(self):
        #creates  a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
#propagate exceptions to the test client
        self.app.testing = True

    def testloginfunctionality(self):
        #Test the login functionality
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                email="bsmrrachel@gmail.com",
                password="123"
                ), follow_redirects=True)

            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)

            logged_in = session["logged_in"]
            user_loggedin = session['logged_in']['username']
            users = session['users']
            user = users.items()
            

            #test that when post request is successful
            self.assertEqual(
                rv.status_code, 200,
                "The sign up page was not loaded as expected")
            self.assertEqual(
                rv1.status_code, 200,
                "The login page was not loaded as expected")
                #test that the user is added to the session
            self.assertNotEqual(None, logged_in,
                                "The user was not logged in")

            #test that the username is in session
            self.assertEqual('phiona', user_loggedin, 'username not in session')
            
            
  
    def testusernamerequirred(self):
        #test that the username is requrred at log in
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
            username="phiona",
            email="bsmrrachel@gmail.com",
            password="123"
            ), follow_redirects=True)
            rv1 = client.post('/signin', data=dict(
                username="",
                password="123"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(None, logged_in,
                            "The user was erroneosly in")

    def testpasswordrequirred(self):
        #test that password is requrred
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
            username="phiona",
            email="bsmrrachel@gmail.com",
            password="123"
            ), follow_redirects=True)
            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password=""), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(None, logged_in,
                            "The user was erroneusly logged in")
            #test that signin page is reloaded
            self.assertEqual(rv1.status_code, 200, "signin page didnot load as expected" )

    def testinvalidcredentials(self):
        #test make sure users cannot login with incorrect credentials
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
            username="phiona",
            email="bsmrrachel@gmail.com",
            password="123"
            ), follow_redirects=True)
            rv1 = client.post('/signin', data=dict(
                username="stella",
                password="456"), follow_redirects=True)

            logged_in = session["logged_in"]

            self.assertEqual(None, logged_in,
                            "The user was erroneusly logged in")

           
            #test that signin page is reloaded
            self.assertEqual(rv1.status_code, 200, "signin page didnot load as expected" )
           
    def testredirectstoviewlist(self):
        #test that successful login redirects to viewlist
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                email="bsmrrachele@gmail.com",
                password="123"
                ), follow_redirects=True)

            rv1 = client.post('/viewcategory', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)

            #test that redirect to viewlist
            self.assertEqual(rv1.status_code, 200, 'doesnot load viewlist')

if __name__ == '__main__':
    unittest.main()