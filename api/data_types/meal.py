from data_types.dish import Dish

class Meal():
    def __init__(self, id: int, name: str, appetizer: Dish, main: Dish, dessert: Dish) -> None:
        self.id = id
        self.name = name
        self.appetizer  = appetizer
        self.main = main
        self.dessert = dessert

    def to_dict(self) -> dict:
        return {
            "name" : self.name,
            "ID": self.id,
            "appetizer": self.check_field("appetizer"),
            "main": self.check_field("main"),
            "dessert": self.check_field("dessert"),
            "cal": self.caclulate_caloris(),
            "sodium": self.caclulate_sodium(),
            "sugar": self.calculate_sugar()
        }
    
    def check_field(self, field_name: str) -> None:
        if field_name == "appetizer" and self.appetizer is not None:
            return self.appetizer.id
        if field_name == "main" and self.main is not None:
            return self.main.id
        if field_name == "dessert" and self.dessert is not None:
            return self.dessert.id
        return None
    

    def caclulate_caloris(self) -> float:
        sum = 0
        if self.appetizer is not None:
            sum += self.appetizer.cal
        if self.dessert is not None:
            sum += self.dessert.cal
        if self.main is not None:
            sum += self.main.cal    
        return sum


    def caclulate_sodium(self) -> float:
        sum = 0
        if self.appetizer is not None:
            sum += self.appetizer.sodium
        if self.dessert is not None:
            sum += self.dessert.sodium
        if self.main is not None:
            sum += self.main.sodium
        return sum


    def calculate_sugar(self) -> float:
        sum = 0
        if self.appetizer is not None:
            sum += self.appetizer.sugar
        if self.dessert is not None:
            sum += self.dessert.sugar
        if self.main is not None:
            sum += self.main.sugar    
        return sum
