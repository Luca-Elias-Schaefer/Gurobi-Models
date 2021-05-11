from gurobipy import *
import networkx as nx
import random as rd


def solveWeightConstrainedSP(G: nx.DiGraph, source: int, sink: int, W: int) -> list:
    """
    Solves the weight-constrained shortest path problem.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :param W: Weight bound
    :return: List of edges
    """
    weightConstrainedSP = Model('weightConstrainedSP')

    # Variable
    X = dict()

    for a in G.edges():
        X[a] = weightConstrainedSP.addVar(vtype=GRB.BINARY, name=f'X_{a}')

    # Objective function
    weightConstrainedSP.setObjective(quicksum(X[a] * G.get_edge_data(*a)['length'] for a in G.edges()), GRB.MINIMIZE)

    # Constraints
    for v in G.nodes():
        if v == source:
            weightConstrainedSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 1)
        elif v == sink:
            weightConstrainedSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, -1)
        else:
            weightConstrainedSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 0)

    weightConstrainedSP.addConstr(quicksum(X[a] * G.get_edge_data(*a)['weight'] for a in G.edges()), GRB.LESS_EQUAL, W)

    # Solve model
    weightConstrainedSP.update()
    weightConstrainedSP.optimize()

    if weightConstrainedSP.status == GRB.OPTIMAL:
        SPedges = list()
        for a in G.edges():
            if round(weightConstrainedSP.getVarByName(f'X_{a}').x, 0) == 1:
                SPedges.append(a)
        return SPedges

    else:
        return None



if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20).to_directed()
    for a in G.edges():
        G[a[0]][a[1]]['length'] = rd.randint(1, 19)
        G[a[0]][a[1]]['weight'] = rd.randint(1,14)

    SPedges = solveWeightConstrainedSP(G, 1, 14, 8)

    print('Shortest path edges: {}'.format(SPedges))
