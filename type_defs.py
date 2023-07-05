from abc import ABC, abstractmethod, abstractproperty
from typing import List
from enum import Enum
from functools import lru_cache
import yaml
import matplotlib.pyplot as plt
import networkx as nx
from pyvis.network import Network


class Resource(ABC):
  def __init__(self, id: str, name: str):
    self.id = id
    self.name = name

  def __str__(self):
    return self.name


class Item(Resource):
  def __init__(self, id: str, name: str):
    super(Item, self).__init__(id, name)

  @classmethod
  def from_dict(cls, D: dict):
    return Item(D['id'], D['name'])

class Matrix(Resource):
  def __init__(self, id: str, name: str, color: str):
    super(Matrix, self).__init__(id, name)
    self.color = color

  @classmethod
  def from_dict(cls, D: dict):
    return Matrix(D['id'], D['name'], D['color'])

class Building(Resource):
  def __init__(self, id: str, name: str, building_type: str):
    super(Building, self).__init__(id, name)
    self.building_type = building_type

  @classmethod
  def from_dict(cls, D: dict):
    return Building(D['id'], D['name'], D['type'])


class Recipe:
  def __init__(self, products: dict, time: float, materials: dict, building: str):
    self.products = products
    self.time = time
    self.materials = materials
    self.building = building

  def __str__(self):
    return ', '.join(list(self.products.keys())) + ' <- ' + ', '.join(list(self.materials.keys()))

  @classmethod
  def from_dict(cls, D: dict):
    return Recipe(D['products'], D['time'], D['materials'], D['building'])


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

    print('-- BUILDINGS --')
    for building in self.buildings:
      print(building)

    print('-- RECIPES --')
    for recipe in self.recipes:
      print(recipe)

  def to_nx(self):
    g = nx.DiGraph()
    for item in self.items:
      color = 'lightblue' if self.craftable(item) else 'lightgreen'
      g.add_node(item.id, label=item.name, shape='circle', color=color)

    for matrix in self.matrices:
      g.add_node(matrix.id, label=matrix.name, color=matrix.color)

    for building in self.buildings:
      g.add_node(building.id, label=building.name, shape='circle', color='pink')

    for recipe in self.recipes:
      for product, _ in recipe.products.items():
        for material, quantity in recipe.materials.items():
          g.add_edge(material, product, label=str(quantity), color='darkgray', width=5)
    return g
  
  def generate(self):
    G = self.to_nx()
    net = Network(directed=True, height='98vh', font_color='black')
    # net.options.layout.set_separation(200)
    net.repulsion(node_distance=150, central_gravity=0.05, spring_length=300, spring_strength=0.01)
    net.set_edge_smooth('continuous')
    net.from_nx(G)
    net.save_graph('dsp_resource_crafting_tree.html')
    # pos = nx.spring_layout(g, seed=3068)
    # nx.draw(g, pos=pos, with_labels=False)
    # labels = {resource.id: resource.name for resource in self.resources}
    # print(labels)
    # nx.draw_networkx_labels(g, pos=pos, labels=labels)
    # plt.show()

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
