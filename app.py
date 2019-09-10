import re
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



### Data for dropdown selectors in add recipe form
meal_types_file = []
with open("data/meals_data.json", "r") as f:
    meal_types_file = json.load(f)
    
allergens_file = []
with open("data/allergen_data.json", "r") as f:
    allergens_file = json.load(f) 
    
"""add recipe / edit recipe  input form """
def recipe_data(request):
    data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "ingredients": request.form.get('ingredients'),
        "instructions": request.form.get('instructions'),
        "image": request.form.get('image'),
        "meals": request.form.get('meals'),
        "allergen": request.form.get('allergen'),
        "preparation": request.form.get('preparation'),
        "cooking": request.form.get('cooking'),
        "servings": request.form.get('servings'),
        "author": request.form.get('author'),
        "username": session['username'],
    }
    return data 

"""----------------------------------------------------"""  

@app.route('/', methods=['GET'])

@app.route('/index', methods=['GET'])
def index():
    return render_template('pages/index.html',
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file)

"""----------------------------------------------------"""


"""if request is POST and if the two given passwords match. It checks if the username already exists in database if the username doesnt already exist it hashs the password using bcrypt, this is sent to MONGODB users collection. if all worked correctly the session username variable is created for that username and the user is redirected to index/home"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    
    if request.method == 'POST':
        if request.form['pass'] != request.form['pass_confirm']:
            error = "Passwords don't match!"
            return render_template('pages/register.html', error=error)
        #mongo.db.users is the database of usernames
        user=mongo.db.users
        existing_user=user.find_one({'name' : request.form['username']})
        
        
        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            user.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            session['logged_in']=True
            error = 'Invalid username or password. Please try again!'
            
            flash('You have successfully registed')
            return redirect(url_for('index',error = error))
        
        return render_template('pages/register.html', error = error)  
    
    return render_template('pages/register.html', error = error) 



"""----------------------------------------------------"""      
"""if the request is POST, it looks for that user in list of usernames in MONGODB users collection, if password matches, session username variable is created for that user. Logged in user is redirected to index/home"""  

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    
    if request.method == 'POST':
        user = mongo.db.users
        logged_in = user.find_one({'name' : request.form['username']})
        error = 'Invalid username or password. Please try again!'

        if logged_in:
            validPasswd = bcrypt.checkpw(request.form['pass'].encode('utf-8'), logged_in['password'])
            if validPasswd:
                session['username'] = request.form['username']
                session['logged_in']=True   
                
                flash('You were successfully logged in')
                return redirect(url_for('index'))
            
        return render_template('pages/login.html', error = error)
        
    return render_template('pages/login.html', error = error)



"""----------------------------------------------------"""
"""logout uses the pop method to release that session variable username """
@app.route('/logout')
def logout():
    session.pop('username')
    flash("Successfully logged out ...")
    return redirect(url_for('index'))

"""----------------------------------------------------"""



# ADD RECIPE #
"""User is sent to 'add recipes page' which includes data from meal_types and allergens json files."""

@app.route('/add_recipe', methods=['GET'])
def add_recipe():
    
    user=mongo.db.users.find_one({"name": session['username']})
    recipes=mongo.db.recipes
    
    return render_template("pages/add_recipe.html",
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file,
                            user=user,
                            recipes=recipes)



# INSERT #
"""from add recipe page the user input information is stored as a dictionary in the MONGODB recipes collection, calling to_dict on the request.form object gives back a dictionary that can be used to display recipes from the recipes collection.Inserts one new recipe with an id into the recipes collection."""

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    
    if 'username' in session:
        user=mongo.db.users.find_one({"name": session['username']})
                                             
        recipes=mongo.db.recipes
        recipe_dict=request.form.to_dict()
        recipe_dict['user_id']=user['_id']
        
        new_recipe_id = recipes.insert_one(recipe_dict)
        new_recipe_id = new_recipe_id.inserted_id
        
        flash('Recipe Added!')
    
    return redirect(url_for('get_user_recipe', recipe_id=new_recipe_id))




# ALL RECIPES #
"""all recipes in the MONGODB recipes collection. find()=find all"""

@app.route("/recipes", methods=['GET', 'POST'])  
def recipes():
    
    recipes=mongo.db.recipes.find()
    numberOfRecipes = None
    
    # PAGINATION #
    #offset=int(request.args['offset'])
    #limit=int(request.args['limit'])
    
    #starting_id=recipe.find().sort('_id', pymongo.ASCENDING)
    #last_id=starting_id[offset]['_id']
    
    #recipes=recipe.find({'_id' : {'$gte' : last_id}}).sort('_id', pymongo.ASCENDING).limit(limit)
    #output=[]
    
    #for i in recipes:
        #output.append({'recipe' : i['recipe']})
        
    #next_url='/recipes?limit=' + str(limit) + '&offset=' + str(offset + limit)
    #prev_url='/recipes?limit=' + str(limit) + '&offset=' + str(offset - limit)
    
    #return jsonify({'result' : output, 'prev_url' : prev_url, 'next_url' : next_url})
        
    return render_template('pages/recipes.html',
                            numberOfRecipes=numberOfRecipes,
                            recipes=recipes,
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file)

   
   
   
# GET USER RECIPE #  
"""Session user recipe list from recipes collection that they have contributed to the database""" 
     
@app.route('/get_user_recipe', methods=['GET', 'POST'])
def get_user_recipe():
    
    if 'username' in session:
        user=mongo.db.users.find_one({"name": session['username']})
        
        
        user_recipes = mongo.db.recipes.find({"user_id": user['_id']})
        recipe_count = user_recipes.count()
        
    return render_template('pages/get_user_recipe.html',
                            recipe_count=recipe_count,
                            user_recipes=user_recipes,
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file)
    
    
    
#single page recipe
@app.route('/single_recipe/<recipe_id>')
def single_recipe(recipe_id):
    
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    
    return render_template('pages/single_recipe_page.html',
                            recipe=the_recipe,
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file)
    
    
    
    
# EDIT #
"""editing one recipe by its recipe_id as the_recipe including meal_type and allergen data display all input information in the form to be edited"""

@app.route('/edit_recipe/<recipe_id>', methods=['GET', 'POST'])
def edit_recipe(recipe_id):
    
    the_recipe=mongo.db.recipes.find_one(
        {"_id": ObjectId(recipe_id)})
    
    flash("Your recipe has been updated")
    return render_template('pages/edit_recipe.html',
                            recipe=the_recipe,
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file,
                            recipe_id=recipe_id)
    
    


# UPDATE #
"""from edit recipe the edited information is sent to MONGODB recipes collection. $set:recipe_data replaces the value of a field with the specified value."""

@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    
    mongo.db.recipes.update_many(
        {'_id': ObjectId(recipe_id)},
        {"$set": recipe_data(request)})
    
    return redirect(url_for('get_user_recipe', recipe_id=recipe_id))
    
    


    
# DELETE # 
"""delete recipe removes recipe from MONGODB recipes collection
only the creator of that recipe can delete by matching session username"""  

### .remove or .delete_one ### 
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    recipes = mongo.db.recipes
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    flash('Recipe deleted')
    
    return redirect(url_for('get_user_recipe',
                            recipes=recipes))


#-----------------------------------Recipes CRUD functionality


"""--------------Search box modal --------------------"""


@app.route("/ingredients_search", methods=['POST'])
def ingredients_search():
    
    regex = re.compile(r'.*{0}.*'.format(request.form.get("ingredients_search")), re.IGNORECASE)
    recipeSearchCategory=mongo.db.recipes.find({"ingredients": {"$regex": regex}})

    numberOfRecipes=recipeSearchCategory.count()


    return render_template('pages/search_results.html',
                            numberOfRecipes=numberOfRecipes,
                            recipeSearchCategory=recipeSearchCategory)




@app.route("/meals_search", methods=['POST'])
def meals_search():
    
    recipeSearchCategory=mongo.db.recipes.find({"meals": request.form.get("meal_type_file")})
    
    numberOfRecipes=recipeSearchCategory.count()
    
    return render_template('pages/search_results.html',
                            numberOfRecipes=numberOfRecipes,
                            recipeSearchCategory=recipeSearchCategory)



@app.route("/allergen_search", methods=['POST'])
def allergen_search():
    
    recipeSearchCategory=mongo.db.recipes.find({"allergen": {"$ne": request.form.get("allergens_file")}})
    
    numberOfRecipes=recipeSearchCategory.count()
    
    return render_template('pages/search_results.html',
                            numberOfRecipes=numberOfRecipes,
                            recipeSearchCategory=recipeSearchCategory)
    
    
    
@app.route("/search_categories", methods=['POST'])
def search_categories():
    
    ingredients = request.form.get("ingredients_search")
    meals = request.form.get("meals_search")
    allergen = request.form.get("allergen_search")
    
    if ingredients:
        recipeSearchCategory = mongo.db.recipes.find( { "ingredients": { "$regex": ingredients } } )
        
    elif meals:
        recipeSearchCategory = mongo.db.recipes.find( { "meals": meals } ) 

    elif allergen:
        recipeSearchCategory = mongo.db.recipes.find( { "allergen": { "$ne": allergen } } )
        
    elif ingredients and meals:
        recipeSearchCategory = mongo.db.recipes.find( { "$and": [ { "meals": meals }, { "ingredients": { "$regex": ingredients } } ] } )

    elif ingredients and allergen:
        recipeSearchCategory = mongo.db.recipes.find( { "$and": [ { "allergen": { "$ne": allergen } }, { "ingredients": { "$regex": ingredients } } ] } )

    elif meals and allergen:
        recipeSearchCategory = mongo.db.recips.find( { "$and": [ { "meals": meals }, { "allergen": { "$ne": allergen } } ] } )
        
    elif ingredients and meals and allergen:
        recipeSearchCategory = mongo.db.recipes.find( { "$and": [ { "meals": meals }, { "allergen": { "$ne": allergen } }, { "ingredients": { "$regex": ingredients } } ] } )
    
    
    numberOfRecipes=recipeSearchCategory.count()
    
    return render_template('pages/search_results.html',
                            numberOfRecipes=numberOfRecipes,
                            recipeSearchCategory=recipeSearchCategory,
                            meal_types_file=meal_types_file,
                            allergens_file=allergens_file)



if __name__ == '__main__':
    app.run(host=os.getenv('IP'), 
            port=int(os.getenv('PORT')), 
            debug=True)  #set debug to false