import pdb

class Vertex:
  def __init__(self, id, duration):
    self.edges = [] #edges originated from this vertex
    self.id = id #note int identifier (-1 to pauses)
    self.duration = duration #duration in ticks

  def through_edge(self, edge):
    # pdb.set_trace()
    if len(self.edges) > 0 and self.edges[-1] == edge:
      self.edges[-1].occurrences[-1] += 1
      return

    for e in self.edges[0:-1]:
      if e == edge:
        e.occurrences.append(1)
        return

    edge.occurrences.append(1)
    self.edges.append(edge)

  def __str__(self):
    return str(self.__dict__)