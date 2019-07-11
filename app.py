import os
import json
import pymongo
from flask import Flask, render_template, redirect, request, url_for,session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'data'
app.config['MONGO_URI'] = ('mongodb+srv://casey:rOOtUser@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority')

mongo = PyMongo(app)


# List of the cuisine categories
cuisines_json = []
with open("data/cuisine_category.json", "r") as file:
    cuisines_json = json.load(file)



# List of the allergen categories
allergens_json = []
with open("data/allergen_category.json", "r") as file:
    allergens_json = json.load(file)


def recipe_database():
    data = {
        "name": request.form.get('name'),
        "cuisine": request.form.getlist('cuisine'),
        "allergens": request.form.getlist('allergens'),
        "description": request.form.get('description'),
        "ingredients": request.form.getlist('ingredient'),
        "instructions": request.form.getlist('instruction'),
        "prep_time": request.form.get('prep_time'),
        "cook_time": request.form.get('cook_time'),
        "recipe_yield": request.form.get('recipe_yield'),
        "author": request.form.get('author'),
        "image": request.form.get('image'),
        "username": session['user']
    }
    return data


def registration_form():
    data = {
        "first_name": request.form.get('register_first_name'),
        "username": request.form.get('register_username'),
        "email": request.form.get('register_email'),
        "password": request.form.get('register_password')
    }
    return data



"""
FUNCTION 1
A function to return a specific field value after performing a query search"""
def find_value(variable):
    item = ""
    for key, value in variable.items():
        if key != "_id":
            item = value
    return item
    
"""
FUNCTION 2
 A function to say that if the session['user'] variable is in session, 
 username will be what the session variable is. """
def if_user_in_session():
    username = ""
    if 'user' in session:
        username = session['user']
    return username
"""
FUNCTION 3
Removes the session variable if it's in session."""
def pop_flask_message():
    if 'flash-message1' in session:
        return session.pop('flash-message1')
        
"""
FUNCTION 4
returns a list of the current usernames in the mlab database. Used in the 
base.html and combined with jinja and javascript to tell the user on
registration from submission, whether the requested username is taken or not."""
def current_usernames():
    
    items = []
    usernames = mongo.db.user_details.find()
    for item in usernames:
        for key, value in item.items():
            if key == "username":
                items.append(value)  
    return items


#-----------------------------------------****INDEX
@app.route('/')
def index():
    
    usernames = current_usernames() # FUNCTION 4
    recipes = mongo.db.recipe.aggregate([{ "$match": { "username": "admin"} }, {"$sample": {"size": 5}}])
    
    return render_template('index.html', recipes=recipes, usernames=usernames)



#------------------------------------------****RECIPES 
@app.route("/recipes")
def recipes():
    all_recipes = mongo.db.recipe.find(
        {"$query": {}, "$orderby": {"name": 1}}).limit(4)
    
    return render_template(
        'recipes.html',
        all_recipes=all_recipes,
        cuisines_json=cuisines_json,
        allergens_json=allergens_json,
        usernames=usernames)      
   
   
   
#----------------------------------------**** ADD RECIPE TO DATABASE
@app.route("/add_recipe")
def add_recipe():
    return render_template(
        "add_recipe.html",
        cuisines_json=cuisines_json,
        allergens_json=allergens_json)
   
   
   
#-----------------------------------**** INSERT RECIPE INTO DATABASE  
@app.route("/insert_recipe", methods=['POST'])
def insert_recipe():
    username = if_user_in_session()
    mongo.db.recipe.insert_one(doc)
    id_num = mongo.db.recipe.find_one(
        {'name': request.form.get('name'), 'username': username})
    
    recipe_id = ""
    for key, value in id_num.items():
        if key == "_id":
            recipe_id = ObjectId(value)
    mongo.db.recipe.update_one({'_id': ObjectId(recipe_id)}, {
        "$set": {"views": 0}}, upsert=True)
    mongo.db.recipe.update_one({'_id': ObjectId(recipe_id)}, {
        "$set": {"likes": 0}}, upsert=True)
        
    mongo.db.recipe.update_one({'_id': ObjectId(recipe_id)}, {
        "$set": {"submit_date":adelaide_now}}, upsert=True)
        
    return redirect(url_for('single_recipe', recipe_id=recipe_id))
   
   
  
#-------------------------------------------------**** EDIT RECIPE
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit_recipe.html',
                            recipe=the_recipe,
                            cuisines_json=cuisines_json,
                            allergens_json=allergens_json)
    
   
   
#-------------------------------------------------**** UPDATE RECIPE
@app.route('/update_recipe/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id):
    username = if_user_in_session() 

    author = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
    contributer = ""
    for key, value in author.items():
        if key == "username":
            contributer = value

    if username == contributer or username == "admin":
        mongo.db.recipe.update_many({'_id': ObjectId(recipe_id)}, {
                                    "$set": recipe_database()})

        id_num = mongo.db.recipe.find_one(
            {'name': request.form.get('name'), 'username': username})

        recipe_id = ""
        for key, value in id_num.items():
            if key == "_id":
                recipe_id = ObjectId(value)

        return redirect(url_for('single_recipe', recipe_id=recipe_id))
    else:
        session['flash-message-not-allowed'] = True
        flash("There was an error in the last action. Please sign in again.")
        if 'user' in session:
            session.pop('user')
        return redirect(url_for('index'))
    
    
    
#-----------------------------------------------------**** DELETE
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    username = if_user_in_session()

    author = mongo.db.recipe.find_one({'_id': ObjectId(recipe_id)})
    contributer = ""
    for key, value in author.items():
        if key == "username":
            contributer = value

    if username == contributer or username == "admin":

        mongo.db.recipe.remove({'_id': ObjectId(recipe_id)})
        return redirect(url_for('my_recipes', username=username))
        
    else:
        session['flash-message-not-allowed'] = True
        flash("There was an error in the last action. Please sign in again.")
        if 'user' in session:
            session.pop('user')
        return redirect(url_for('index'))



#--------------------------------------------------**** USER RECIPES
@app.route('/user_recipes/<username>')
def user_recipes(username):
    pop_flask_message() # FUNCTION 3
    if session['user'] == username:
        user = mongo.db.user_details.find_one({"username": username})
        user_recipes = mongo.db.recipe.find({"username": session['user']})
        recipe_count = user_recipes.count()

        return render_template(
            'user_recipes.html',
            user=user,
            user_recipes=user_recipes,
            cuisines_json=cuisines_json,
            allergens_json=allergens_json,
            recipe_count=recipe_count)

    else:
        session['flash-message-not-allowed'] = True
        flash("There was an error in the last action. Please sign in again.")
        if 'user' in session:
            session.pop('user')
        return redirect(url_for('index'))



#------------------------------------------------**** SINGLE RECIPE
@app.route('/single_recipe/<recipe_id>')
def single_recipe(recipe_id):
    pop_flask_message()
    usernames = current_usernames() 
    recipe_name = mongo.db.recipe.find_one(
        {'_id': ObjectId(recipe_id)}, {"name"})
        
    the_recipe = mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    username = if_user_in_session()   
    recipe = find_value(recipe_name) 

   





#-------------- Registration Section - signin into user session

# ---------------------------------------Registration form
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



# --------------------------------------- Sign in
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



#--------------------------------------------Log out
@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('index'))

#----END OF------- Registration Section - signin into user session



#----------------------------------**** FIND INGREDIENTS
@app.route("/find_ingredient", methods=['POST'])
def find_ingredient():
    pop_flask_message() 
    usernames = current_usernames()
    session["search_title"] = 0
    recipe_category = mongo.db.recipe.find(
        {"ingredients": {"$regex": request.form.get("ingredient_category"), "$options": 'i'}})
    recipe_count = recipe_category.count()
    return render_template(
        'search_results.html',
        recipe_category=recipe_category,
        cuisines_json=cuisines_json,
        allergens_json=allergens_json,
        usernames=usernames)






























if __name__ == '__main__':
    app.run(
            debug=True)