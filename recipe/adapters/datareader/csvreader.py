from __future__ import annotations

import csv
from ast import literal_eval
from datetime import datetime
from pathlib import Path
from typing import List
from dateutil import parser as date_parser

from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.author import Author
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.category import Category
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction


class CSVReader:
    def __init__(self, file_path: str | Path):
        self.__file_path = Path(file_path)
        self.__recipes: list[Recipe] = []
        self.__authors: dict[int, Author] = {}
        self.__categories: dict[str, Category] = {}
        self.__nutrition: dict[int, Nutrition] = {}
        self.__images: list[RecipeImage] = []
        self.__ingredients: list[RecipeIngredient] = []
        self.__instructions: list[RecipeInstruction] = []

    def extract_data(self) -> None:
        """Reads the CSV and creates domain model objects."""

        def parse_list(value:str) -> list:
            if value == "None":
                return []
            try:
                return literal_eval(value)
            except (ValueError, SyntaxError):
                return []

        with open(self.__file_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            category_id = 0
            for row in reader:

                created_date = None,
                if row.get("DatePublished"):
                    try:
                        created_date = date_parser.parse(row["DatePublished"])
                    except (ValueError, OverflowError):
                        created_date = None

                # --- Author ---
                author_id = int(row["AuthorId"])
                if author_id not in self.__authors:
                    self.__authors[author_id] = Author(
                        author_id = author_id,
                        name = row["AuthorName"]
                    )

                # --- Category ---
                category_type = row["RecipeCategory"]
                if category_type not in self.__categories:
                    category_id = category_id + 1
                    self.__categories[category_type] = Category(
                        name = category_type,
                        category_id = category_id
                    )

                # --- Nutrition ---
                nutrition = Nutrition(
                    id = int(row["RecipeId"]),
                    calories = float(row["Calories"]) if row["Calories"] else None,
                    fat = float(row["FatContent"]) if row["FatContent"] else None,
                    saturated_fat = float(row["SaturatedFatContent"]) if row["SaturatedFatContent"] else None,
                    cholesterol = float(row["CholesterolContent"]) if row["CholesterolContent"] else None,
                    sodium = float(row["SodiumContent"]) if row["SodiumContent"] else None,
                    carbohydrates = float(row["CarbohydrateContent"]) if row["CarbohydrateContent"] else None,
                    fiber = float(row["FiberContent"]) if row["FiberContent"] else None,
                    sugar = float(row["SugarContent"]) if row["SugarContent"] else None,
                    protein = float(row["ProteinContent"]) if row["ProteinContent"] else None
                )
                self.__nutrition[int(row["RecipeId"])] = nutrition

                # --- Recipe ---
                recipe = Recipe(
                    recipe_id = int(row["RecipeId"]),
                    name = row["Name"],
                    author = self.__authors[author_id],
                    cook_time = int(row["CookTime"]) if row["CookTime"] else 0,
                    preparation_time = int(row["PrepTime"]) if row["PrepTime"] else 0,
                    created_date = created_date,
                    description = row.get("Description", ""),
                    images = parse_list(row.get("Images")),
                    category = self.__categories[category_type],
                    ingredient_quantities = parse_list(row.get("RecipeIngredientQuantities")),
                    ingredients = parse_list(row.get("RecipeIngredientParts")),
                    nutrition = nutrition,
                    servings = row.get("RecipeServings"),
                    recipe_yield = row.get("RecipeYield"),
                    instructions = parse_list(row.get("RecipeInstructions"))
                )

                self.__recipes.append(recipe)
                # connect author & category relationships
                self.__authors[author_id].add_recipe(recipe)
                self.__categories[category_type].add_recipe(recipe)

                id = int(row["RecipeId"])
                image_urls = parse_list(row.get("Images"))
                for i in range(len(image_urls)):
                    self.__images.append(RecipeImage(id, image_urls[i], i))

                ingredient_quantities = parse_list(row.get("RecipeIngredientQuantities"))
                ingredients = parse_list(row.get("RecipeIngredientParts"))
                for i in range(min(len(ingredient_quantities), len(ingredients))):
                    self.__ingredients.append(RecipeIngredient(id, ingredient_quantities[i], ingredients[i], i))

                instructions = parse_list(row.get("RecipeInstructions"))
                for i in range(len(instructions)):
                    self.__instructions.append(RecipeInstruction(id, instructions[i], i))


    # --- Accessors ---
    def get_recipes(self) -> List[Recipe]:
        return self.__recipes

    def get_authors(self) -> dict[int, Author]:
        return self.__authors

    def get_categories(self) -> dict[str, Category]:
        return self.__categories

    def get_nutrition(self) -> dict[int, Nutrition]:
        return self.__nutrition

    def get_recipe_ingredients(self) -> list[RecipeIngredient]:
        return self.__ingredients

    def get_instructions(self) -> list[RecipeInstruction]:
        return self.__instructions

    def get_images(self) -> list[RecipeImage]:
        return self.__images
