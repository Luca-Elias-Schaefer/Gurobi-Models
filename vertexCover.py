from gurobipy import *
import networkx as nx


def solveVertexCover(G: nx.Graph) -> list:
    """
    Solves the vertex cover problem.
    :param G: undirected graph
    :return: List of nodes
    """
    vertexCover = Model('VertexCover')

    # Variables
    X = {}

    for v in G.nodes():
        X[v] = vertexCover.addVar(vtype=GRB.BINARY, name=f'X_{v}')

    # Objective function
    vertexCover.setObjective(quicksum(X[v] for v in G.nodes()), sense=GRB.MINIMIZE)

    # Constraint
    for u,v in G.edges():
        vertexCover.addConstr(X[u] + X[v], GRB.GREATER_EQUAL, 1.0)

    # Solve model
    vertexCover.update()
    vertexCover.optimize()

    if vertexCover.status == GRB.OPTIMAL:
        nodesInCover = list()
        for u in G.nodes():
            if round(vertexCover.getVarByName(f'X_{u}').x, 0) == 1:
                nodesInCover.append(u)

        return nodesInCover

    else:
        return list()




if __name__ == '__main__':
    # Example: Ladder graph on 20 vertices
    G = nx.ladder_graph(20)

    vertexCover = solveVertexCover(G)
    print('Cover nodes: {}'.format(vertexCover))