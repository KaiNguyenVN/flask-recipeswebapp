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

    for recipe in recipes:
        repo.add_recipe(recipe)
    for id in categories:
        repo.add_category(id, categories[id])
    for id in nutrition:
        repo.add_nutrition(id, nutrition[id])
    for id in authors:
        repo.add_author(id, authors[id])

    if database_mode:
        for instruction in instructions:
            repo.add_instruction(instruction)
        for image in images:
            repo.add_image(image)
        for ingredient in ingredients:
            repo.add_ingredient(ingredient)
