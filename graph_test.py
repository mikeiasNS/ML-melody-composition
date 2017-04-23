from graph.vertex import Vertex
from graph.edge import Edge

c = Vertex(0, 960)
g = Vertex(7, 960)

e1 = Edge(g)
e2 = Edge(c)

c.through_edge(e1)
g.through_edge(e2)
c.through_edge(e1)

print c.edges[0]