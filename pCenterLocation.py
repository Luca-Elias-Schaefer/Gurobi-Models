from gurobipy import *
import networkx as nx
import random as rd

def solvepCenterLocation(G: nx.Graph, p: int, distances: dict) -> list:

    pcenterlocation = Model(name='pcenterlocation')

    Y = dict()
    X = dict()

    M = pcenterlocation.addVar(vtype=GRB.CONTINUOUS, name='M')

    for u in G.nodes():
        X[u] = pcenterlocation.addVar(vtype=GRB.BINARY, name=f'X_{u}')
        for v in G.nodes():
            Y[u,v] = pcenterlocation.addVar(vtype=GRB.BINARY, name=f'Y_{u}_{v}')

    for u in G.nodes():
        pcenterlocation.addConstr(quicksum(Y[u,v] for v in G.nodes()), GRB.EQUAL, 1)

    pcenterlocation.addConstr(quicksum(X[u] for u in G.nodes()), GRB.LESS_EQUAL, p)

    for u in G.nodes():
        for v in G.nodes():
            pcenterlocation.addConstr(Y[u,v], GRB.LESS_EQUAL, X[v])
            pcenterlocation.addConstr(Y[u,v]*distances[u][v]*G.nodes[u]['demand'], GRB.LESS_EQUAL, M)

    pcenterlocation.setObjective(M, sense=GRB.MINIMIZE)

    pcenterlocation.update()
    pcenterlocation.optimize()

    if pcenterlocation.status == GRB.OPTIMAL:
        pcenter = list()
        for u in G.nodes():
            if pcenterlocation.getVarByName(f'X_{u}').x == 1:
                pcenter.append(u)

        return pcenter

    else:
        return []


if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20)
    for u,v in G.edges():
        G[u][v]['length'] = rd.randint(1,23)

    for u in G.nodes():
        G.nodes[u]['demand'] = rd.randint(1,10)

    distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

    solution = solvepCenterLocation(G, 4, distances)
    print('Locations: {}'.format(solution))
