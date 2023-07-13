from assertions import *
import database
import connectionController
import json


URL = "http://127.0.0.1:8000"

def http_post(resource: str, data: {}):
    response = requests.post(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"}, data=json.dumps(data))
    return response

def http_get(resource: str):
    response = requests.get(url=f"{URL}/{resource}", headers={"Content-Type": "application/json"})
    return response


def add_dish(name: str) -> int:
    dish = {"name": name}
    response = http_post("dishes", dish)
    assert_valid_added_resource(response)
    return response.json()


def add_meal(name: str, appetizer_id: int, main_id: int, dessert_id: int) -> int:
    meal = {
        "name": name,
        "appetizer": appetizer_id,
        "main": main_id,
        "dessert": dessert_id
    }
    response = connectionController.http_post("meals", meal)
    assert_valid_added_resource(response)
    return response.json()



def assert_err_code_three_options(response: requests.Response):
    expected_error_codes = [404, 400, 422]
    assert response.status_code in expected_error_codes



def assert_valid_added_resource(response: requests.Response):
    assert response.status_code == 201
    # should be positive ID
    VALID_RETURNED_RESOURCE_ID = 0
    assert response.json() > VALID_RETURNED_RESOURCE_ID



# test 1
def test_check_three_posts():

    assert add_dish("orange") > 0, "Failed to add 'orange' dish."
    assert add_dish("spaghetti") > 0, "Failed to add 'spaghetti' dish."
    assert add_dish("apple pie") > 0, "Failed to add 'apple pie' dish."

    print("All dishes added successfully!")

# test 2
def test_get_dish_by_id():
    orange_dish =  connectionController.http_get("dishes/orange")
    orange_data = orange_dish.json()
    orange_id = orange_data["ID"]
    response = connectionController.http_get(f"dishes/{orange_id}")
    assert_err_code(response, error_code=200)
    assert_dish(response.json(), database.ORANGE)

# test 3
def test_get_all_dishes():
    response = connectionController.http_get("dishes")
    assert_err_code(response, error_code=200)

    DISH_INDEX = "1"
    dishes = response.json()
    assert len(dishes) > 0

    first_dish = dishes[DISH_INDEX]

    assert "ID" in first_dish
    assert "name" in first_dish
    assert "cal" in first_dish
    assert "size" in first_dish
    assert "sodium" in first_dish
    assert "sugar" in first_dish

    DISH_INDEX = "2"

    second_dish = dishes[DISH_INDEX]

    assert "ID" in first_dish
    assert "name" in first_dish
    assert "cal" in first_dish
    assert "size" in first_dish
    assert "sodium" in first_dish
    assert "sugar" in first_dish

    DISH_INDEX = "3"

    third_dish = dishes[DISH_INDEX]
    assert "ID" in first_dish
    assert "name" in first_dish
    assert "cal" in first_dish
    assert "size" in first_dish
    assert "sodium" in first_dish
    assert "sugar" in first_dish

# test 4
def test_add_blha_all_dishes():

    dish_name = {
    "name": "blah",
}
    response = http_post("dishes",data=dish_name)
    assert_err_code_three_options(response)
    data_value = response.text
    assert "-3" == data_value.strip()

    

# test 5
def test_add_exists_dish():
    DISH_NAME = "orange"
    response = connectionController.http_post("dishes", {"name": DISH_NAME})
    assert_err_code_three_options(response)
    data_value = response.text
    assert "-2" == data_value.strip()

# test 6
def test_add_meal():

    orange_dish =  connectionController.http_get("dishes/orange")
    orange_data = orange_dish.json()
    orange_id = orange_data["ID"]

    spaghetti_dish =  connectionController.http_get("dishes/spaghetti")
    spaghetti_data = spaghetti_dish.json()
    spaghetti_id = spaghetti_data["ID"]

    apple_pie_dish =  connectionController.http_get("dishes/apple pie")
    apple_pie_data = apple_pie_dish.json()
    apple_pie_id = apple_pie_data["ID"]

    meal = {"name": "delicious", "appetizer": orange_id, "main": spaghetti_id, "dessert": apple_pie_id}
    response = connectionController.http_post("meals", meal)

    assert_err_code(response, error_code=201)

    data_value = response.text
    assert 0 < int(data_value.strip())

# test 7
def test_get_meals():
    response = connectionController.http_get("meals")
    assert_err_code(response, error_code=200)

    DISH_INDEX = "1"
    meals = response.json()
    assert len(meals) == 1


    DISH_INDEX = "1"
    meal = meals[DISH_INDEX]
    assert_meal(meal)

    assert 400 <= int(meal["cal"]) <= 500

# test 8

def test_meal_already_exists():

    orange_dish =  connectionController.http_get("dishes/orange")
    orange_data = orange_dish.json()
    orange_id = orange_data["ID"]

    spaghetti_dish =  connectionController.http_get("dishes/spaghetti")
    spaghetti_data = spaghetti_dish.json()
    spaghetti_id = spaghetti_data["ID"]

    apple_pie_dish =  connectionController.http_get("dishes/apple pie")
    apple_pie_data = apple_pie_dish.json()
    apple_pie_id = apple_pie_data["ID"]


    meal = {"name": "delicious", "appetizer": orange_id, "main": spaghetti_id, "dessert": apple_pie_id}
    response = connectionController.http_post("meals", meal)
    expected_error_codes = [400, 422]
    assert response.status_code in expected_error_codes

    assert_ret_value(response, returned_value=-2)





   
