from pydantic import BaseModel
from enum import Enum
from uuid import UUID,uuid4

class DrinkEnum(str, Enum):  
    coffee: str = "coffee"  
    soda: str = "soda"  
    beer: str = "beer"  
    wine: str = "wine"  
  
  
class MealEnum(str, Enum):  
    pasta: str = "pasta"  
    pizza: str = "pizza"  
    meat: str = "meat"  
    fish: str = "fish"  
  
  
class DessertEnum(str, Enum):  
    cookie: str = "cookie"  
    donut: str = "donut"  
    brownie: str = "brownie"  
    gelato: str = "gelato"  
    
  
class OrderCreate(BaseModel):  
    order_id: UUID = uuid4()  
    drink: DrinkEnum  
    meal: MealEnum  
    dessert: DessertEnum