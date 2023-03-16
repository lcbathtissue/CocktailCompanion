# Cocktail Search App

This is a Flask-based web app that allows users to search for cocktails by name, ingredient, or ID. The app uses data from the 'Cocktail DB' API.

## Dependencies

The app requires the following dependencies:

* Flask
* Requests
* Jsonify

To install the dependencies, run:

pip install flask requests jsonify

## Usage

Usage:
To run the app, navigate to the project directory and run:

python CocktailCompanion.py

This will start the Flask server and you can access the app by visiting http://localhost:5000/ in your web browser.

## Home Page
The home page allows users to search for cocktails by name, ingredient, or ID. Users can select their search type from a dropdown menu and enter their search term in the input field.

## Drink Page
The drink page shows the details of a particular drink, identified by its ID.

## Ingredient Page
The ingredient page shows the details of a particular ingredient, identified by its name.

## JSON Endpoints
The app also provides JSON endpoints for the search results:

/json/drinks: returns a list of all drinks
/json/drink_name/<name>: returns the details of drinks matching the given name
/json/ingredient_name/<name>: returns the details of ingredients matching the given name
/json/drink_ID/<ID>: returns the details of the drink with the given ID
/json/drink/random: returns the details of a random drink

## License
This app is licensed under the MIT license. See LICENSE for more details.
