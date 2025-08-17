import csv

class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_recipes(self):
        recipes = []
        with open(self.file_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # skip header
            for row in reader:
                # Recipe: id, name, description, ingredients, instructions, cookingTime
                id = row[0].strip()
                name = row[1].strip()
                description = row[8].strip()
                ingredients = row[12].strip()
                instructions = row[24].strip()
                cookingTime = row[4].strip()

                # Author: id, name
                author = Author(str(row[2]), str(row[3]))
                # declare category
                category = Category(row[10].strip())
                # declare: cal, fat, saturated fate, cholesterol, sodium, carbohydrate, fiber, sugar, protein
                nutrition = Nutrition(float(row[13]), float(row[14]), float(row[15]), float(row[16]), float(row[17]), float(row[18]), float(row[19]), float(row[20]), float(row[21]))
                recipe = Recipe(id, name, author, description, ingredients, instructions, cookingTime, category, nutrition)

                #list of recipes: category
                category.add_recipe(recipe)
                #list of recipes: author
                author.add_recipe(recipe)
                recipes.append(recipe)
        return recipes

class Recipe:
    def __init__(self, id, name, author, description, ingredients, instructions, cookingTime, category, nutrition):
        self.id = id
        self.name = name
        self.author = author
        self.description = description
        self.ingredients = ingredients
        self.instructions = instructions
        self.cookingTime = cookingTime
        self.category = category
        self.nutrition = nutrition

class Author:
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

class Category:
    _nextID_ = 1

    def __init__(self, name):
        #id
        self.id = Category._nextID_
        Category._nextID_ += 1

        #attributes
        self.name = name
        self.recipes = []

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

class Nutrition:
    _nextID_ = 1
    def __init__(self, calories, fat, saturated_fate, cholesterol, sodium, carbohydrate, fiber, sugar, protein):
        #id
        self.id = Nutrition._nextID_
        Nutrition._nextID_ += 1

        #attributes
        self.calories = calories
        self.fat = fat
        self.saturated_fate = saturated_fate
        self.cholesterol = cholesterol
        self.sodium = sodium
        self.carbohydrate = carbohydrate
        self.fiber = fiber
        self.sugar = sugar
        self.protein = protein

# main
if __name__ == "__main__":
    reader = CSVReader("recipes.csv")
    recipes = reader.read_recipes()
    for r in recipes:
        print(f"{r.name} by {r.author.name} [{r.category.name}] -> {r.nutrition.calories} cal")
