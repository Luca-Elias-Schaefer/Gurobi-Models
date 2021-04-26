from gurobipy import *
import networkx as nx
import random as rd

def solveShortestPathInterdiction(G:nx.DiGraph, interdictionBudget: int, source:int, sink:int) -> list:
    """
    Solves the shortest path network interdiction problem.
    :param G: directed graph
    :param interdictionBudget: Interdiction budget (int)
    :param source: Source node in G
    :param sink: Sink node in G
    :return: List of edges
    """
    shortestPathInterdiction = Model('shortestPathInterdiction')

    # Variables
    Pi = dict()
    Theta = dict()
    Y = dict()
    Omega = dict()

    # Big-M
    M = sum(G[u][v]['length'] for u,v in G.edges())

    for v in G.nodes():
        Pi[v] = shortestPathInterdiction.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, name=f'Pi_{v}')

    for u,v in G.edges():
        Theta[u, v] = shortestPathInterdiction.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=0.0,
                                                      name=f'Theta_{u}_{v}')
        Y[u, v] = shortestPathInterdiction.addVar(vtype=GRB.CONTINUOUS, ub=0.0, lb=-GRB.INFINITY, name=f'Y_{u}_{v}')
        Omega[u, v] = shortestPathInterdiction.addVar(vtype=GRB.BINARY, name=f'Omega_{u}_{v}')

    # Objective function
    shortestPathInterdiction.setObjective(Pi[sink] - Pi[source] + quicksum(Theta[u, v] for u, v in G.edges()),
                                          sense=GRB.MAXIMIZE)

    # Constraints
    shortestPathInterdiction.addConstr(quicksum(Omega[u, v] * G[u][v]['cost'] for u, v in G.edges()), GRB.LESS_EQUAL,
                                       interdictionBudget)

    for u,v in G.edges():
        shortestPathInterdiction.addConstr(Pi[v] - Pi[u] + Y[u,v], GRB.LESS_EQUAL, G[u][v]['length'])
        shortestPathInterdiction.addConstr(Theta[u,v], GRB.LESS_EQUAL, Y[u,v] + Omega[u,v] * M)

    shortestPathInterdiction.addConstr(Pi[source], GRB.EQUAL, 0)

    # Solve model
    shortestPathInterdiction.update()
    shortestPathInterdiction.optimize()

    if shortestPathInterdiction.status == GRB.OPTIMAL:
        interdictedEdges = list()
        for u,v in G.edges():
            if round(shortestPathInterdiction.getVarByName(f'Omega_{u}_{v}').x, 0) == 1:
                interdictedEdges.append((u,v))
        return interdictedEdges
    else:
        return None


if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20)
    H = G.to_directed()

    for u,v in H.edges():
        H[u][v]['cost'] = rd.randint(1,10)
        H[u][v]['length'] = rd.randint(20, 70)

    interdictionBudget = 30
    source = 3
    sink = 19

    interdictedEdges = solveShortestPathInterdiction(H, interdictionBudget, source, sink)
    print('Interdicted edges: {}'.format(interdictedEdges))
