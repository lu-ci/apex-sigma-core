import os

import yaml

from .item_core import ItemCore
from .properties import cook_icons, cook_colors


class SigmaRecipe(object):
    def __init__(self, core, item_data):
        self.recipe_core = core
        self.raw_data = item_data
        self.file_id = self.raw_data['file_id']
        self.name = self.raw_data['name']
        self.type = self.raw_data['type']
        self.icon = cook_icons[self.type.lower()]
        self.color = cook_colors[self.type.lower()]
        self.desc = self.raw_data['description']
        self.value = self.raw_data['value']
        self.raw_ingredients = self.raw_data['ingredients']
        self.ingredients = []
        self.load_ingredients()

    def load_ingredients(self):
        for ingredient in self.raw_ingredients:
            ingr_item = self.recipe_core.item_core.get_item_by_file_id(ingredient)
            self.ingredients.append(ingr_item)


class RecipeCore(object):
    def __init__(self, item_directory):
        self.base_dir = item_directory
        self.item_core = ItemCore(self.base_dir)
        self.recipes = []
        self.init_items()

    def find_recipe(self, name):
        out = None
        for recipe in self.recipes:
            if recipe.name.lower() == name.lower():
                out = recipe
                break
        return out

    def init_items(self):
        for root, dirs, files in os.walk(f'{self.base_dir}/recipes'):
            for file in files:
                if file.endswith('.yml'):
                    file_path = (os.path.join(root, file))
                    with open(file_path, encoding='utf-8') as item_file:
                        item_id = file.split('.')[0]
                        item_data = yaml.safe_load(item_file)
                        item_data.update({'file_id': item_id})
                        item_object = SigmaRecipe(self, item_data)
                        self.recipes.append(item_object)
