import os, base64
from flask import session, request
from werkzeug.security import generate_password_hash


class Abstract:
    """A parent class where session ids will be created"""
    def generate_id(self, session_key):
        """Method for generating unique session ids"""
        generated_id = os.urandom(10).hex()
        while generated_id in session[session_key]:
            generated_id = os.urandom(10).hex()
        return generated_id

class User(Abstract):
    """A class to define a store a user object"""
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.userid = self.generate_id('users')
        

class recipe_category(Abstract):
    """A class to define and store a recipe category object"""
    def __init__(self, categoryname):
        self.categoryname = categoryname
        self.category_id = self.generate_id('recipe_category')
        self.userid = session['logged_in']['userid']

class recipe(recipe_category):
    """A class to define and store a recipe object"""
    def __init__(self, name, category_id):
        self.name =name
        self.category_id = category_id
        recipe_category.category_id = category_id
        self.recipe_id = self.generate_id('recipes')
        self.userid = session['logged_in']['userid']