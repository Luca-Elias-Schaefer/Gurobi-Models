from gurobipy import *
import networkx as nx
import random as rd

def solveMaxFlow(G: nx.DiGraph, source: int, sink: int) -> dict:
    """
    Solves the maximum flow problem.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :return: Dict of edges and flow values
    """
    maxFlow = Model('MaxFlow')

    # Variable
    X = dict()

    for a in G.edges():
        X[a] = maxFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=G.get_edge_data(*a)['capacity'], name=f'X_{a}')

    B = maxFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, name='B')

    # Objective function
    maxFlow.setObjective(B, sense=GRB.MAXIMIZE)

    # Constraints
    for v in G.nodes():
        if v == source:
            maxFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, B)
        elif v == sink:
            maxFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, -B)
        else:
            maxFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 0)

    # Solve model
    maxFlow.update()
    maxFlow.optimize()

    if maxFlow.status == GRB.OPTIMAL:
        flows = dict()
        for a in G.edges():
            if maxFlow.getVarByName(f'X_{a}').x > 0:
                flows[a] = maxFlow.getVarByName(f'X_{a}').x
        return flows

    else:
        return dict()



if __name__ == '__main__':
    # Example: Complete graph on 100 vertices
    G = nx.complete_graph(100).to_directed()
    for a in G.edges():
        G[a[0]][a[1]]['capacity'] = rd.randint(1,14)

    flows = solveMaxFlow(G, 0, 99)

    print('Max flow edges: {}'.format(flows))

