
import csv
from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from datetime import datetime

class CSVDataReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.nutriID_count = 1

    def read_recipes(self):
        recipes = []
        with open(self.file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                # nutrition id - since it don't have id, I put incremental id instead
                nutriID = self.nutriID_count
                self.nutriID_count += 1

                # Recipe: id, name, description, ingredients, instructions, cookingTime
                id = int(row[0].strip())
                name = row[1].strip()
                description = row[8].strip()
                ingredients = [row[12].strip()]
                instructions = [row[24].strip()]
                cookingTime = int(row[4].strip())
                preparationTime = int(row[5].strip())
                datePublished = datetime(row[7].strip())
                imagesLink = [row[9].strip()]
                ingrQuantities = [row[11].strip()]
                servings = row[22].strip()
                recipeYield = row[23].strip()
                rating = int(input("Enter your rating: "))

                # Author: id, name
                author = Author(int(row[2]), str(row[3]), [])
                # declare category
                category = Category(row[10].strip(), [])
                # declare: cal, fat, saturated fate, cholesterol, sodium, carbohydrate, fiber, sugar, protein
                nutrition = Nutrition(nutriID, float(row[13]), float(row[14]), float(row[15]), float(row[16]), float(row[17]),
                                      float(row[18]), float(row[19]), float(row[20]), float(row[21]))
                recipe = Recipe(id, name, author, cookingTime, preparationTime, datePublished, description, imagesLink, category,
                                ingrQuantities, ingredients, rating, nutrition, servings, recipeYield, instructions)

                # list of recipes: category
                category.add_recipe(recipe)
                # list of recipes: author
                author.add_recipe(recipe)
                recipes.append(recipe)
        return recipes

# main
if __name__ == "__main__":
    reader = CSVDataReader("recipe/adapters/data/recipes.csv")
    recipes = reader.read_recipes()
    for r in recipes:
        print(f"{r.name} by {r.author.name} [{r.category.name}] -> {r.nutrition.calories} cal")

