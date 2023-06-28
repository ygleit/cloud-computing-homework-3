from data_types.dish import Dish
class Dishes():
    def __init__(self) -> None:
        self.dishes = []

    def append(self, dish: Dish) -> bool:
        if dish not in self.dishes:
            self.dishes.append(dish)
            return True
        return False
    
    def remove_by_id(self, id: int) -> bool:
        for dish in self.dishes:
            if dish.id == id:
                self.dishes.remove(dish)
                return True
        return False
    
    
    def remove_by_name(self, name: str) -> bool:
        for dish in self.dishes:
            if dish.name == name:
                self.dishes.remove(dish)
                return True
        return False

    
    def update(self, dish: Dish) -> bool:
        if self.remove(dish):
            return self.append(dish)
        return False
    
    def get_dish_by_id(self, id: int) -> Dish:
        for dish in self.dishes:
            if dish.id == id:
                return dish
        return None
    
    def get_dish_by_name(self, name: str) -> Dish:
        for dish in self.dishes:
            if dish.name == name:
                return dish
        return None
    
    def to_dict(self) -> dict:
        return {str(dish.id) : dish.to_dict() for dish in self.dishes}
    
    def validate_dish(self, content) -> bool:
            return "name" in content
