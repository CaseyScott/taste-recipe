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


users = mongo.db.users
recipes = mongo.db.recipes




### Data for dropdown selectors in add recipe form
cuisine_json = []
with open("data/cuisine_data.json", "r") as file:
    cuisine_json = json.load(file)
allergen_json = []
with open("data/allergen_data.json", "r") as file:
    allergens_json = json.load(file)
    
    
    

def recipe_data():
    data = {
        "name": request.form.get('recipe_name'),
        "description": request.form.get('description'),
        "ingredients": request.form.get('ingredients'),
        "instructions": request.form.get('instructions'),
        "image": request.form.get('image'),
        "cuisine": request.form.getlist('cuisine'),
        "allergens": request.form.getlist('allergens'),
        "preparation": request.form.get('preparation'),
        "cooking": request.form.get('cooking'),
        "servings": request.form.get('servings'),
        "username": session['username']
    }
    return data



def logged_in_user():
    username=''
    if 'username' in session:
        username=session['username']
    return username



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
 
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

"""----------------------------------------------------"""


@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    recipes = mongo.db.recipes
    return render_template("pages/add_recipe.html",
    cuisine_json=cuisine_json,
    allergens_json=allergens_json)



@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    new_recipe_id=recipes.insert_one(request.form.to_dict()).inserted_id
    return redirect(url_for('get_recipe', recipe_id=new_recipe_id))



"""Getting a document back out, use the find_one() function"""
### all the recipes #
@app.route("/recipes", methods=['GET', 'POST'])  
def recipes():
    recipes=mongo.db.recipes.find_one()
    return render_template('pages/recipes.html')

   
   
   
### single recipe users added recipes#   
@app.route('/get_recipe/<recipe_id>')
def get_recipe(recipe_id):    
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template('pages/recipes.html', recipe=the_recipe)
    
    


@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    return render_template(
        'pages/edit_recipe.html',
        recipe=the_recipe,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
    



@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    recipes=mongo.db.recipes
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
#$regex
"""https://docs.mongodb.com/manual/reference/operator/query-evaluation/"""

#request.form.getlist
"""https://stackoverflow.com/questions/14188451/get-multiple-request-params-of-the-same-name"""

#case sensitive caseInsensitive
"""https://stackoverflow.com/questions/10700921/case-insensitive-search-with-in"""

#mongo return documents without a specific value
"""https://docs.mongodb.com/manual/reference/operator/query/nin/"""

#Query MongoDB with $and and Multiple $or
"""https://stackoverflow.com/questions/40388657/query-mongodb-with-and-and-multiple-or"""

#Validation - check to make sure at least one field is filled out
"""https://www.sitepoint.com/community/t/validation-check-to-make-sure-at-least-one-field-is-filled-out/2329"""

#Javascript - How to check if a typed image URL really exists
"""https://stackoverflow.com/questions/24577534/javascript-how-to-check-if-a-typed-image-url-really-exists"""

@app.route("/ingredients_search", methods=['POST'])
def ingredients_search():
    recipe_category = mongo.db.recipes.find(
        {"ingredients": {"$regex": request.form.getlist("ingredient_category"), "$options": 'i'}})
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)


@app.route("/cuisine_search", methods=['POST'])
def cuisine_search():
    recipe_category = mongo.db.recipe.find(
        {"cuisine": request.form.getlist("cuisine_category").title()})
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)


@app.route("/allergen_search", methods=['POST'])
def allergen_search():
    recipe_category = mongo.db.recipe.find(
        {"allergens": {"$nin": request.form.getlist("allergen_category")}})
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)
    
    
@app.route("/search_categories", methods=['POST'])
def search_categories():
    ingredient = request.form.get("ingredient_search")
    cuisine = request.form.getlist("cuisine_search")
    allergens = request.form.getlist("allergen_search")
    
    if ingredient and cuisine and allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and": [{"cuisine":cuisine},
            {"allergens": {"$nin": allergens}},
            {"ingredients": {"$regex": ingredient, "$options": 'i'}}]})

    elif ingredient and cuisine and not allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and":[
            {"cuisine": cuisine},
            {"allergens": {"$nin": allergens}},
            {"ingredients": {"$regex": ingredient, "$options": 'i'}}]})

    elif ingredient and cuisine == "" and allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and": [{"allergens": {"$nin": allergens}},
            {"ingredients": {"$regex": ingredient, "$options": 'i'}}]})

    elif not ingredient and cuisine and allergens:
        recipe_category = mongo.db.recips.find(
            {"$and": [
            {"cuisine": cuisine}, {"allergens": {"$nin": allergens}}]})

    elif not ingredient and not allergens:
        recipe_category = mongo.db.recipe.find(
            {"cuisine": cuisine}) 

    elif cuisine == "" and not allergens:
        recipe_category = mongo.db.recipe.find(
            {"ingredients": {"$regex": ingredient, "$options": 'i'}})

    elif cuisine == "" and not ingredient:
        recipe_category = mongo.db.recipe.find(
            {"allergens": {"$nin": allergens}})
        
        
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        recipe_count=recipe_count,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json)



if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)