from pathlib import Path

from recipe.adapters.datareader.csvreader import CSVReader
from recipe.adapters.repository import AbstractRepository


def populate(data_path: Path, repo: AbstractRepository, database_mode: bool):

    csv_reader = CSVReader(data_path)
    csv_reader.extract_data()
    recipes = csv_reader.get_recipes()
    categories = csv_reader.get_categories()
    nutrition = csv_reader.get_nutrition()
    authors = csv_reader.get_authors()
    instructions = csv_reader.get_instructions()
    images = csv_reader.get_images()
    ingredients = csv_reader.get_recipe_ingredients()

    repo.add_multiple_recipe(recipes)
    repo.add_multiple_category(categories)
    repo.add_multiple_nutrition(nutrition)
    repo.add_multiple_author(authors)

    if database_mode:
        repo.add_multiple_instruction(instructions)
        repo.add_multiple_image(images)
        repo.add_multiple_ingredient(ingredients)
