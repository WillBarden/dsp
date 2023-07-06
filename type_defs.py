from abc import ABC, abstractmethod, abstractproperty
from enum import Enum
from functools import lru_cache
from typing import List


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
