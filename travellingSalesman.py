from gurobipy import *
import networkx as nx
import itertools as it
import random as rd
import time


def solveTSP(G: nx.DiGraph, subtour: str) -> list:
    """
    Solves the travelling salesman problem.
    :param G: directed graph
    :param subtour: String indicating whether classical subtour elimination constraints or Miller-Tucker-Zemlin
    constraints should be used
    :return: List of nodes (tour)
    """
    TSP = Model('TSP')

    # Variable
    X = dict()

    for u, v in G.edges():
        X[u, v] = TSP.addVar(vtype=GRB.BINARY, name=f'X_{u}_{v}')

    # Objective function
    TSP.setObjective(quicksum(X[u, v] * G[u][v]['length'] for u, v in G.edges()), sense=GRB.MINIMIZE)

    # Constraints
    for u in G.nodes():
        TSP.addConstr(quicksum(X[w, v] for w, v in G.out_edges(u)), GRB.EQUAL, 1)
        TSP.addConstr(quicksum(X[w, v] for w, v in G.in_edges(u)), GRB.EQUAL, 1)

    # Subtour elimination constraints
    if subtour == 'classic':
        for r in range(2, len(list(G.nodes()))):
            for set in it.combinations(list(G.nodes()), r):
                TSP.addConstr(quicksum(X[u, v] for u, v in G.edges() if u in set and v in set), GRB.LESS_EQUAL, r-1)

    # Miller-Tucker-Zemlin constraints
    if subtour == 'mtz':
        N = G.number_of_nodes()
        U = dict()
        start = list(G.nodes())[0]
        for u in G.nodes():
            U[u] = TSP.addVar(vtype=GRB.INTEGER, lb=1, ub=N - 1, name=f'U_{u}')

        for u in G.nodes():
            if not u == start:
                for v in G.nodes():
                    if not v == start:
                        if not v == u:
                            TSP.addConstr(U[u] - U[v] + N * X[u, v], GRB.LESS_EQUAL, N - 1)

    # Solve model
    TSP.update()
    TSP.optimize()

    if TSP.status == GRB.OPTIMAL:
        i = 1
        currentNode = list(G.nodes())[0]
        tour = [currentNode]
        while i < G.number_of_nodes() + 1:
            for u, v in G.out_edges(currentNode):
                if round(TSP.getVarByName(f'X_{currentNode}_{v}').x, 0) == 1:
                    tour.append(v)
                    currentNode = v
                    i += 1
                    break
        return tour
    else:
        return None



if __name__ == '__main__':
    # Example: Complete graph on 15 vertices
    rd.seed(1)
    G = nx.complete_graph(15).to_directed()
    for u,v in G.edges():
        G[u][v]['length'] = rd.randint(1, 23)


    startClassic = time.time()
    result = solveTSP(G, 'classic')
    endClassic = time.time()

    startMTZ = time.time()
    resultMTZ = solveTSP(G, 'mtz')
    endMTZ = time.time()

    print('\nTSP using subtour elimination constraints\nOptimal tour: {}, Required time: {}\n'.format(result, endClassic-startClassic))
    print('TSP using Miller-Tucker-Zemlin constraints\nOptimal tour: {}, Required time: {}'.format(resultMTZ, endMTZ-startMTZ))
