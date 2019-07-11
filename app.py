import os
import json
import pymongo
from flask import Flask, render_template, redirect, request, url_for
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
        "last_name": request.form.get('register_last_name'),
        "username": request.form.get('register_username'),
        "email": request.form.get('register_email'),
        "password": request.form.get('register_password'),
        "liked_recipes": []
    }
    return data


#---- Tasks ---------

@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template('tasks.html', tasks=mongo.db.tasks.find())
   
#-------------------------------edited for recipe
@app.route("/add_recipe")
def add_recipe():
    return render_template(
        "add_recipe.html",
        cuisines_json=cuisines_json,
        allergens_json=allergens_json)
   
#----------------------------------------insert recipe into database  
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
   
   
  
    
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipe.find_one({"_id": ObjectId(recipe_id)})
    return render_template('edit_recipe.html',
                            recipe=the_recipe,
                            cuisines_json=cuisines_json,
                            allergens_json=allergens_json)
    
   
@app.route('/update_task/<task_id>', methods=['POST'])
def update_task(task_id):
    tasks = mongo.db.tasks
    tasks.update({'_id': ObjectId(task_id)},
    {
        'task_name': request.form.get('task_name'),
        'category_name': request.form.get('category_name'),
        'task_description': request.form.get('task_description'),
        'due_date': request.form.get('due_date'),
        'is_urgent': request.form.get('is_urgent')
    })
    return redirect(url_for('get_tasks'))
    
    
@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    mongo.db.tasks.remove({'_id': ObjectId(task_id)})
    return redirect(url_for('get_tasks'))



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




































if __name__ == '__main__':
    app.run(
            debug=True)