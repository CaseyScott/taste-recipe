import os
from flask import Flask, render_template, redirect, request,url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config['MONGO_DBNAME']='data'
app.config['MONGO_URI']='mongodb+srv://casey:rOOtUser@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority'

mongo=PyMongo(app)

@app.route('/')
  
@app.route('/get_recipes')
def get_recipes():
  return render_template('recipes.html', recipe= mongo.db.recipe.find())

if __name__ == '__main__':
  
  #app.run(debug=True)
  """app.run(host=os.environ.get("0.0.0.0"),
          port=os.environ.get("5000"),
          debug=True)"""
  
  app.run(host=os.getenv("IP"),
          port=os.getenv("PORT"),
          debug=True)