import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for,session, json, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
#import bcrypt
#from flask_login import login_user
#from app.home import home
#from app import mongo, bcrypt, login_manager
#from app.home.user_loging_manager import User

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


@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']
        
    return render_template('pages/index.html')


#--------------------------------------------User session functions
def find_value(variable):
    item = ""
    for key, value in variable.items():
        if key != "_id":
            item = value
    return item


def if_user_in_session():
    username = ""
    if 'user' in session:
        username = session['user']
    return username


def pop_flask_message():
    if 'flash-message1' in session:
        return session.pop('flash-message1')
 
 
def current_usernames():
    items = []
    usernames = mongo.db.user_details.find()
    for item in usernames:
        for key, value in item.items():
            if key == "username":
                items.append(value)  
    return items
#--------------------------------------User session functions 

#-----------------------------------------------Registion Form  
def registration_form():
    data = {
        "username": request.form.get('register_username'),
        "email": request.form.get('register_email'),
        "password": request.form.get('register_password'),
    }
    return data

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
                        'my_recipe',
                        username=requested_username))

            else:
                return redirect(request.referrer)

        except BaseException:
            return redirect(request.referrer)

    else:
        return redirect(request.referrer)
    
#-----------------------------------------------Registion Form

#---------------------------------------------------Sign In Form

@app.route('/signin', methods=['POST'])
def signin():

    username = request.form.get('signin_username')
    password = request.form.get('signin_password')

    try:
        user_doc_username = mongo.db.user_details.find_one(
            {'username': username}, {'username'})
        user_doc_password = mongo.db.user_details.find_one(
            {'username': username}, {'password'})

        stored_username = find_value(user_doc_username) 
        stored_password = find_value(user_doc_password)  
        if password == stored_password and username == stored_username:
            if 'flash-message1' in session:
                session.pop('flash-message1')
            session['user'] = username
            return redirect(url_for('my_recipes', username=username))

        else:
            session['flash-message1'] = 1
            flash("Incorrect username or password")
            return redirect(url_for('index'))

    except BaseException:
        session['flash-message1'] = 1
        flash("Incorrect username or password")
        return redirect(url_for('index'))
        
#---------------------------------------Sign In Form  

#-------------------------------------Sign Out  
@app.route('/signout')
def signout():
    session.pop('user')
    return redirect(url_for('index'))
#---------------------------------------Sign Out

#----------------------------------------Recipes CRUD functionality
@app.route("/recipes")
def recipes():
    usernames = current_usernames()
    recipes = mongo.db.recipe.find()

    pop_flask_message()

    return render_template(
        'pages/recipes.html',
        recipes=recipes,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json,
        usernames=usernames)


@app.route('/get_recipes')
def get_recipes():
    return render_template('pages/recipes.html', recipes=mongo.db.recipes.find())
   
   
@app.route('/add_recipe')
def add_recipe():
    return render_template(
        "pages/add_recipe.html",
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
   
   
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe(): 
    recipes=mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))

  
@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        'pages/edit_recipe.html',
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
        'recipe_description': request.form.get('recipe_description')
    })
    return redirect(url_for('get_recipes'))
    
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))

#-----------------------------------Recipes CRUD functionality

#---------------------------Categories CRUD functionality
@app.route('/get_categories')
def get_categories():
    return render_template('pages/categories.html',
    categories = mongo.db.categories.find())


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('pages/editcategory.html',
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
    return render_template('pages/addcategory.html')
#-----------------------------------Categories CRUD functionality

#-------------------------------------------------Database
def recipe_database():
    data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "ingredients": request.form.getlist('ingredients'),
        "instructions": request.form.getlist('instructions'),
        "image": request.form.get('image'),
        "cuisine": request.form.getlist('cuisine'),
        "allergens": request.form.getlist('allergens'),
        "prep": request.form.get('prep'),
        "cook": request.form.get('cook'),
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

#-------------------------------------------------My Recipes
@app.route('/my_recipes/<username>')
def my_recipes(username):
    pop_flask_message() 
    if session['user'] == username:
        user = mongo.db.user_details.find_one({"username": username})
        user_recipes = mongo.db.recipe.find({"username": session['user']})
        recipe_count = user_recipes.count()

        return render_template(
            'pages/my_recipes.html',
            user=user,
            user_recipes=user_recipes,
            cuisine_json=cuisine_json,
            allergens_json=allergens_json,
            recipe_count=recipe_count)

    else:
        session['flash-message-not-allowed'] = True
        flash("There was an error in the last action. Please sign in again.")
        if 'user' in session:
            session.pop('user')
        return redirect(url_for('index'))
#------------------------------------------------My Recipes
    
    
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)