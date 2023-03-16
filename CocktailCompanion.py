import requests, json, jsonify, random
from flask import Flask, render_template, request

# UTILITY FUNCTIONS
def save_JSON(filename, data):
    with open(f"json/{filename}", 'w') as f:
        json.dump(data, f, indent=4)

# 'COCKTAIL DB' API FUNCTIONS
def search_cocktail_by_name(name):
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
    params = {"s": name}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_cocktail_by_name.json', data)
    return data

def search_ingredient_by_name(name):
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
    params = {"i": name}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_ingredient_by_name.json', data)
    return data

def search_cocktail_by_ID(id):
    url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    params = {"i": id}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_cocktail_by_ID.json', data)
    return data

def search_random_cocktail():
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    data = response.json()
    save_JSON('search_random_cocktail.json', data)
    return data

app = Flask(__name__)

# HOMEPAGE RESPONSE
@app.route('/', methods=['GET', 'POST'])
def homepage():
    cocktail_img = "https://www.thecocktaildb.com/images/media/drink/vyxwut1468875960.jpg"
    if request.method == 'POST':
        query_type = request.form['search_option']
        query = request.form['search_term']

        if query_type == "name":
            results = json_drink_search(query)['drinks']
        elif query_type == "ingredient":
            results = json_ingredient_search(query)['ingredients']
        elif query_type == "id":
            results = json_drink_ID(query)['drinks']

        cards = ''
        cards += "test"
        # for result in results:
        #     cards += '<div class="card">'
        #     cards += '<img class="card-img-top" src="'+ cocktail_img +'" alt="Card image cap">'  
        #     cards += '<div class="card-body">'
        #     cards += '<h5 class="card-title">' + result['strDrink'] + '</h5>'
        #     cards += '<p class="card-text">' + result['strInstructions'] + '</p>'
        #     cards += '</div>'
        #     cards += '</div>'
        return render_template('index.html', cards=cards)
    return render_template('index.html')

# PAGE RESPONSES
@app.route('/drink_ID/<drink_ID>')
def show_drink(drink_ID):
    drink_data = search_cocktail_by_ID(drink_ID)
    return render_template('drink.html', drink=drink_data['drinks'][0])

@app.route('/ingredient_name/<ingredient_name>')
def show_ingredient(ingredient_name):
    ingredient_data = search_ingredient_by_name(ingredient_name)
    return render_template('ingredient.html', ingredient_data=ingredient_data['ingredients'][0])

# JSON RESPONSES
@app.route('/json/drinks')
def json_json():
    return search_cocktail_by_name("")

@app.route('/json/drink_name/<name>')
def json_drink_search(drink_name):
    return search_cocktail_by_name(drink_name)

@app.route('/json/ingredient_name/<name>')
def json_ingredient_search(ingredient_name):
    return search_ingredient_by_name(ingredient_name)

@app.route('/json/drink_ID/<ID>')
def json_drink_ID(ID):
    return search_cocktail_by_ID(ID)

@app.route('/json/drink/random')
def json_random_drink():
    return search_random_cocktail()

# START FLASK SERVER
if __name__ == '__main__':
    app.run(debug=True)
