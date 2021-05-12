from gurobipy import *
import networkx as nx
import random as rd


def solvePMedian(G: nx.Graph, p: int, distances: dict) -> dict:
    """
    Solves the p-Median location problem.
    :param G: undirected graph
    :param p: Number of facilities
    :param distances: Dict of distances
    :return: Dict of nodes
    """
    pMedian = Model('pMedian')

    # Variables
    Y = {}
    X = {}

    for v in G.nodes():
        Y[v] = pMedian.addVar(vtype=GRB.BINARY, name=f'Y_{v}')
        for u in G.nodes():
            X[v,u] = pMedian.addVar(vtype=GRB.BINARY, name=f'X_{v}_{u}')

    # Objective function
    pMedian.setObjective(
        quicksum(X[v, u] * G.nodes()[v]['demand'] * distances[v][u] for v in G.nodes() for u in G.nodes()),
        sense=GRB.MINIMIZE)

    # Constraints
    for v in G.nodes():
        pMedian.addConstr(quicksum(X[v,u] for u in G.nodes()), GRB.EQUAL, 1)
        for u in G.nodes():
            pMedian.addConstr(X[v,u], GRB.LESS_EQUAL, Y[u])

    pMedian.addConstr(quicksum(Y[v] for v in G.nodes()), GRB.EQUAL, p)

    # Solve model
    pMedian.update()
    pMedian.optimize()

    if pMedian.status == GRB.OPTIMAL:
        assignment = dict()
        for v in G.nodes():
            for u in G.nodes():
                if round(pMedian.getVarByName(f'X_{v}_{u}').x, 0) == 1:
                    assignment[v] = u

        return assignment

    else:
        return dict()




if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    rd.seed(0)
    G = nx.complete_graph(20)

    for u,v in G.edges():
        G[u][v]['length'] = rd.randint(1,15)

    for v in G.nodes():
        G.nodes[v]['demand'] = rd.randint(4,13)

    distances = dict(nx.all_pairs_dijkstra_path_length(G, weight='length'))

    assignment = solvePMedian(G, 3, distances)
    print('Assignment: {}'.format(assignment))