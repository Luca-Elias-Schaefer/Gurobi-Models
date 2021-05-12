from gurobipy import *
import networkx as nx
import random as rd

def solveMinMaxMatching(G: nx.Graph) -> list:
    """
    Solves the minimum maximal matching problem.
    :param G: undirected graph
    :return: List of edges
    """
    minmaxMatching = Model(name='minmaxMatching')

    # Edge variables
    X = {}
    for u,v in G.edges():
        X[u,v] = minmaxMatching.addVar(vtype=GRB.BINARY, name=f'X_{u}_{v}')

    # Objective functions
    minmaxMatching.setObjective(quicksum(X[u, v] for u, v in G.edges()), sense=GRB.MINIMIZE)

    # Constraints
    for u in G.nodes():
        minmaxMatching.addConstr(quicksum(X[v,w] for v,w in G.edges() if v == u or w == u), GRB.LESS_EQUAL, 1)

    for u,v in G.edges():
        minmaxMatching.addConstr(1-X[u,v], GRB.LESS_EQUAL, quicksum(X[a,b] for a,b in G.edges() if a == u or b == u and not (a,b) == (u,v))
                                 + quicksum(X[a,b] for a,b in G.edges() if a == v or b == v and not (a,b) == (v,u)))

    # Solve model
    minmaxMatching.update()
    minmaxMatching.optimize()

    if minmaxMatching.status == GRB.OPTIMAL:
        sol = list()
        for u,v in G.edges():
            if round(minmaxMatching.getVarByName(f'X_{u}_{v}').x, 0) == 1:
                sol.append((u,v))
        return sol

    else:
        return list()


if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20)
    solution = solveMinMaxMatching(G)
    print('Minimum maximal matching: {}'.format(solution))
