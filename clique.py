from gurobipy import *
import networkx as nx


def solveClique(G: nx.Graph) -> list:
    """
    Solves the maximum clique problem.
    :param G: undirected graph
    :return: List of nodes
    """
    clique = Model('Clique')

    # Variable
    X = dict()

    for u in G.nodes():
        X[u] = clique.addVar(vtype=GRB.BINARY, name=f'X_{u}')

    # Constraints
    for u in G.nodes():
        for v in G.nodes():
            if (((u,v) not in G.edges()) or ((v,u) not in G.edges())) and (u != v):
                clique.addConstr(X[u] + X[v], GRB.LESS_EQUAL, 1)

    # Objective function
    clique.setObjective(quicksum(X[u] for u in G.nodes()), sense=GRB.MAXIMIZE)

    clique.update()
    clique.optimize()

    if clique.status == GRB.OPTIMAL:
        solution = list()
        for u in G.nodes():
            if round(clique.getVarByName(f'X_{u}').x, 0) == 1:
                solution.append(u)
        return solution

    else:
        return None


if __name__ == '__main__':
    # Example: Graph with 5 nodes and 5 edges
    G = nx.Graph()
    G.add_edges_from([(2,3), (3,1), (3,4), (3,5), (4,5)])

    sol = solveClique(G)
    print('Clique nodes: {}'.format(sol))