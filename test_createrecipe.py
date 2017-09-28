import unittest
import re
from flask import session
from app import app

class createrecipetestcase(unittest.TestCase):
    """ Test to test the create recipe"""
    def setUp(self):
        #creates  a test client
        self.app = app.test_client()
        app.config['WTF_CSRF_ENABLED'] = False
#propagate exceptions to the test client
        self.app.testing = True

    def testcreaterecipemfunctionality(self):
        #Test the create item functionality
        with app.test_client() as client:
            rv = client.post('/signup', data=dict(
                username="phiona",
                email="phionae@gmail.com",
                password="123"
                ), follow_redirects=True)

            rv1 = client.post('/signin', data=dict(
                username="phiona",
                password="123"), follow_redirects=True)
            
            sl = client.post('/createcategory', data=dict(
                listname="fish"), follow_redirects=True)

            it = client.post('/addrecipe<category_id>', data = dict(name = 'fish steak', 
                                        category_id = 1), follow_redirects=True)

            logged_in = session["logged_in"]
            category = session['recipe_category']
            recipes = session ['recipes']
            added = False
            for key in recipes:
                recipe = recipes[key]
                if recipe['name']=='fish steak':
                    added = True
                    break
            

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
            self.assertEqual(
                it.status_code, 200,
                "The createrecipem page was not loaded as expected") 
            self.assertNotEqual(None, logged_in,
                                "The user was not logged in")
            self.assertEqual(added, True, 'recipe not created')

            #test that the username is in session
            self.assertNotEqual({}, recipes, 'recipe not in session')
            
            
  
    def testupdaterecipename(self):
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

            it = client.post('/addrecipe<category_id>', data = dict(name = 'fish', 
                                        category_id = 1), follow_redirects=True)

            recipes= session['recipes']
            recipe_updated = False
            for key in recipes:
                recipe = recipes[key]
                if recipe['name'] == 'fish':
                    recipe['name'] = 'new'
                    if recipe['name']=='new' and recipe['name']!='fish':
                        recipe_updated = True
                        break
                    

            self.assertEqual(recipe_updated, True, 'recipe not updated')


    def deleterecipe(self):
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

            it = client.post('/addrecipe<category_id>', data = dict(name = '', 
                                        category_id = 1), follow_redirects=True)

            recipes= session['recipes']
            recipe_deleted = False
            for key in recipes:
                recipe = recipes[key]
                if recipe['name'] == 'fish':
                    del recipe['name']
                    if recipe['name']!='fish':
                        recipe_deleted = True
                        break
                    

            self.assertEqual(recipe_deleted, True, 'recipe not updated')
 

    
if __name__ == '__main__':
    unittest.main()