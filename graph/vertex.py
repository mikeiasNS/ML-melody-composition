import pdb

class Vertex:
  def __init__(self, id, duration, tempo):
    self.edges = [] #edges originated from this vertex
    self.id = id #note int identifier (-1 to pauses)
    self.duration = duration #duration in ticks
    self.tempo = tempo

  def through_edge(self, edge):
    # pdb.set_trace()
    for e in self.edges:
      if e == edge:
        e.occurrences += 1
        return

    for e in self.edges:
      if e == edge:
        edges.append(edge)
        return

    self.edges.append(edge)

  def __str__(self):
    edges_dict = []
    for e in self.edges:
      edges_dict.append(str(e))
    my_dict = {'edges': edges_dict, 'id': self.id, 'duration': self.duration}
    return str(my_dict)