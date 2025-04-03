# main.py
from graph_tool.all import *


def main():
    # Create a directed graph
    g = Graph()

    # Add vertices
    v1 = g.add_vertex()
    v2 = g.add_vertex()

    # Add an edge between the vertices
    e = g.add_edge(v1, v2)

    # Visualize the graph
    graph_draw(g, vertex_text=g.vertex_index, output="results/test.svg")
    print("[graph visualization saved]")


if __name__ == "__main__":
    main()
