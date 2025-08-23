import os
import csv
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe


class CSVDataReader:
    # TODO: Complete the implementation of the CSVDataReader class.
    pass

def create_recipes() -> list[Recipe]:
    author1 = Author(1024, "sid")
    recipe1 = Recipe(24, "Coke", author1,description= "it is cool", ingredients= ["happy", "love"], instructions=["do this", "then this", "and this"],images="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/12/9/picI35rA2.jpg")

    author2 = Author(2048, "cool_sid")
    recipe2 = Recipe(48, "Pepsi", author2, description="this is even cooler", ingredients=["double_happy", "love"], instructions=["secret"], images="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/16/7/pictKxvMg.jpg")

    author3 = Author(4096, "sid")
    recipe3 = Recipe(8192, "Coke", author3, description="this is different kind of coke", ingredients=["happy", "happy", "illusion"], instructions=["not something you can make at home"], images="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/84/pickFstbF.jpg")

    author4 = Author(512, "sid")
    recipe4 = Recipe(12, "Coke", author3, description="this is different kind of coke",
                     ingredients=["happy", "happy", "illusion"], instructions=["not something you can make at home"],
                     images="https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/84/pickFstbF.jpg")

    return [recipe1, recipe2, recipe3, recipe4]
c1 = Category("Coke")
c2 = Category("Pepsi")
c3 = Category("coconut")
list_of_categories = [c1, c2, c3]
list_of_recipes = create_recipes()
