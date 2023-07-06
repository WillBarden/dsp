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
  edge_color = 'darkgray'

  G = nx.DiGraph()
  for item in catalog.items:
    color = item_color if catalog.craftable(item) else base_color
    G.add_node(item.id, label=item.name, color=color)

  for matrix in catalog.matrices:
    G.add_node(matrix.id, label=matrix.name, color=matrix.color)

  for building in catalog.buildings:
    G.add_node(building.id, label=building.name, color=building_color)

  for recipe in catalog.recipes:
    for product, _ in recipe.products.items():
      for material, quantity in recipe.materials.items():
        G.add_edge(material, product, label=str(quantity), color=edge_color, weight=(recipe.time / 2))
  return G
  

def generate_html(G, file_name):
  net = Network(directed=True, height='98vh', font_color='black', layout=False)
  net.repulsion(node_distance=100, central_gravity=0.05, spring_length=200, spring_strength=0.01)
  net.set_edge_smooth('continuous')
  net.from_nx(G)
  net.save_graph(file_name)


def main():
  catalog = Catalog.load()
  generate_html(create_crafting_graph(catalog), 'dsp_crafting_tree.html')


if __name__ == '__main__':
  main()
