
class Dish:
    def __init__(self, name: str, id: int, cal: float, size: float, sodium: float, sugar: float) -> None:
        self.name = name
        self.id = id
        self.cal = cal
        self.size = size
        self.sodium = sodium
        self.sugar = sugar

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Dish):
            return self.id == __value.id
    
    def to_dict(self) -> dict:
        return {
            "name" : self.name,
            "ID": self.id,
            "cal": self.cal,
            "sodium": self.sodium,
            "sugar": self.sugar,
            "size": self.size
        }        
    
    def __repr__(self) -> str:
        return f"Dish(name={self.name} id={self.id}, cal={self.cal}, size={self.size}, sodium={self.sodium}, sugar={self.sugar})"