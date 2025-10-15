

from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text, UniqueConstraint, MetaData
)
from sqlalchemy.orm import registry, relationship, foreign

from recipe.domainmodel.author import Author
from recipe.domainmodel.category import Category
from recipe.domainmodel.favourite import Favourite
from recipe.domainmodel.nutrition import Nutrition
from recipe.domainmodel.recipe import Recipe
from recipe.domainmodel.recipe_image import RecipeImage
from recipe.domainmodel.recipe_ingredient import RecipeIngredient
from recipe.domainmodel.recipe_instruction import RecipeInstruction
from recipe.domainmodel.review import Review
from recipe.domainmodel.user import User

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

# Authors table
authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False)
)

# Category table
categories_table = Table(
    'category', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False)
)

# Favorite table
favorite_table = Table(
    'favorite', mapper_registry.metadata,
    Column('id', Integer,primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False),
    Column('username', String(255), ForeignKey('user.username'), nullable=False),
)

# Nutrition table
nutrition_table = Table(
    'nutrition', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False),
    Column('calories', Float, nullable=False),
    Column('fat', Float, nullable=False),
    Column('saturated_fat', Float, nullable=False),
    Column('cholesterol', Float, nullable=False),
    Column('sodium', Float, nullable=False),
    Column('carbohydrates', Float, nullable=False),
    Column('fiber', Float, nullable=False),
    Column('sugar', Float, nullable=False),
    Column('protein', Float, nullable=False),
)

# Recipe table
recipe_table = Table(
    'recipe', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('author_id', Integer, ForeignKey('authors.id'), nullable=False),
    Column('cook_time', Integer, nullable=False),
    Column('preparation_time', Integer, nullable=False),
    Column('date', DateTime, nullable=False),
    Column('description', Text, nullable=False),
    Column('category_id', Integer, ForeignKey('category.id'), nullable=False),
    Column('rating', Float, nullable=True),
    Column('servings', String(255), nullable=False),
    Column('recipe_yield', String(255), nullable=False),
)

# Ingredient table
ingredient_table = Table(
    'ingredient', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, nullable=False),
    Column('ingredient', String(255), nullable=False),
    Column('quantity', String(255), nullable=False),
    Column('position', Integer, nullable=False),
)

# Instruction table
instruction_table = Table(
    'instruction', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, nullable=False),
    Column('step', String(255), nullable=False),
    Column('position', Integer, nullable=False),
)

# Image table
image_table = Table(
    'image', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('recipe_id', Integer, nullable=False),
    Column('url', String(500), nullable=False),
    Column('position', Integer, nullable=False)
)

# Review table
review_table = Table(
    'review', mapper_registry.metadata,
    Column('id', Integer, primary_key=True),
    Column('recipe_id', Integer, ForeignKey('recipe.id'), nullable=False),
    Column('username', String(255), ForeignKey('user.username'), nullable=False),
    Column('rating', Integer, nullable=False),
    Column('review', Text, nullable=False),
    Column('date', DateTime, nullable=False),
)

# User table
user_table = Table(
    'user', mapper_registry.metadata,
#    Column('id', Integer, nullable=False),
    Column('username', String(255), primary_key=True),
    Column('password', String(255), nullable=False),
)

# ORM Mappings
def map_model_to_tables():
    # Author mapping
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_Author__id': authors_table.c.id,
        '_Author__name': authors_table.c.name,
        '_Author__recipes': relationship(Recipe, back_populates='_Recipe__author', foreign_keys=[recipe_table.c.author_id]),
    })
    # Category mapping
    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_Category__id': categories_table.c.id,
        '_Category__name': categories_table.c.name,
        '_Category__recipes': relationship(Recipe, back_populates='_Recipe__category', foreign_keys=[recipe_table.c.category_id]),
    })
    # Favorite mapping
    mapper_registry.map_imperatively(Favourite, favorite_table, properties={
        '_Favourite__id': favorite_table.c.id,
        '_Favourite__username': relationship(User, back_populates='_User__favourite_recipes', foreign_keys=[favorite_table.c.username], uselist=False),
        '_Favourite__recipe': relationship(Recipe, foreign_keys=[favorite_table.c.recipe_id], uselist=False),
    })
    # Recipe mapping
    mapper_registry.map_imperatively(Recipe, recipe_table, properties={
        '_Recipe__id': recipe_table.c.id,
        '_Recipe__name': recipe_table.c.name,
        '_Recipe__author': relationship(Author, back_populates='_Author__recipes', foreign_keys=[recipe_table.c.author_id], uselist=False),
        '_Recipe__cook_time': recipe_table.c.cook_time,
        '_Recipe__preparation_time': recipe_table.c.preparation_time,
        '_Recipe__date': recipe_table.c.date,
        '_Recipe__description': recipe_table.c.description,
        '_Recipe__category': relationship(Category, back_populates='_Category__recipes',foreign_keys=[recipe_table.c.category_id], uselist=False),
        '_Recipe__rating': recipe_table.c.rating,
        '_Recipe__servings': recipe_table.c.servings,
        '_Recipe__recipe_yield': recipe_table.c.recipe_yield,
        '_Recipe__reviews': relationship(Review, back_populates='_Review__recipe'),
        '_Recipe__nutrition': relationship(Nutrition, back_populates='_Nutrition__recipe', uselist=False)
    })
    # Nutrition mapping
    mapper_registry.map_imperatively(Nutrition, nutrition_table, properties={
        '_Nutrition__id': nutrition_table.c.id,
        '_Nutrition__calories': nutrition_table.c.calories,
        '_Nutrition__fat': nutrition_table.c.fat,
        '_Nutrition__saturated_fat': nutrition_table.c.saturated_fat,
        '_Nutrition__cholesterol': nutrition_table.c.cholesterol,
        '_Nutrition__sodium': nutrition_table.c.sodium,
        '_Nutrition__carbohydrates': nutrition_table.c.carbohydrates,
        '_Nutrition__fiber': nutrition_table.c.fiber,
        '_Nutrition__sugar': nutrition_table.c.sugar,
        '_Nutrition__protein': nutrition_table.c.protein,
        '_Nutrition__recipe': relationship(Recipe, back_populates='_Recipe__nutrition', uselist=False)
    })
    # Ingredient mapping
    mapper_registry.map_imperatively(RecipeIngredient, ingredient_table, properties={
        '_RecipeIngredient__recipe_id': ingredient_table.c.recipe_id,
        '_RecipeIngredient__ingredient': ingredient_table.c.ingredient,
        '_RecipeIngredient__quantity': ingredient_table.c.quantity,
        '_RecipeIngredient__position': ingredient_table.c.position,
    })
    # Instruction mapping
    mapper_registry.map_imperatively(RecipeInstruction, instruction_table, properties={
        '_RecipeInstruction__recipe_id': instruction_table.c.recipe_id,
        '_RecipeInstruction__step': instruction_table.c.step,
        '_RecipeInstruction__position': instruction_table.c.position,
    })
    # Image mapping
    mapper_registry.map_imperatively(RecipeImage, image_table, properties={
        '_RecipeImage__recipe_id': image_table.c.recipe_id,
        '_RecipeImage__url': image_table.c.url,
        '_RecipeImage__position': image_table.c.position,
    })
    # Review mapping
    mapper_registry.map_imperatively(Review, review_table, properties={
        '_Review__id': review_table.c.id,
        '_Review__recipe': relationship(Recipe, back_populates='_Recipe__reviews',foreign_keys=[review_table.c.recipe_id], uselist=False),
        '_Review__rating': review_table.c.rating,
        '_Review__date': review_table.c.date,
        '_Review__review': review_table.c.review,
        '_Review__username': relationship(User, back_populates='_User__reviews', foreign_keys=[review_table.c.username], uselist=False),
    })
    # User mapping
    mapper_registry.map_imperatively(User, user_table, properties={
        '_User__username': user_table.c.username,
        '_User__password': user_table.c.password,
        '_User__favourite_recipes': relationship(Favourite, back_populates='_Favourite__username'),
        '_User__reviews': relationship(Review, back_populates='_Review__username')
    })