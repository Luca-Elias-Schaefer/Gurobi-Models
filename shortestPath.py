from gurobipy import *
import networkx as nx
import random as rd

def solveShortestPath(G: nx.DiGraph, source,  sink) -> list:
    """
    Solves the shortest path problem.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :return: List of edges
    """
    shortestPath = Model('ShortestPath')

    # Variable
    X = dict()

    for a in G.edges():
        X[a] = shortestPath.addVar(vtype=GRB.BINARY, name=f'X_{a}')

    # Objective function
    shortestPath.setObjective(quicksum(X[a] * G.get_edge_data(*a)['weight'] for a in G.edges()), GRB.MINIMIZE)

    # Constraints
    for v in G.nodes():
        if v == source:
            shortestPath.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 1)
        elif v == sink:
            shortestPath.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, -1)
        else:
            shortestPath.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 0)

    # Solve model
    shortestPath.update()
    shortestPath.optimize()

    if shortestPath.status == GRB.OPTIMAL:
        SPedges = list()
        for a in G.edges():
            if round(shortestPath.getVarByName(f'X_{a}').x, 0) == 1.0:
                SPedges.append(a)
        return SPedges

    else:
        return list()



if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20)
    H = G.to_directed()
    for a in H.edges():
        H[a[0]][a[1]]['weight'] = rd.randint(1,14)

    SPedges = solveShortestPath(H, 1, 14)

    print('Shortest path edges: {}'.format(SPedges))
