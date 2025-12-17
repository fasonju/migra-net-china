import networkx as nx


def graph_in_range(G: nx.MultiDiGraph, years: list[int]) -> nx.MultiDiGraph:
    """
    Subgraph of G containing only edges from the specified years.
    """
    H = nx.MultiDiGraph()
    for u, v, key, data in G.edges(keys=True, data=True):
        if data['attributes'].year in years:
            if not H.has_node(u):
                H.add_node(u, **G.nodes[u])
            if not H.has_node(v):
                H.add_node(v, **G.nodes[v])
            H.add_edge(u, v, key=key, **data)
    return H
