from data_types.meal import Meal
class Meals():

    def __init__(self) -> None:
        self.meals = []

    def append(self, meal: Meal) -> bool:
        if meal not in self.meals:
            self.meals.append(meal)
            return True
        return False
    
    def remove_by_id(self, id: int) -> bool:
        for meal in self.meals:
            if meal.id == id:
                self.meals.remove(meal)
                return True
        return False
    
    def remove_by_name(self, name: str) -> bool:
        for meal in self.meals:
            if meal.name == name:
                self.meals.remove(meal)
                return True
        return False
    
    def get_meal_by_name(self, name: str) -> Meal:
        for meal in self.meals:
            if meal.name == name:
                return meal
        return None 
    
    def get_meal_by_id(self, id: int) -> Meal:
        for meal in self.meals:
            if meal.id == id:
                return meal
        return None

    def to_dict(self) -> dict:
        return { str(meal.id): meal.to_dict() for meal in self.meals}
    
    def delete_dish(self, id: int) -> None:
        for meal in self.meals:
            if meal.appetizer is not None and meal.appetizer.id == id:
                meal.appetizer = None
            elif meal.main is not None and meal.main.id == id:
                meal.main = None
            elif meal.dessert is not None and meal.dessert.id == id:
                meal.dessert = None    

    def update_meal(self, id: int, update_meal: Meal) -> None:
        self.remove_by_id(id)
        update_meal.id = id
        self.append(update_meal)
        self.meals.sort(key=lambda meal: meal.id)
    