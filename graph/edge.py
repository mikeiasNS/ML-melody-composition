import pdb

class Edge:
  """docstring for Edge"""
  def __init__(self, destination_vertex):
    self.destination = destination_vertex
    self.occurrences = [] #A list with the number of sequential ocurrences

  def __eq__(self, other):
    # pdb.set_trace()
    return self.destination.id == other.destination.id

  def __str__(self):
    return str(self.__dict__)