import requests, json, jsonify, random, os, logging, datetime
from flask import Flask, render_template, request

# UTILITY FUNCTIONS
def save_JSON(filename, data):
    directory = "json"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f"{directory}/{filename}", 'w') as f:
        json.dump(data, f, indent=4)

def start_logger():
    logger = logging.getLogger('API_call_logger')
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler('API_calls.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger
logger = start_logger()

def log_API_call(logger, call_type, query, content):
    current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'[{current_time}] API call made of type={call_type}\nquery={ascii(query)}\ncontent={ascii(content)}')

# 'COCKTAIL DB' API FUNCTIONS
def search_cocktail_by_name(name):
    global logger
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
    params = {"s": name}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_cocktail_by_name.json', data)
    log_API_call(logger, "search_cocktail_by_name", name, data)
    return data

def search_ingredient_by_name(name):
    global logger
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php"
    params = {"i": name}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_ingredient_by_name.json', data)
    log_API_call(logger, "search_ingredient_by_name", name, data)
    return data

def search_cocktail_by_ID(id):
    global logger
    url = "https://www.thecocktaildb.com/api/json/v1/1/lookup.php"
    params = {"i": id}
    response = requests.get(url, params=params)
    data = response.json()
    save_JSON('search_cocktail_by_ID.json', data)
    log_API_call(logger, "search_cocktail_by_ID", id, data)
    return data

def search_random_cocktail():
    global logger
    url = "https://www.thecocktaildb.com/api/json/v1/1/random.php"
    response = requests.get(url)
    data = response.json()
    save_JSON('search_random_cocktail.json', data)
    log_API_call(logger, "search_random_cocktail", "search_random_cocktail", data)
    return data

app = Flask(__name__)

# HOMEPAGE RESPONSE
@app.route('/', methods=['GET', 'POST'])
def homepage():
    cocktail_img = "https://www.thecocktaildb.com/images/media/drink/vyxwut1468875960.jpg"
    if request.method == 'POST':
        query_type = request.form['search_option']
        query = request.form['search_term']
        # print(f"\n\nquery_type={query_type}\n\n")
        # print(f"\n\nquery={query}\n\n")
        if query_type == "cocktail_name":
            # print("\n\nNEW QUERY - TYPE 1\n\n")
            results = json_drink_search(query)
        elif query_type == "cocktail_ingredient":
            # print("\n\nNEW QUERY - TYPE 2\n\n")
            results = json_ingredient_search(query)
        elif query_type == "cocktail_id":
            # print("\n\nNEW QUERY - TYPE 3\n\n")
            results = json_drink_ID(query)

        titles = []
        for drink in results['drinks']:
            titles.append(drink['strDrink'])

        cards = [{"title": title, "description": "This is a card description."} for title in titles]
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
def json_all_drinks():
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
