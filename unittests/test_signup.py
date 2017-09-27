import unittest
from flask import session
from app import app

class testsignupfunctionality(unittest.TestCase):
    #test the functionality of signup
    def setUp(self):
        #creates  a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
#propagate exceptions to the test client
        self.app.testing = True

    def testsignupfunctionality(self):
        #Test the signup functionality
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                password="123",
                email="bsmrrachel@gmail.com"
                ), follow_redirects=True)

            logged_in = session["logged_in"]
            users = session['users']
            created = False
            for k in users:
                user = users[k]
                if user["username"] == "phiona":
                    created = True
                    break

                self.assertEqual(rv.status_code, 200, "signup page not loaded as expected")
                self.assertEqual(None, logged_in, "user not logged in")
                self.assertNotEqual(users, {}, 'user not in session')
                self.assertEqual(created, True, 'user not created')

    def testusernamerequired(self):
        #test that username is requirred at signup
      with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="",
                password="123",
                email="bsmrrachel@gmail.com"
                ), follow_redirects=True)

            
            users = session['users']
            created = False
            for k in users:
                user = users[k]
                if user["email"] == "bsmrrachel@gmail.com":
                    created = True
                    break
            self.assertEqual(users, {}, 'user not in session')
            self.assertEqual(created, False, "user created without a username")

    def testpasswordrequirred(self):
        #test that password is requirred
       with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                password="",
                email="vincenthokie@gmail.com"
                ), follow_redirects=True)
                
            users = session['users']
            created = False
            for k in users:
                user = users[k]
                if user["email"] == "bsmrrachel@gmail.com":
                    created = True
                    break
            self.assertEqual(users, {}, 'user not in session')
            self.assertEqual(created, False, "user created without a password")

 
  
    def emailrequirred(self):
        #test that the email is requirred
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                password="123",
                email=""
                ), follow_redirects=True)

            users = session['users']
            created = False
            for k in users:
                user = users[k]
                if user["username"] == "phiona":
                    created = True
                    break

            self.assertEqual(users, {}, 'user not in session')
            self.assertEqual(created, False, "user created without an email")


if __name__ == '__main__':
    unittest.main()
        