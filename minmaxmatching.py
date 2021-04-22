from gurobipy import *
import networkx as nx
import random as rd

def solveMinMaxMatching(G: nx.Graph) -> list:

    minmaxMatching = Model(name='minmaxMatching')

    X = {}
    for u,v in G.edges():
        X[u,v] = minmaxMatching.addVar(vtype=GRB.BINARY, name=f'X_{u}_{v}')

    for u in G.nodes():
        minmaxMatching.addConstr(quicksum(X[v,w] for v,w in G.edges() if v == u or w == u), GRB.LESS_EQUAL, 1)

    for u,v in G.edges():
        minmaxMatching.addConstr(1-X[u,v], GRB.LESS_EQUAL, quicksum(X[a,b] for a,b in G.edges() if a == u or b == u and not (a,b) == (u,v))
                                 + quicksum(X[a,b] for a,b in G.edges() if a == v or b == v and not (a,b) == (v,u)))

    minmaxMatching.setObjective(quicksum(X[u,v] for u,v in G.edges()), sense=GRB.MINIMIZE)

    minmaxMatching.update()
    minmaxMatching.optimize()

    if minmaxMatching.status == GRB.OPTIMAL:
        sol = list()
        for u,v in G.edges():
            if minmaxMatching.getVarByName(f'X_{u}_{v}').x == 1:
                sol.append((u,v))
        return sol

    else:
        return []


if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20)
    solution = solveMinMaxMatching(G)
    print('Minimal maximum matching: {}'.format(solution))
