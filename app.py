import os
import pymongo
from flask import Flask, render_template, redirect, request, url_for,escape, session, json, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt


app = Flask(__name__)
#bcrypt = Bcrypt(app)

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



cuisine_json = []
with open("data/cuisine_data.json", "r") as file:
    cuisine_json = json.load(file)


allergen_json = []
with open("data/allergen_data.json", "r") as file:
    allergens_json = json.load(file)
    

def recipe_data():
    data = {
        "recipe_name": request.form.get('recipe_name'),
        "description": request.form.get('description'),
        "ingredients": request.form.getlist('ingredients'),
        "instructions": request.form.getlist('instructions'),
        "image": request.form.get('image'),
        "cuisine": request.form.getlist('cuisine'),
        "allergens": request.form.getlist('allergens'),
        "prep": request.form.get('prep_time'),
        "cook": request.form.get('cook_time'),
        "servings": request.form.get('servings'),
        "username": session['username']
    }
    return data

def registration_data():
    data = {
        "name": request.form.get('username'),
        "password": request.form.get('pass')
    }
    return data

"""----------------------------------------------------"""  

@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('pages/index.html')

"""----------------------------------------------------"""      
        
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        users = mongo.db.users
        logged_in = users.find_one({'name' : request.form['username']})
        error = 'Invalid username or password. Please try again!'

        if logged_in:
            validPasswd = bcrypt.checkpw(request.form['pass'].encode('utf-8'), logged_in['password'])
            if validPasswd:
                session['username'] = request.form['username']
                   
                
                return redirect(url_for('index'))
            
        return render_template('pages/login.html', error = error)
        
    return render_template('pages/login.html', error = error)


"""----------------------------------------------------"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        if request.form['pass'] != request.form['pass_confirm']:
            error = "Passwords don't match!"
            return render_template('pages/register.html', error=error)
        
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            
            
            error = 'Invalid username or password. Please try again!'
            
            return redirect(url_for('index',error = error))
        
        return render_template('pages/register.html', error = error)  
    
    return render_template('pages/register.html', error = error) 
  
         
          
#-------------------------------------Sign Out  
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))
#---------------------------------------Sign Out

#----------------------------------------Recipes CRUD functionality

### all the recipes #
@app.route("/recipes")  
def recipes():
    recipes=mongo.db.recipes.find_one()
    return render_template('pages/recipes.html')

 
@app.route('/add_recipe')
def add_recipe():
    recipes = mongo.db.recipes
    return render_template("pages/add_recipe.html",
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
   
   
### single recipe #   
@app.route('/recipe/<recipe_id>', methods=['GET', 'POST'])
def recipe(recipe_id):
    
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    return render_template(
        'pages/recipe.html',
        recipe=the_recipe)



@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    objectID=recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipe', recipe_id=objectID))



@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template(
        'pages/edit_recipe.html',
        recipe=the_recipe,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
    


@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipe=mongo.db.recipes
    recipe.update({'_id': ObjectId(recipe_id)},
    {
        'recipe_name': request.form.get('recipe_name'),
        'category_name': request.form.get('category_name'),
        'description': request.form.get('description')
    })
    return redirect(url_for('recipes'))
    
    
    
### .remove or .delete_one ### 
@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipes = mongo.db.recipes
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))


#-----------------------------------Recipes CRUD functionality
"""-------------------------------------------------------"""
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
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)