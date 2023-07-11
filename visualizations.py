import os
from functools import reduce
from typing import Optional

import networkx as nx
from pyvis.network import Network

from catalog import Catalog
from type_defs import *


def create_crafting_graph(catalog: Catalog):
  base_item_color = 'lightgreen'
  item_color = 'lightblue'
  edge_color = 'lightgray'

  G = nx.DiGraph()
  for item in catalog.items:
    color = item_color if catalog.craftable(item) else base_item_color
    G.add_node(item.id, label=item.name, color=color)

  for matrix in catalog.matrices:
    G.add_node(matrix.id, label=matrix.name, color=matrix.color)

  for recipe in catalog.recipes:
    recipe_id = str(hash(recipe))
    if recipe.time:
      label = str(catalog.building_types[recipe.building]) + ' ' + str(recipe.time) + 's'
    elif recipe.fraction:
      label = str(catalog.building_types[recipe.building]) + ' ' + str(recipe.fraction * 100) + '%'
    G.add_node(recipe_id, label=label, shape='text', color=edge_color)
    for product, product_quantity in recipe.products.items():
      G.add_edge(recipe_id, product, label=str(product_quantity), color=edge_color)
      for material, material_quantity in recipe.materials.items():
        G.add_edge(material, recipe_id, label=str(material_quantity), color=edge_color)
  return G

def create_dependency_graph(catalog: Catalog):
  base_item_color = 'lightgreen'
  item_color = 'lightblue'
  edge_color = 'lightgray'

  G = nx.DiGraph()
  for item in catalog.items:
    color = item_color if catalog.craftable(item) else base_item_color
    G.add_node(item.id, label=item.name, color=color)

  for matrix in catalog.matrices:
    G.add_node(matrix.id, label=matrix.name, color=matrix.color)

  for recipe in catalog.recipes:
    for product, product_quantity in recipe.products.items():
      for material, material_quantity in recipe.materials.items():
        G.add_edge(product, material, label=str(material_quantity), color=edge_color, 
                   material_quantity=material_quantity, product_quantity=product_quantity, time=recipe.time)
  return G


def generate_html(graph, file_name):
  net = Network(directed=True, height='98vh', font_color='black', layout=False)
  net.hrepulsion(node_distance=100, central_gravity=0.05, spring_length=200, spring_strength=0.01)
  net.set_edge_smooth('continuous')
  net.from_nx(graph)
  net.save_graph(file_name)


def main():
  catalog = Catalog.load()
  catalog.validate()

  visualization_dir = 'dsp_diagrams'
  if not os.path.exists(visualization_dir):
    os.mkdir(visualization_dir)

  for name, method in {
    'crafting_graph': [create_crafting_graph, catalog],
    'dependency_graph': [create_dependency_graph, catalog]
  }.items():
    generate_html(method[0](*method[1:]), os.path.join(visualization_dir, name) + '.html')


if __name__ == '__main__':
  main()
