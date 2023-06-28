from flask import Flask, Request, Response, jsonify, request
import json
from data_types.dishes import Dishes
from data_types.dish import Dish
from data_types.meal import Meal
from data_types.meals import Meals
from invoker.invoker import Invoker

dishes = Dishes()
meals = Meals()
id_dishes_counter = 0
id_meals_counter = 0


app = Flask(__name__)


@app.route("/dishes", methods=["GET"])
def get_dishes() -> Response:
    response = jsonify(dishes.to_dict())
    response.status_code = 200
    return response

def is_id(search_parameter: str) -> bool:
    return search_parameter.isdigit()

def handle_get_id(id: str) -> Response:
    if int(id) > 0:
        dish = dishes.get_dish_by_id(int(id))
        if dish is not None:
            response = jsonify(dish.to_dict())
            response.status_code = 200
            return response
    return jsonify(-5), 404

def handle_get_name(name: str) -> Response:
    dish = dishes.get_dish_by_name(name)
    if dish is not None:
        response = jsonify(dish.to_dict())
        response.status_code = 200
        return response
    return jsonify(-5), 404

@app.route("/dishes/<search_parameter>", methods=["GET"])
def get_dish_by_id(search_parameter: str) -> Response:
    if is_id(search_parameter):
        return handle_get_id(search_parameter)
    else:
        return handle_get_name(search_parameter)
    
@app.route("/dishes/<search_parameter>", methods=["DELETE"])
def delete_dish(search_parameter: str) -> Response:
    if is_id(search_parameter):
        return handle_delete_id(int(search_parameter))
    else:
        return handle_delete_name(search_parameter)
    
    
def handle_delete_id(id: int) -> Response:
    if dishes.remove_by_id(id):
        meals.delete_dish(id)
        return jsonify(id), 200
    return jsonify(-5), 404


def handle_delete_name(name: str) -> Response:
    if dishes.get_dish_by_name(name) != None:
        id = dishes.get_dish_by_name(name).id
        meals.delete_dish(id)
        dishes.remove_by_name(name)
        return jsonify(id), 200
    return jsonify(-5), 404

@app.route("/dishes", methods=['POST'])
def save_new_dish() -> Response:
    if not validate_content_type(request):
        return jsonify(0), 415
    content = parse_request(request)
           
    if not dishes.validate_dish(content):
        return jsonify(-1), 422
    
    if dishes.get_dish_by_name(content["name"]) is not None:
        return jsonify(-2), 422

    invoker = Invoker()
    response = invoker.invoke(content['name'])
    if response.status_code == 200:
        body = json.loads(response.content)
        if not body:
            return jsonify(-3), 422
        parsed_dishes = build_dishes(body)
        if parsed_dishes is not None:
            for dish in parsed_dishes:
                dishes.append(dish)
            return jsonify(dish.id), 201
    return jsonify(-4), 504

def build_dishes(body: list) -> list:
    parsed_dishes = []
    for raw_dish in body:
        if not dishes.get_dish_by_name(raw_dish["name"]):
            global id_dishes_counter
            id_dishes_counter += 1
            dish = Dish(raw_dish["name"], id_dishes_counter, raw_dish["calories"],
                raw_dish["serving_size_g"], raw_dish["sodium_mg"], raw_dish["sugar_g"])
            parsed_dishes.append(dish)
    if len(parsed_dishes) == 0:
        return None
    return parsed_dishes

@app.route("/dishes", methods=["DELETE"])
def delete_dishes():
    return jsonify("This method is not allowed for the requested URL"), 405

def validate_content_type(request: Request) -> bool:
    return request.content_type == "application/json"


def parse_request(request: Request) -> dict:
    body = request.data
    body_str = body.decode('utf-8')
    return json.loads(body_str)


@app.route("/meals", methods=['GET'])
def get_meals()-> Response:
    response = jsonify(meals.to_dict())
    response.status_code = 200
    return response

@app.route("/meals", methods=['POST'])
def save_new_meal() -> Response:
    response, is_valid = validate_request(request)
    if not is_valid:
        return response
    meal = build_meal(parse_request(request))
    meals.append(meal)
    return jsonify(meal.id), 201

@app.route("/meals/<search_parameter>", methods=['GET'])
def get_meal(search_parameter: str) -> Response:
    if is_id(search_parameter):
        return handle_get_meal_id(int(search_parameter))
    else:
        return handle_get_meal_name(search_parameter)
    
def handle_get_meal_id(id: int) -> Response:
    if int(id) > 0:
        meal = meals.get_meal_by_id(id)
        if meal is not None:
            response = jsonify(meal.to_dict())
            response.status_code = 200
            return response
    return jsonify(-5), 404

def handle_get_meal_name(name: str) -> Response:
    meal = meals.get_meal_by_name(name)
    if meal is not None:
        response = jsonify(meal.to_dict())
        response.status_code = 200
        return response
    return jsonify(-5), 404

@app.route("/meals/<search_parameter>", methods=['DELETE'])
def delete_meal(search_parameter: str) -> Response:
    if is_id(search_parameter):
        return handle_delete_meal_id(int(search_parameter))
    else:
        return handle_delete_meal_name(search_parameter)
    
def handle_delete_meal_id(id: int) -> Response:
    if meals.remove_by_id(id):
        return jsonify(id), 200
    return jsonify(-5), 404


def handle_delete_meal_name(name: str) -> Response:
    if meals.get_meal_by_name(name) != None:
        id = meals.get_meal_by_name(name).id
        meals.remove_by_name(name)
        return jsonify(id), 200
    return jsonify(-5), 404

@app.route('/meals/<id>', methods=['PUT'])
def handle_update_meal(id: str) -> Response:
    response, is_valid = validate_request(request)
    if not is_valid:
        return response
    update_meal = build_meal(parse_request(request))
    meals.update_meal(int(id), update_meal)
    return jsonify(int(id)), 200
    

def validate_request(request: Request) -> tuple:
    if not validate_content_type(request):
        return ((jsonify(0), 415), False)
    content = parse_request(request)
    if not validate_meal_body(content):
        return ((jsonify(-1), 422), False)
    if request.method == "POST" and meals.get_meal_by_name(content["name"]):
        return ((jsonify(-2), 422), False)
    if not can_build_meal(content):
        return ((jsonify(-6), 422), False)
    else:
        return None, True


def build_meal(content: dict) -> Meal:
    global id_meals_counter
    id_meals_counter += 1
    meal_name = content["name"]
    appetizer = dishes.get_dish_by_id(content["appetizer"])
    main = dishes.get_dish_by_id(content["main"])
    dessert = dishes.get_dish_by_id(content["dessert"])
    return Meal(id_meals_counter, meal_name, appetizer, main, dessert)

def can_build_meal(content: dict) -> bool:
    return dishes.get_dish_by_id(content["appetizer"]) and dishes.get_dish_by_id(content["main"]) and dishes.get_dish_by_id(content["dessert"])

def validate_meal_body(content: dict) -> bool:
    return "name" in content and "appetizer" in content and "main" in content and "dessert" in content



if __name__ == '__main__':
    app.run(debug=True)