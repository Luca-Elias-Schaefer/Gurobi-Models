from gurobipy import *
import networkx as nx
import random as rd


def solveMinCostFlow(G: nx.DiGraph, source: int, sink: int, demand: int) -> dict:
    """
    Solves the minimum cost flow problem.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :param demand: Demand value
    :return: Dict of edges and flow values
    """

    minCostFlow = Model('MinCostFlow')

    # Variable
    X = dict()

    for a in G.edges():
        X[a] = minCostFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=G.get_edge_data(*a)['capacity'], name=f'X_{a}')

    # Objective function
    minCostFlow.setObjective(quicksum(X[a]*G.get_edge_data(*a)['cost'] for a in G.edges()), sense=GRB.MINIMIZE)


    # Constraints
    for v in G.nodes():
        if v == source:
            minCostFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                              GRB.EQUAL, demand)
        elif v == sink:
            minCostFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                              GRB.EQUAL, -demand)
        else:
            minCostFlow.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                              GRB.EQUAL, 0)

    # Solve model
    minCostFlow.update()
    minCostFlow.optimize()

    if minCostFlow.status == GRB.OPTIMAL:
        flows = dict()
        for a in G.edges():
            if minCostFlow.getVarByName(f'X_{a}').x > 0:
                flows[a] = minCostFlow.getVarByName(f'X_{a}').x
        return flows

    else:
        return dict()



if __name__ == '__main__':
    # Example: Complete graph on 100 vertices
    G = nx.complete_graph(100).to_directed()
    for a in G.edges():
        G[a[0]][a[1]]['capacity'] = rd.randint(1, 14)
        G[a[0]][a[1]]['cost'] = rd.randint(1, 14)

    flows = solveMinCostFlow(G, 0, 99, 5)

    print('Min cost flow edges: {}'.format(flows))



