import os
from flask import Flask, request, render_template, flash, redirect, url_for, get_flashed_messages, session, abort
from .forms import LoginForm, RegistrationForm, RecipecatergoryForm, addrecipeForm
from . import app
from app.modals import User, recipe_category, recipe, Abstract

def create_session_keys():
    if "users" not in session:
        session["users"] = {}
    if "recipe_category" not in session:
        session["recipe"] = {}

    if "recipes" not in session:
        session["items"] = {}

    if "logged_in" not in session:
        session["logged_in"] = None 


def user_redirect():
    """A method to prevent logged in users from log in and sign up pages"""
    if "logged_in" in session and session["logged_in"] is not None:
        flash({
            "message":
            "You have already logged in!"
        })
        return True
    else:
        return False

def guest_redirect():
    """A method to ensure users log in before proceeding"""
    if "logged_in" in session and session["logged_in"] is None:
        flash({
            "message":
            "Please log in to proceed"
        })
        return True
    else:
        return False


@app.route('/', methods= ['GET', 'POST'])
def index():
    """creates a homepage"""
    create_session_keys()
    if request.method=='GET':
        return render_template('homepage.html')
    
    elif "users" in session:
        return redirect(url_for('viewcategory'))
    else:
        return render_template('homepage.html')
    


@app.route('/signup', methods= ['GET', 'POST'])
def signup():
    """Method to sign users up"""
    if user_redirect():
        return redirect(url_for('viewcategory')) #if user already logged in notify user
    
    create_session_keys()

    form = RegistrationForm() #registering the user

    if request.method == 'POST':
        if form.validate_on_submit():
            
            new_user = User(form.username.data, form.password.data, form.email.data)
            session["users"][new_user.userid] = vars(new_user)
            flash({"message": "You have successfully signed up! Login to continue"})

            return redirect('/signin')

        return render_template("signup.html",
                               title='Create Profile',
                               form=form)               
    elif request.method == 'GET':
        return render_template('signup.html', 
                           title='Sign up',
                           form=form)
    


@app.route('/signin', methods= ['GET', 'POST'])
def signin():
    """Method to sign users in"""
    if user_redirect():
        return redirect(url_for('viewcategory')) #if user already logged in notify user
    
    create_session_keys()
    
    form = LoginForm()
    form_reg = RegistrationForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            users = session["users"]
            lists = users.items()
            
            for key in users:
                
                user = users[key]
                
                session['logged_in'] = {'username':form.username.data, 'userid': user['userid']}
                return redirect(url_for('viewcategory'))
                flash({"message": 'You are not signed up please sign up to continue'})
            
        flash({"message":'Login failed! incorrect credentials. Please sign up to continue'})
        return redirect(url_for('signup'))
    
    elif request.method == 'GET':
        return render_template('signin.html', title = 'log in', form = form, form_reg = form_reg)

@app.route('/logout', methods= ['GET', 'POST'])
def logout():
    """Method to log out users"""
    if guest_redirect():
        return redirect(url_for("signin"))

    create_session_keys()
    session["logged_in"] = None

    flash({
            "message":
            'You have successfully logged out!'
        })

    return redirect(url_for ('signin'))

@app.route('/homepage', methods= ['GET', 'POST'])
def homepage():
    create_session_keys()
    return render_template('homepage.html')

@app.route('/createcategory', methods= ['GET', 'POST'])
def createcategory():
    """method to create a recipe category"""
    create_session_keys()
    if guest_redirect():
        flash({"message": "You need to sign in to continue"})
        return redirect(url_for("signin"))
    form = RecipecatergoryForm()

    if form.validate_on_submit():
        newcategory = recipe_category(form.categoryname.data)
        session["recipe_category"][newcategory.category_id] = vars(newcategory)
        flash({"message": "You have successfully created a recipe category! Select it to start adding items to it"})
        return redirect(url_for('viewcategory'))
    return render_template('createcategory.html', form = form)

@app.route('/updatecategory/<category_id>', methods= ['GET', 'POST'])
def updatecategory(category_id):
    """method to update a recipe category"""
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = RecipecatergoryForm()

    if form.validate_on_submit():
        session['recipe_category'][category_id]['categoryname'] = form.categoryname.data
        flash('message: Update successful')
        return redirect(url_for('viewcategory'))
    category = session['recipe_category'][category_id]

    return render_template('updatecategory.html', form = form, 
                                            categoryname = category['categoryname'],
                                            category_id = category_id )
    
@app.route('/deletecategory/<category_id>', methods= ['GET', 'POST'])    
def deletecategory(list_id):
    """methid to delete a recipe category"""
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = RecipecatergoryForm()
    if form.validate_on_submit():
        session['recipe_category'][category_id]['categoryname'] = form.categoryname.data
        del session['recipe_category'][category_id]
        flash('message: delete successful')
        return redirect(url_for('viewcategory'))
    category = session['recipe_category'][category_id]

    return render_template('deletelist.html', form = form, 
                                            categoryname = category['categoryname'],
                                            category_id = category_id )
    
    

@app.route('/viewcategory', methods= ['GET', 'POST'])
def viewcategory():
    """method to view recipe categories and recipes"""
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))

    form = RecipecatergoryForm()
    form_recipe = addrecipeForm()

    return render_template("viewcategory.html",
                           title='View recipe categories',
                           category=session["recipe_category"],
                            recipe = session["recipes"],
                           form=form,
                           user=session["logged_in"]["userid"],
                           form_item = form_item)

@app.route('/addrecipe<id>', methods= ['GET', 'POST'])
def addrecipe(id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))

    form = addrecipeForm()
    
    if form.validate_on_submit():
        
        new_recipe = recipe(form.name.data, id)
        
        session["recipes"][new_recipe.recipe_id] = vars(new_recipe)
        
        flash({"message":
                "recipe successfully added"})
        return redirect(url_for('viewcategory'))

    return render_template('addrecipe.html', form = form, category_id = id, recipes = session["recipes"])


@app.route('/updaterecipe/<recipe_id>', methods= ['GET', 'POST'])
def updateitem(recipe_id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = additemsForm()

    if form.validate_on_submit():
        session['recipes'][recipe_id]['name'] = form.name.data
        flash('message: Update successful')
        return redirect(url_for('viewcategory'))
    recipes = session['recipes'][recipe_id]

    return render_template('updateitem.html', form = form, 
                                            name = recipes['name'],
                                            recipe_id = recipe_id )

@app.route('/deleterecipe/<recipe_id>', methods= ['GET', 'POST'])
def deleterecipe(recipe_id):
    create_session_keys()
    if guest_redirect():
        return redirect(url_for("signin"))
    form = additemsForm()

    if form.validate_on_submit():
        session['recipes'][recipe_id]['name'] = form.name.data
        del session['recipes'][recipe_id]
        flash('message: Delete successful')
        return redirect(url_for('viewcategory'))
    recipes = session['recipes'][recipe_id]

    return render_template('updateitem.html', form = form, 
                                            name = recipes['name'],
                                            recipe_id = recipe_id )

