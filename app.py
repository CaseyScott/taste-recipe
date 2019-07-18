import os
import json
import pymongo
from flask import Flask, render_template, redirect, request, url_for,session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

#config.py file set to ignore by gitignore.
#config vars set up in heroku
if app.debug == True:
    import config
    app.config["MONGO_DBNAME"] = config.DB_CONFIG["MONGO_DBNAME"]
    app.config["MONGO_URI"] = config.DB_CONFIG["MONGO_URI"]
    app.secret_key = config.DB_CONFIG['SECRET_KEY']
else:
    app.secret_key = os.environ.get('SECRET_KEY')
    app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
    app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('home.html')

#----------------------------------------------------Registion Form  
def registration_form():
    data = {
        "username": request.form.get('register_username'),
        "password": request.form.get('register_password')
    }
    return data

"""if the passwords don't match or username already exists, return the user to the home page.
If successful, a session['user'] variable is set to that username.
Register form information is sent to the collection in Mongo database."""

@app.route('/register', methods=['POST'])
def register():
    requested_username = request.form.get("register_username")
    new_password = request.form.get("register_password")
    comfirm_password = request.form.get("comfirm_password")

    if comfirm_password == new_password:
        try:
            existing_user = mongo.db.user_details.find_one(
                {'username': requested_username}, {"username"})

            if existing_user is None:

                mongo.db.user_details.insert_one(registration_form())
                session['user'] = requested_username
                return redirect(
                    url_for(
                        'my_recipes',
                        username=requested_username))
            else:
                return redirect(request.referrer)

        except BaseException:
            return redirect(request.referrer)

    else:
        return redirect(request.referrer)

#----------------------------------------------------Registion Form

#-------------------------------------------------------Sign In Form
""" verifies that the posted username and password from the sign in form
matches the username and password stored in the database.
Upon a successful sign in, a session['user'] variable is set to what the
form username is."""

@app.route('/signin', methods=['POST'])
def signin():

    username = request.form.get('signin_username')
    password = request.form.get('signin_password')

    try:
        user_doc_username = mongo.db.user_details.find_one(
            {'username': username}, {'username'})
        user_doc_password = mongo.db.user_details.find_one(
            {'username': username}, {'password'})

        stored_username = find_value(user_doc_username)  # FUNCTION 1
        stored_password = find_value(user_doc_password)  # FUNCTION 1
        if password == stored_password and username == stored_username:
            if 'flash-message1' in session:
                session.pop('flash-message')
            session['user'] = username
            return redirect(url_for('my_recipes', username=username))

        else:
            session['flash-message'] = 1
            flash("Incorrect username or password")
            return redirect(url_for('home'))

    except BaseException:
        session['flash-message'] = 1
        flash("Incorrect username or password")
        return redirect(url_for('home'))
#-------------------------------------------------------Sign In Form  #------------------------------------------------------Log Out  
""" When the logout button is pressed the user session ends and is returned to
the index page"""

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))
#------------------------------------------------------Log Out
#--------------------------------------------------------User session functions
"""User in session function: 
 A function to say that if the session['user'] variable is in session, 
 username will be what the session variable is. """
def if_user_in_session():
    username = ""
    if 'user' in session:
        username = session['user']
    return username


"""Remove session variable if in use"""
def pop_flask_message():
    if 'flash-message' in session:
        return session.pop('flash-message')
 
 
 
"""returns a list of the current usernames in the collections database whether the requested username is taken."""
def current_usernames():
    items = []
    usernames = mongo.db.user_details.find()
    for item in usernames:
        for key, value in item.items():
            if key == "username":
                items.append(value)  
    return items
#------------------------------------------------------------User session functions     

#--------------------------------------------------Recipes CRUD functionality
@app.route('/get_recipes')
def get_recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())
   
   
"""Adding the recipe into mongo db: recipes, cuisine and allergens collections""" 
@app.route('/add_recipe')
def add_recipe():
    return render_template(
        "add_recipe.html",
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
   
   
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe(): 
    recipes=mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

  
"""Route for editing the recipes page, using the recipe id to display that recipes content from the form"""
@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        'edit_recipe.html',
        recipe=the_recipe,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
    
   
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes=mongo.db.recipes
    recipes.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'recipe_description': request.form.get('recipe_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_recipes'))
    
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

#--------------------------------------------------Recipes CRUD functionality

#--------------------------------------------------Categories CRUD functionality
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
    categories = mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category = mongo.db.categories.find_one({'_id': ObjectId(category_id)}))
    

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))


@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id':ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/insert_category', methods=['POST'])
def insert_category():
    categories = mongo.db.categories
    category_doc = {'category_name': request.form.get('category_name')}
    categories.insert_one(category_doc)
    return redirect (url_for('get_categories'))
    
    
@app.route('/new_category')
def new_category():
    return render_template('addcategory.html')
#--------------------------------------------------Categories CRUD functionality

#-------------------------------------------------Database
def recipe_database():
    data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "ingredients": request.form.getlist('ingredient'),
        "instructions": request.form.getlist('instruction'),
        "image": request.form.get('image'),
        "cuisine": request.form.getlist('cuisine'),
        "allergens": request.form.getlist('allergens'),
        "prep_time": request.form.get('prep_time'),
        "cook_time": request.form.get('cook_time'),
        "servings": request.form.get('servings'),
        "username": session['user']
    }
    return data

# List of the cuisine categories
cuisine_json = []
with open("data/cuisine_category.json", "r") as file:
    cuisine_json = json.load(file)


# List of the allergen categories
allergens_json = []
with open("data/allergen_category.json", "r") as file:
    allergens_json = json.load(file)
#-------------------------------------------------Database
    
    
    
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)