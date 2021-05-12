from gurobipy import *
import networkx as nx
import random as rd


def solveMaxFlowInterdiction(G: nx.DiGraph, interdictionBudget: int, source, sink) -> dict:
    """
    Solves the maximum flow network interdiction problem.
    :param G: directed graph
    :param interdictionBudget: Interdiction budget (int)
    :param source: Source node in G
    :param sink: Sink node in G
    :return: List of edges
    """
    maxFlowInterdiction = Model('maxFlowInterdiction')

    # Variables
    Alpha = dict()
    Beta = dict()
    Gamma = dict()

    for u in G.nodes():
        Alpha[u] = maxFlowInterdiction.addVar(vtype=GRB.BINARY, name=f'Alpha_{u}')

    for u,v in G.edges():
        Beta[u,v] = maxFlowInterdiction.addVar(vtype=GRB.BINARY, name=f'Beta_{u}_{v}')
        Gamma[u,v] = maxFlowInterdiction.addVar(vtype=GRB.BINARY, name=f'Gamma_{u}_{v}')

    # Objective function
    maxFlowInterdiction.setObjective(quicksum(G[u][v]['capacity'] * Beta[u, v] for u, v in G.edges()), sense=GRB.MINIMIZE)

    # Constraints
    maxFlowInterdiction.addConstr(quicksum(G[u][v]['cost']*Gamma[u,v] for u,v in G.edges()), GRB.LESS_EQUAL, interdictionBudget)

    maxFlowInterdiction.addConstr(Alpha[sink] - Alpha[source], GRB.GREATER_EQUAL, 1)

    for u,v in G.edges():
        maxFlowInterdiction.addConstr(Alpha[u] - Alpha[v] + Beta[u,v] + Gamma[u,v], GRB.GREATER_EQUAL, 0)

    # Solve model
    maxFlowInterdiction.update()
    maxFlowInterdiction.optimize()

    if maxFlowInterdiction.status == GRB.OPTIMAL:
        interdictedEdges = list()
        for u,v in G.edges():
            if round(maxFlowInterdiction.getVarByName(f'Gamma_{u}_{v}').x, 0) == 1:
                interdictedEdges.append((u,v))
        return interdictedEdges

    else:
        return list()


if __name__ == '__main__':
    # Example: Complete graph on 40 vertices
    G = nx.complete_graph(40)
    H = G.to_directed()

    for u,v in H.edges():
        H[u][v]['cost'] = rd.randint(1,10)
        H[u][v]['capacity'] = rd.randint(10, 60)

    interdictionBudget = 10
    source, sink = 0, 20

    sol = solveMaxFlowInterdiction(H, interdictionBudget, source, sink)
    print('Interdicted edges: {}'.format(sol))


