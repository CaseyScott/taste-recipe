[Restaurant Chef](https://taste-recipe.herokuapp.com/) 

# **Table of Contents**

- [**Table of Contents**](#table-of-contents)
	- [**Restaurant Chef**](#restaurant-chef)
	- [**Given Brief**](#The-Given-Brief-and-Requirements)
	- [**UX**](#ux)
	   - [**User Stories**](#user-stories)
      - [**Users**](#users)
		- [**Existing features**](#existing-features)
			- [Create account and log in](#Create-account-and-log-in)
			- [Home page](#home-page)
			- [Recipes page](#recipes-page)
         - [Single Recipe page](#single-recipe-page)
         - [My recipes](#my-recipes)
         - [Navigation bar and footer](#navigation-barand-footer)
	- [**Features left to implement**](#features-left-to-implement)
   - [**Wireframes**](#wireframes)
   - [**Database**](#database)
	- [**Technologies used**](#technologies-used)
	- [**Testing**](#testing)
	- [**Deployment**](#deployment)
	- [**How to run the project locally?**](#how-to-run-the-project-locally)
	- [**How to get started**](#how-to-get-started)
   - [**Code used**](#code-used)
	- [**Credits**](#credits)
		- [Special thanks to](#special-thanks-to)
		- [Recipes](#recipes)
		- [Media](#media)



## **Restaurant-Chef**
For display purposes I have created four Users that have each added five recipes. Sign into one of these or create your own for viewing of Create, Read, Update and delete functionality. User names: Asus, Intel, Nvidia, Corsair all users have password of admin.
If deleting please create a new false 'add recipe' entry as delete function is hard delete.

Milestone Project Three:
In this project, I have built a data-driven web application using the technologies that I have learned throughout Data Centric Development. I have choosen to follow the example brief, A recipe webapp with C.R.U.D funcitionality. ( create, read, update and delete )


## **The Given Brief and Requirements**
- **CREATE AN ONLINE COOKBOOK**
- Create a web application that allows users to store and easily access cooking recipes
- design a database schema based on recipes, and any other related properties and entities (e.g. views, upvotes, ingredients, recipe authors, allergens, author’s country of origin, cuisine etc…).
- Create the backend code and frontend form to allow users to add new recipes to the site.
- Create the backend code to group and summarise the recipes on the site, based on their attributes such as cuisine, country of origin, allergens, ingredients, etc. and a frontend page to show this summary, and make the categories clickable to drill down into a filtered view based on that category. This frontend page can be as simple or as complex as you’d like; you can use a Python library such as matplotlib, or a JS library such as d3/dc (that you learned about if you took the frontend modules) for visualisation
- Create the backend code to retrieve a list of recipes, filtered based on various criteria (e.g. allergens, cuisine, etc…) and order them based on some reasonable aspect (e.g. number of views or upvotes). Create a frontend page to display these, and to show some summary statistics around the list (e.g. number of matching recipes, number of new recipes. Optionally, add support for pagination, when the number of results is large
- Create a detailed view for each recipes, that would just show all attributes for that recipe, and the full preparation instructions
- Allow for editing and deleting of the recipe records, either on separate pages, or built into the list/detail pages
- Optionally, you may choose to add basic user registration and authentication to the site. This can as simple as adding a username field to the recipe creation form, without a password (for this project only, this is not expected to be secure)
<hr />

[**To top**](#Table-of-Contents)

## **UX**
I aimed for simple and moden interface with plan easy to use forms for registration, sign in, add recipe and edit recipe. When a user looks for a recipes application they want quick easy access that gets straight to the point. If the users likes the flow of the webapp and its usability they may be interested in contributing their own content to the database to make the application they enjoy using better for others to use to.


## **User Stories**
- As a user I want an easy to use application that I can use on all devices. Weather using my Tablet or laptop in the kitchen or preparing earlier on desktop or mobile to find new family meal ideas.
- As a user I want access to a list of good reicpes with the correct information for me to replicate the meal.
- As a user I want to be able to deselect recipes by allergens as I am allergic to ______.
- As a user I want to be able to contribute to the page with my own recipes.
- As a user I want to sign into my own account to have access to my own recipes that I can edit or delete as I please.
- As a user I want to choose meals to search by a given ingredient. 
- As a user I want to search for a meal type like dinner to be shown all the meals categorised as dinner meals.

### Users
- I have create four Users Asus, Intel, Nvidia, Corsair all users have password of 'admin' these can be used to test add, edit and delete functionality. (Intel/admin1)
- users of the application can use all search functionality and leave with no registration or log in
- users can create an account and log in / log out.
- users that have created an account and are logged in. can add / edit / delete any of their recipes they have contributed.


## Existing Features
### Create account and log in
- A user is able to create and account and log in which changes the Navigation bar to show 'add recipe' and 'my recipes page' which shows that users recipes they have added, giving only them the ability to edit each entry or hard delete that recipe from the database.

### Home page
- Home page gives information about the applications functionality, has links to my linkedin and github pages. If the user wants to get straight to the point they can open the search modal and search by ingredient, type of meal or deselect an allergen they do not want included this will take them directly to the recipes in the database.
- Home page has button link to create an account or user can use Nav bar.
- log in and log out in Nav bar.

### Recipes page
- Recipe page displays all recipes as they have been added. no order. if the user wants to find something specific they can search by type of meal they are looking for e.g Dinner, Breakfast, Dessert or they can search by Ingredient eg. beef or if the user has allergens they do not want included in their search they can choose which allergen they do not want included.

### Single Recipe page
- From the recipes page or results from the 'search by:' selector the user is able to open a single page for that one recipe which gives all the needed details to make the meal. including prep time, cooking time, serving size, ingredients, insructions and the author who contributed the recipe to the database.

### My recipes
- Once the user has logged in the Navigation bar is changed to show my recipes and add recipe buttons, the my recipes page shows all the recipes that user has contributed to the database. they also have the ability to edit or delete their recipes. recipes cards have a read more button linking that recipe to a single full page descripion of that recipe.

### Navigation bar and footer
- navigation for non signed in user (Home, Recipes, Create Account, Log in)
- navigation for signed in user (Home, Recipes, My Recipes, Add Recipe, Log out)
- main Title on top left of Nav goes back to home page from any page.
- footer has My name and my current email address.

## Features left to implement
If I had more time to spend on this project I would like to add:
- pagination is a must for any web app like this.
- Image upload instead of url for add recipe.
- home page images would link to there recipes.
- up voting on favourite recipes.
- user comments on the recipes so people have feedback.
- delete function opens (are you sure?) modal to confirm before hard delete as currently delete is instint hard delete with out confirmation.
- Recipes added by api, data scraping from open source (free) datasets. 
- A back button for Iphone users
- drop down options to not sit infront of submit button on pop up modal.
- more mobile friendly for viewing all recipes.
- most popular recipes by views
- There is a bug in the edit recipe where once the recipe is edited the Added by: is changed to None.

## Wireframes
[wireframe images](https://github.com/CaseyScott/taste-recipe/tree/master/static/img/wireframes)


### Database
The database I have used Is MongoDB, Mongo DB is a document-oriented NoSQL database.
Each database contains collections which in turn contains documents. Each document can be different with a varying number of fields. The Schema doesn't need to be defined beforehand as the fields can be created on the fly.

Example of Schema for recipe:
```
_id:ObjectId("5d54556e67e08a48fa08c77d")
name:"Bitterballen (Dutch meatballs)"
description:"Bread crumbed Beef meatballs"
ingredients:
"100g butter
150g flour
700ml beef stock
30g onion
1tbs parsley
40..."
instructions:
"Melt the butter in a skillet or pan. When melted, add the flour little..."
image:"https://www.themealdb.com/images/media/meals/lhqev81565090111.jpg"
meals:"Snack"
allergen:"eggs"
preparation:"10 minutes"
cooking:"15 minutes"
servings:"4"
author:"Admin"
```

Example of Schema for Users:
```
_id:ObjectId("5d55c2b6c4972d7a816b9233")
name:"admin"
password:Binary('JDJiJDEyJFFjRS45VlkyNkt2ZFpGdjRoS1dXSS5HQzd5d1V5NHlYTzJ0cmFRaUovd0QyRGhkV24ubUVt')
```


[**To top**](#Table-of-Contents)

# Technologies used
## Languages
- HTML5
- Python 3
- CSS3
- JavaScript

## Tools
- [Visual Studio Code](https://code.visualstudio.com/) code editor
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) NoSql document oriented database.
- [GitHub](https://github.com/) hosting
- [Browserstack](https://www.browserstack.com/) testing all browsers and devices
- [Git](https://www.atlassian.com/git/tutorials/install-git) version control

## Libraries
- [JQuery](https://jquery.com) to simplify DOM manipulation.
- [Flask](https://flask.palletsprojects.com/en/1.0.x/) to redirect and render pages.
- [Bootstrap](https://www.bootstrapcdn.com/) Simplify the structure of the website and make the website responsive easily.
- [Jinja](http://jinja.pocoo.org/docs/2.10/) displaying data from the backend
- [FontAwesome](https://www.bootstrapcdn.com/fontawesome/) icons
- [Google Fonts](https://fonts.google.com/) font styling


[**To top**](#Table-of-Contents)

## **Testing**
### Manual Testing
- Home page
   - Text, controls and images are aligned properly
   - Color, shading, and gradient are consistent
   - Font size, style and color are consistent for each type of text
   - Text, images, controls, and frames do not run into the edges of the screen.
   - Typed text (data entry) scrolls and displays properly
   - Pages are readable on all resolutions.
   - Search by: button opens modal and searches each selector properly.
   - linkedin and githubs redirect correctly.
   - Title link goes to home page.

- Recipes page
   - Cards are displaying correct data.
   - Read more button connects to single recipe page.
   - Search by: button opens modal and searches each selector properly.

- My Recipes page
   - Displays that signed in users recipes only.
   - Edit button connects to edit page and updates information correctly.
   - Delete button deletes that recipe from the collection.

- Add Recipe page
   - form requires all fields to be infilled.
   - add entry button submits to the collection in mongoDB and gives feedback of 'recipe added'
   - Dropdown selectors function correctly.

- Log in and Log out
   - log in signs that user into there account enabling that user to see their 'my recipes' section and the option to add recipes. user is flash messaged 'sign in successful'
   - log out pops the session removing the option to add recipes and see their 'my recipes section' user is flash messaged 'logged out successfully'
   - Sign up here link sends user without and account to create account page. user is flash messages 'account created successfullly'
- Register / Create and Account
   - warns users if that username is already taken
   - warns users if password is not the same after entering password in both input fields
   - register button submits that entry into the MongoDB collections
- Flash messaging give the usere feedback
   - [flash message images](https://github.com/CaseyScott/taste-recipe/tree/master/static/img/FlashMessaging)

#### Browser Testing 
All testing on the list of Browers below.
- Google Chrome (no issues found at time of testing)
- Firefox (issue with text-align:-webkit-center on single recipe page instructions should all be centered)
- Internet Explorer & Edge (issue with text-align:-webkit-center on single recipe page instructions should all be centered)
- Opera (no issues found at time of testing)

#### Responsive-Design testing
Responsive testing done on Google DevTools – Device Mode and Browserstack.


## **Deployment**
- **Heroku**
   - Create a new app `taste-recipe`
- **In the terminal:**
   -log into heroku with `heroku login` using username and password.   
   - initialise a git repository `git init`
   -link the GitHub repo to the app in heroku `git remote add heroku https://https://taste-recipe.herokuapp.com//` 
   - creates a txt file with all the dependencies to run the app `pip3 freeze --local > requirements.txt`
   - This is a web app that will run on app.py `echo web: python run.py >procfile` .
   - will scale your app to one running dyno `ps:scale web=1`
   
- **In app.py set the app.config variables so Heroku can find them.**
   ```python
   app.secret_key = os.environ.get('SECRET_KEY')
   app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
   app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
   ```
- **In the terminal line entered:**
  
  - `git add`
  - `git commit -m "message"`
  - `git push -u heroku master` pushes the project to Heroku.
 
- **In Heroku:**
   - Go to the project > setting > config vars
   ```
   IP = `0.0.0.0`
   PORT =  `5000`
   SECRET_KEY = |secret key|
   MONGO_DBNAME = |database name|
   MONGO_URI = mongodb+srv://|user:password|@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority
   ```
   - More > restart all dynos

[**To top**](#Table-of-Contents)


## **How to run the project locally?**
To run this project these instructions are given for a code editor I am using [Visual Studio Code](https://code.visualstudio.com/) on a windows machine.

You will need:
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) 
- [Python 3](https://www.python.org/downloads/)
- [Git](https://www.atlassian.com/git/tutorials/install-git)
- [Pip](https://www.liquidweb.com/kb/install-pip-windows/)

### How to get started
1. From Github repository [Resturant Chef Repo](https://github.com/CaseyScott/taste-recipe) download.zip and extract to your chosen destination.

2. Using python in VS code you need to set up a virtual environment. check to see if pip is installed with pip -h get help setting up [environment](https://uoa-eresearch.github.io/eresearch-cookbook/recipe/2014/11/26/python-virtual-env/)
Install the virtualenv package
- pip install virtualenv  

Create the virtual environment
- virtualenv mypython

Activate the virtual environment
- mypython\Scripts\activate

3. install all requirements needed to run this app using
```
pip install -r requirements.txt.
```

4. Create a file called config.py 
In the terminal line enter `echo 'config.py' > gitignore` to hide the `config.py` file.
In this file you will need to enter the following:
```
DB_CONFIG = {   
    "MONGO_DBNAME": |yourdatabasename|,
    "MONGO_URI": "mongodb+srv://|yourusername|:|yourpassword|r@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority",
    "SECRET_KEY": |yoursecretkey|,
    "IP": "0.0.0.0",
    "PORT": 5000
}
```
5. Create app.py file
In app.py, set the app.config variables to the variables set in the config.py file
    import config
    ```
    app.config["MONGO_DBNAME"] = config.DB_CONFIG['MONGO_DBNAME']
    app.config["MONGO_URI"] = config.DB_CONFIG['MONGO_URI']
    app.secret_key = config.DB_CONFIG['SECRET_KEY']
    ```
6. In the terminal line enter:
  - `python -m flask run`   which will run on `http://127.0.0.1:5000`



[**To top**](#Table-of-Contents)

### Code Used
- code templates used for [cards](https://coreui.io/docs/components/cards/) 
- index page layout theme [bootstrap theme](https://startbootstrap.com/themes/)
- code templates used for [modals](https://getbootstrap.com/docs/4.0/components/modal/)
- code templates used for [dropdowns](https://getbootstrap.com/docs/4.0/components/dropdowns/)
- code templates for [sign in and registration](https://bootsnipp.com/tags/login)
- search by ingredients route was written by my Tutor:
```
@app.route("/ingredients_search", methods=['GET','POST'])
def ingredients_search():
    regex = re.compile(r'.*{0}.*'.format(request.form.get("ingredient_search")), re.IGNORECASE)
    recipesByIngredients=mongo.db.recipes.find(
        {"ingredients": {"$regex": regex}})
    return render_template(
        'pages/search_results.html',
        recipes=recipesByIngredients,
        meal_types_file=meal_types_file,
        allergens_file=allergens_file)
```

## **Credits**
### Special thanks to
My Tutor and Mentor, Dick Vlaanderen and the Code Institute tutors for helping me Throughout this project.

### Recipes
- The recipes used are from [The Meal DB](https://https://www.themealdb.com/api.php) 
- Other needed information on recipes I used general google search

### Media
- Font Awesome for icons
- Main index picture from [The Meal DB](https://https://www.themealdb.com/api.php)

### Git for version control and pushing to GitHub
- Each commit should be used to save each new change to keep record of what changes have been made. 
Throughout this project dew to my split shifts between study early morning, work through the day, study after work and into the evening I have used both git (saving locally) and pushing to github as more of a general save option as getting stuck on a problem meant I had to commit broken or unfinished code and push to github to have it reviewed to get help in a 24hour cycle as my time zoning is 12 hours out of loop with students and tutors. I have a greater understanding of version control than what I have used in this project.