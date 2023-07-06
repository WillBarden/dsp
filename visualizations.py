import math
import networkx as nx
import yaml
from pyvis.network import Network

from catalog import Catalog
from type_defs import *


def create_crafting_graph(catalog):
  base_color = 'lightgreen'
  item_color = 'lightblue'
  building_color = 'pink'
  edge_color = 'lightgray'

  G = nx.DiGraph()
  for item in catalog.items:
    color = item_color if catalog.craftable(item) else base_color
    G.add_node(item.id, label=item.name, color=color)

  for matrix in catalog.matrices:
    G.add_node(matrix.id, label=matrix.name, color=matrix.color)

  # for building in catalog.buildings:
  #   G.add_node(building.id, label=building.name, color=building_color)

  for recipe in catalog.recipes:
    recipe_id = str(hash(recipe))
    if recipe.time:
      label = str(recipe.time) + 's'
    elif recipe.fraction:
      label = str(recipe.fraction * 100) + '%'
    G.add_node(recipe_id, label=label, shape='text', color=edge_color)
    for product, product_quantity in recipe.products.items():
      G.add_edge(recipe_id, product, label=str(product_quantity), color=edge_color)
      for material, material_quantity in recipe.materials.items():
        G.add_edge(material, recipe_id, label=str(material_quantity), color=edge_color)
  return G
  

def generate_html(G, file_name):
  net = Network(directed=True, height='98vh', font_color='black', layout=False)
  net.repulsion(node_distance=100, central_gravity=0.05, spring_length=200, spring_strength=0.01)
  net.set_edge_smooth('continuous')
  net.from_nx(G)
  net.save_graph(file_name)


def main():
  catalog = Catalog.load()
  catalog.validate()
  generate_html(create_crafting_graph(catalog), 'dsp_crafting_tree.html')


if __name__ == '__main__':
  main()
