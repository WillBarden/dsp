from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from functools import lru_cache
from typing import List

import networkx as nx
import yaml
from pyvis.network import Network
from type_defs import *


class Catalog:
  def __init__(self, items: List[Item], building_types: dict, buildings: List[Building], matrices: List[Matrix], recipes: List[Recipe]):
    self.items = items
    self.building_types = building_types
    self.buildings = buildings
    self.recipes = recipes
    self.matrices = matrices

  @property
  def resources(self):
    return self.items + self.buildings
  
  @lru_cache
  def craftable(self, item: Item):
    return item.id in (product for recipe in self.recipes for product in recipe.products.keys())

  def print(self):
    print('-- ITEMS --')
    for item in self.items:
      print(item)

    print('-- SCIENCE MATRICES --')
    for matrix in self.matrices:
      print(matrix)

    print('-- BUILDINGS --')
    for building in self.buildings:
      print(building)

    print('-- RECIPES --')
    for recipe in self.recipes:
      print(recipe)

  def validate(self):
    for recipe in self.recipes:
      if recipe.building not in self.building_types.keys():
        raise ValueError(f'Invalid building "{recipe.building}" in recipe "{str(recipe)}"')
      for product in recipe.products.keys():
        if product not in (item.id for item in self.items + self.matrices):
          raise ValueError(f'Invalid product "{product}" in recipe "{str(recipe)}"')
      for material in recipe.materials.keys():
        if material not in (item.id for item in self.items + self.matrices):
          raise ValueError(f'Invalid material "{material}" in recipe "{str(recipe)}"')

  @classmethod
  def load_config(cls):
    with open('resources.yaml', 'r') as file:
      return yaml.safe_load(file)

  @classmethod
  def from_config(cls, config):
    items = [Item.from_dict(d) for d in config['items']]
    building_types = config['building-types']
    buildings = [Building.from_dict(d) for d in config['buildings']]
    matrices = [Matrix.from_dict(d) for d in config['matrices']]
    recipes = [Recipe.from_dict(d) for d in config['recipes']]
    return Catalog(items, building_types, buildings, matrices, recipes)

  @classmethod
  def load(cls):
    return Catalog.from_config(Catalog.load_config())
