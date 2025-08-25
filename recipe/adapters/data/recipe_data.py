from recipe.adapters.datareader.csvreader import CSVReader
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "recipes.csv")
reader = CSVReader(csv_path)
reader.extract_data()

recipes = reader.get_recipes()
categories = reader.get_categories()
nutrition = reader.get_nutrition()
authors = reader.get_authors()