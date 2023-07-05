import json
import yaml
from typing import List, Optional
from pyvis.network import Network
from types import SimpleNamespace
from abc import ABC, abstractmethod

RESOURCES_FILE = 'resources.yaml'
VISUALIZATION_FILE = 'dsp_resource_crafting_tree.html'


class Resource(ABC):
  def __init__(self, id: str, name: str):
    self.id = id
    self.name = name


class NaturalResource(Resource):
  def __init__(self, id: str, name: str):
    super(NaturalResource, self).__init__(id, name)

  def __str__(self):
    return self.name

  @classmethod
  def from_dict(cls, d):
    return NaturalResource(d['id'], d['name'])


class Recipe:
  def __init__(self, building_type: str, quantity: int, time: int, ingredients: dict):
    self.building_type = building_type
    self.quantity = quantity
    self.time = time
    self.ingredients = ingredients

  def __str__(self):
    return [i for i in self.ingredients.keys()]
  
  @classmethod
  def from_dict(cls, d):
    return Recipe(d['building_type'], d['quantity'], d['time'], d['ingredients'])


class Item(Resource):
  def __init__(self, id: str, name: str, recipes: List[Recipe]):
    super(Item, self).__init__(id, name)
    self.recipes = recipes

  def __str__(self):
    return self.name
  
  @classmethod
  def from_dict(cls, d):
    return Item(d['id'], d['name'], [Recipe.from_dict(r) for r in d['recipes']])


class Building(Resource):
  def __init__(self, id: str, name: str):
    super(Building, self).__init__(id, name)


class Catalog:
  def __init__(
      self, 
      natural_resources: List[NaturalResource], 
      items: List[Item], 
      buildings: List[Building],
      building_types: dict
  ):
    self.natural_resources = natural_resources
    self.items = items
    self.buildings = buildings
    self.building_types = building_types

  def __contains__(self, item):
    item = item if isinstance(item, str) else item.id
    return item in (r.id for r in self.all_resources())

  def all_resources(self):
    return self.natural_resources + self.items + self.buildings

  @classmethod
  def from_config(cls, config):
    natural_resources = [NaturalResource.from_dict(r) for r in config['natural_resources']]
    items = [Item.from_dict(i) for i in config['items']]
    building_types = {t['id']: t['name'] for t in config['building_types']}
    return Catalog(natural_resources, items, [], building_types)


def load_resource_config():
  with open(RESOURCES_FILE, 'r') as file:
    return yaml.safe_load(file)


def create_crafting_tree_visualization(catalog: Catalog):
  net = Network(directed=True, width=1500, height=1000)
  # net.toggle_physics(True)
  # net.barnes_hut()

  for resource in catalog.all_resources():
    print(resource.id)
    if isinstance(resource, NaturalResource):
      net.add_node(resource.id, label=resource.name, color='green')
    elif isinstance(resource, Item):
      net.add_node(resource.id, label=resource.name, color='blue')
    elif isinstance(resource, Building):
      pass

  for item in catalog.items:
    for recipe in item.recipes:
      net.add_node(hash(recipe), label=catalog.building_types[recipe.building_type], color='gray')
      net.add_edge(hash(recipe), item.id, label=f'{recipe.quantity}/{recipe.time}s', color='black')
      for ingredient, quantity in recipe.ingredients.items():
        net.add_edge(ingredient, hash(recipe), label=str(quantity), color='black')

  net.save_graph(VISUALIZATION_FILE)
    

if __name__ == '__main__':
  catalog = Catalog.from_config(load_resource_config())
  create_crafting_tree_visualization(catalog)
