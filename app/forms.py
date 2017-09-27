from flask_wtf import Form, FlaskForm
from wtforms import validators, ValidationError, TextField, StringField, IntegerField, PasswordField, TextAreaField, SubmitField, RadioField, SelectField, BooleanField
from wtforms.validators import (DataRequired, ValidationError, Email,
                                Length, EqualTo)

class LoginForm(FlaskForm):
   username = TextField("username",[validators.Required()])
   password = PasswordField("password", [validators.Required()])
   submit = SubmitField("submit")
   
class RegistrationForm(FlaskForm):
    username = TextField("username", [validators.Required()])
    email = TextField("email", [validators.Required(), validators.Email()])
    password = PasswordField("password", [validators.Required()])
    submit = SubmitField("submit")

class RecipecatergoryForm(FlaskForm):
    categoryname = TextField("CategoryName",[validators.Required()])
    submit = SubmitField("submit")
    

class addrecipeForm(FlaskForm):
    name = TextField("name",[validators.Required()])
    category_id = StringField('category_id')
    submit = SubmitField("submit")

class editrecipeForm(FlaskForm):
    name = TextField("name")
    category_id = StringField('category_id')
    submit = SubmitField("submit")