[Restaurant Chef](https://taste-recipe.herokuapp.com/)

# **Table of Contents**

- [**Table of Contents**](#table-of-contents)
	- [**Restaurant Chef**](#restaurant-chef)
	- [**Given Brief**](#brief)
	- [**UX**](#ux)
		- [**Requirements**](#requirements)
			- [Database](#database)
			- [Users](#users)
			- [Pages](#pages)
		- [**General Design**](#general-design)
	- [**Features**](#features)
		- [Existing features](#existing-features)
			- [Database existing features](#database-existing-features)
			- [Existing pages](#existing-pages)
			- [Helper](#helper)
		- [Features left to implement](#features-left-to-implement)
	- [**Technologies used**](#technologies-used)
		- [Front End](#front-end)
		- [Back End](#back-end)
	- [**Testing**](#testing)
		- [Tools used for testing](#tools-used-for-testing)
	- [**Changelog and Fixes**](#changelog-and-fixes)
	- [**Deployment**](#deployment)
	- [**How to run the project locally?**](#how-to-run-the-project-locally)
	- [**What could be done better?**](#what-could-be-done-better)
	- [**Credits**](#credits)
		- [Special thanks to](#special-thanks-to)
		- [Recipes](#recipes)
		- [Media](#media)

<hr />

## **Restaurant-Chef**

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
I aimed for simple and moden interface with plan easy to use forms for registration, sign in, add recipe and edit recipe.

## **User Stories**


## Wireframes

#### Database

#### Users


#### Pages


### **Design**


## **Features**

[**To top**](#Table-of-Contents)

### Features left to implement

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
- [Flask](https://flask.palletsprojects.com/en/1.0.x/) to construct and render pages.
- [Bootstrap](https://www.bootstrapcdn.com/) Simplify the structure of the website and make the website responsive easily.
- [Jinja](http://jinja.pocoo.org/docs/2.10/) displaying data from the backend
- [FontAwesome](https://www.bootstrapcdn.com/fontawesome/) icons
- [Google Fonts](https://fonts.google.com/) font styling



### Front End


### Back End
[**To top**](#Table-of-Contents)

## **Testing**

### Tools used for testing

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

<hr />

## **How to run the project locally?**
To run this project these instructions are given for a code editor I am using [Visual Studio Code](https://code.visualstudio.com/)on a windows machine.

You will need:
- A MongoDB account [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
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
- mypthon\Scripts\activate

3. install all requirements needed to run this app using
```
pip -r requirements.txt.
```

4. Create a file called config.py 
In the terminal line enter `echo 'config.py' > gitignore` to hide the `config.py` file.
In this file you will need to emter the following:
DB_CONFIG = {   
    "MONGO_DBNAME": |yourdatabasename|,
    "MONGO_URI": "mongodb+srv://|yourusername|:|yourpassword|r@cluster0-uoefk.mongodb.net/data?retryWrites=true&w=majority",
    "SECRET_KEY": |yoursecretkey|,
    "IP": "0.0.0.0",
    "PORT": 5000
}

5. Create app.py file
In app.py, set the app.config variables to the variables set in the config.py file
    import config
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



### Recipes
- The recipes used are from [The Meal DB](https://https://www.themealdb.com/api.php) 
- other needed information on recipes I used general google search

### Media
- Font Awesome for icons
- main index picture from [The Meal DB](https://https://www.themealdb.com/api.php)

[**To top**](#Table-of-Contents)

## **Credits**

### Special thanks to
## helpful pages I used

- Rendering Templates 
https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates

- Adding input fields Dynamically || https://www.youtube.com/watch?v=jSSRMC0F6u8

- $regex
https://docs.mongodb.com/manual/reference/operator/query-evaluation/

- request.form.getlist
https://stackoverflow.com/questions/14188451/get-multiple-request-params-of-the-same-name

- case sensitive caseInsensitive
https://stackoverflow.com/questions/10700921/case-insensitive-search-with-in

- mongo return documents without a specific value
https://docs.mongodb.com/manual/reference/operator/query/nin/

- Query MongoDB with $and and Multiple $or
https://stackoverflow.com/questions/40388657/query-mongodb-with-and-and-multiple-or

- Validation - check to make sure at least one field is filled out
https://www.sitepoint.com/community/t/validation-check-to-make-sure-at-least-one-field-is-filled-out/2329

- Javascript - How to check if a typed image URL really exists
https://stackoverflow.com/questions/24577534/javascript-how-to-check-if-a-typed-image-url-really-exists

- simple sign in and sign out 
https://gist.github.com/daGrevis/2427189

- sccess session variables in jinja 2
https://stackoverflow.com/questions/42013067/how-to-access-session-variables-in-jinja-2-flask