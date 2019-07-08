import os
import json
from flask import Flask, render_template, redirect, request,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME']='data'
app.config['MONGO_URI']='mongodb+srv://casey:rOOtUser@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority'

mongo=PyMongo(app)

# List of the cuisine categories
cuisines_json = []
with open("data/cuisine_category.json", "r") as file:
    cuisines_json = json.load(file)



# List of the allergen categories
allergens_json = []
with open("data/allergen_category.json", "r") as file:
    allergens_json = json.load(file)



@app.route('/')
  
@app.route('/get_recipes')
def get_recipes():
  return render_template('recipes.html', recipe= mongo.db.recipe.find())

@app.route("/add_recipe")
def add_recipe():
    return render_template(
        "addrecipe.html",
        cuisines_json=cuisines_json,
        allergens_json=allergens_json)


@app.route("/recipes")
def recipes():
  
  return render_template(
        'recipes.html',
        all_recipes=all_recipes,
        new_recipes=new_recipes,
        most_popular_recipes=most_popular_recipes,
        cuisines_json=cuisines_json,
        allergens_json=allergens_json,
        usernames=usernames)

@app.route("/insert_recipe", methods=['POST'])
def insert_recipe():
  recipe=mongo.db.recipe
  recipe.insert_one(request.form.to_dict())
  return redirect(url_for("get_recipe"))


















if __name__ == '__main__':
  app.run(port=5000,
          debug=True)