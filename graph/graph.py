from edge import Edge

class Graph:
  def __init__(self, first_vertex, ticks_per_beat, time_signature):
    self.vertexes = [first_vertex]
    self.ticks_per_beat = ticks_per_beat
    self.time_signature = time_signature

  def keep_going_to(self, vertex):
    append_it = True

    for v in self.vertexes:
      if v.id == vertex.id and v.duration == vertex.duration:
        append_it = False
    
    self.vertexes[-1].through_edge(Edge(vertex))

    if append_it:
      self.vertexes.append(vertex)