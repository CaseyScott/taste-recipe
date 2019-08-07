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
meal_types_file = []
with open("data/meals_data.json", "r") as json_data:
    meal_types_file = json.load(json_data)
    
allergens_file = []
with open("data/allergen_data.json", "r") as json_data:
    allergens_file = json.load(json_data)
    
    
    



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
"""if request is POST and if the two given passwords match. It checks if the username already exists in database if the username doesnt already exist it hashs the password using bcrypt, this is sent to MONGODB users collection. if all worked corectly the session username variable is created for that username and the user is redirected to index/home"""
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        if request.form['pass'] != request.form['pass_confirm']:
            error = "Passwords don't match!"
            return render_template('pages/register.html', error=error)
        #mongo.db.users is the database of usernames
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
"""if the request is POST, it looks for that user in list of usernames in MONGODB users collection, if password matches, session username variable is created for that user. Logged in user is redirected to index/home"""  
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
"""logout uses the pop method to release that session variable username """
@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('index'))

"""----------------------------------------------------"""
# ADD RECIPE #
"""User is sent to 'add recipes page' which includes data from meal_types and allergens json files."""
@app.route('/add_recipe', methods=['GET', 'POST'])
def add_recipe():
    recipes=mongo.db.recipes
    return render_template("pages/add_recipe.html",
    meal_types_file=meal_types_file,
    allergens_file=allergens_file)

# INSERT #
"""from add recipe page the user input information is stored as a dictionary in the MONGODB recipes collection, calling to_dict on the request.form object gives back a dictionary that can be used to display recipes from the recipes collection.Inserts one new recipe with an id into the recipes collection."""
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes=mongo.db.recipes
    new_recipe_id=recipes.insert_one(request.form.to_dict()).inserted_id
    return redirect(url_for('get_user_recipe', recipe_id=new_recipe_id))



# ALL RECIPES #
"""all recipes in the MONGODB recipes collection. find()=find all"""
@app.route("/recipes", methods=['GET', 'POST'])  
def recipes():
    recipes=mongo.db.recipes.find()
    return render_template('pages/recipes.html',
    recipes=recipes)

   
# GET USER RECIPE #  
"""Session user recipe list from recipes collection that they have contributed to the database"""      
@app.route('/get_user_recipe', methods=['GET', 'POST'])
def get_user_recipe(): 
    
    recipes=mongo.db.recipes.find()
    
    return render_template('pages/get_user_recipe.html',
        recipes=recipes,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)
    
    
# EDIT #
"""editing one recipe by its recipe_id as the_recipe including meal_type and allergen data display all input information in the form to be edited"""
@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    
    the_recipe=mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    return render_template('pages/edit_recipe.html',
        recipes=the_recipe,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)
    
    
"""add recipe / edit recipe  input form"""    
def recipe_data():
    data = {
        "name": request.form.get('name'),
        "description": request.form.getlist('description'),
        "ingredients": request.form.getlist('ingredients'),
        "instructions": request.form.getlist('instructions'),
        "image": request.form.get('image'),
        "meal_types": request.form.getlist('meal_types'),
        "allergens": request.form.getlist('allergens'),
        "preparation": request.form.get('preparation'),
        "cooking": request.form.get('cooking'),
        "servings": request.form.get('servings'),
        "username": session['username']
    }
    return data

# UPDATE #
"""from edit recipe the edited information is sent to MONGODB recipes collection. $set:recipe_data replaces the value of a field with the specified value."""
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
    
    recipes=mongo.db.recipes
    recipes.update_many(
        {'_id': ObjectId(recipe_id)},
        {"$set": recipe_data()})
                  
    return redirect(url_for('get_user_recipe', recipe_id=recipe_id))
    
    


    
# DELETE # 
"""delete recipe removes recipe from MONGODB recipes collection
only the creator of that recipe can delete by matching session username"""  
### .remove or .delete_one ### 
@app.route('/delete_recipe/<recipe_id>', methods=['POST'])
def delete_recipe(recipe_id):
    recipes = mongo.db.recipes
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('recipes'))


#-----------------------------------Recipes CRUD functionality
"""-------------------------------------------------------"""


@app.route("/ingredients_search", methods=['POST'])
def ingredients_search():
    recipesByIngredients=mongo.db.recipesByIngredients.find(
        {"ingredients": {"$text": request.form.get("ingredient_category")}})
    return render_template(
        'search_results.html',
        recipes=recipes_by_ingredients,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)


@app.route("/meals_search", methods=['POST'])
def category_search():
    recipes_by_meals=mongo.db.recipe.find(
        {"meals": request.form.get("meals").title()})
    return render_template(
        'search_results.html',
        recipes=recipes_by_cuisine,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)


@app.route("/allergen_search", methods=['POST'])
def allergen_search():
    recipes_by_allergen=mongo.db.recipe.find(
        {"allergens": {"$nin": request.form.get("allergen_category")}})
    return render_template(
        'search_results.html',
        recipes=recipes_by_allergen,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)
    
    
@app.route("/search_categories", methods=['POST'])
def search_categories():
    ingredients = request.form.get("ingredient_search")
    meal_types = request.form.getlist("meal_types_search")
    allergens = request.form.getlist("allergen_search")
    
    
    #if all 3 search boxes are used to search for ingreditents, meal type and allergens $text performs a text search on the content of the input fields"""
    if ingredients and meal_types and allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and": [
                {"meal_types": meal_types},
                {"allergens": allergens},
                {"ingredients": {"$text": ingredients}}]})


    #if ingredients and meal type are searched"""
    elif ingredients and meal_types and not allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and":[
                {"meal_types": meal_types},
                {"ingredients": {"$text": ingredients}}]})


     #if ingredients and allergen are searched but meal type is left empty
    elif ingredients and meal_types == "" and allergens:
        recipe_category = mongo.db.recipes.find(
            {"$and": [
                {"allergens": allergens},
                {"ingredients": {"$text": ingredient}}]})

    elif not ingredients and meal_types and allergens:
        recipe_category = mongo.db.recips.find(
            {"$and": [
                {"meal_types": meal_types},
                {"allergens": {"$nin": allergens}}]})

    elif not ingredients and not allergens:
        recipe_category = mongo.db.recipe.find(
            {"meal_types": meal_types}) 

    elif meal_types == "" and not allergens:
        recipe_category = mongo.db.recipe.find(
            {"ingredients": {"$text": ingredients}})

    elif meal_types == "" and not ingredients:
        recipe_category = mongo.db.recipe.find(
            {"allergens": allergens})
        
        
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)



if __name__ == '__main__':
    app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)