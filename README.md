# Issues found 

1. `base.thml`  
   Redundant `</script>` tag found 
1. `base.html`:
   <br>
   Materialize was included before jQuery
   Caused the following javascript error:
   <br>
   `materialize.min.js:6 Uncaught ReferenceError: $ is not defined
    at materialize.min.js:6`
1. `static/jquery/jquery.js`  
   After moving Materialize to after jQuery was loaded, 
   the following error showed: 
   <br>
   `jquery-3.4.1.min.js:2 Uncaught TypeError: Materialize.updateTextFields is not a function
    at HTMLDocument.<anonymous> (jquery.js:4)
    at e (jquery-3.4.1.min.js:2)
    at t (jquery-3.4.1.min.js:2)`
    <br>
    This is caused by using `Materialize.updateTextFields` 
    in `static/jquery/jquery.js`
    Remedy: Move the loading of this file after loading 
    Materialize.
1. `static/jquery/jquery.js`:  
   `Uncaught TypeError: $(...).formSelect is not a function
    at HTMLDocument.<anonymous> (jquery.js:7)
    at e (jquery-3.4.1.min.js:2)
    at t (jquery-3.4.1.min.js:2)`
    <br>
    Where is `formSelect` defined?
    <br>
    Statement disabled
1. `static/jquery/jquery.js`:  
   `Uncaught TypeError: $(...).vasl is not a function
    at HTMLDocument.<anonymous> (jquery.js:8)
    at e (jquery-3.4.1.min.js:2)
    at t (jquery-3.4.1.min.js:2)`  
    Spelling mistake
1.  `add.py`:  
    ```python  
    return render_template(  
        'recipes.html',
        recipes=all_recipes,
        cuisine_json=cuisine_json,
        allergens_json=allergens_json,
        usernames=usernames)
    ```
    `all_recipes` not defined
    
    
## Hints
1.  `static/jquery/jquery.js`
    <br>
    Better practice is not to name javascript files the same as in 
    included third party library.
