from gurobipy import *
import networkx as nx
import random as rd


def solveBiobjectiveSP(G: nx.DiGraph, source: int, sink: int, objVal) -> dict:
    """
    Computes a (weakly) non-dominated point of the biobjective shortest paths problem.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :param objVal: Bound on second objective
    :return: Dict with objective value and path
    """
    BiobjSP = Model('BiobjSP')

    # Variables
    X = dict()

    for u,v in G.edges():
        X[u,v] = BiobjSP.addVar(vtype=GRB.BINARY, name=f'X_{u}_{v}')

    # Objective function
    BiobjSP.setObjective(quicksum(X[u,v]*G[u][v]['length1'] for u,v in G.edges()), sense=GRB.MINIMIZE)

    # Constraints
    for v in G.nodes():
        if v == source:
            BiobjSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 1)
        elif v == sink:
            BiobjSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, -1)
        else:
            BiobjSP.addConstr(quicksum(X[a] for a in G.out_edges(v)) - quicksum(X[a] for a in G.in_edges(v)),
                                  GRB.EQUAL, 0)

    BiobjSP.addConstr(quicksum(X[u,v]*G[u][v]['length2'] for u,v in G.edges()), GRB.LESS_EQUAL, objVal - 1)

    # Solve model
    BiobjSP.update()
    BiobjSP.optimize()

    if BiobjSP.status == GRB.OPTIMAL:
        SP = dict()
        SP['objVal'] = (BiobjSP.objVal, sum(BiobjSP.getVarByName(f'X_{u}_{v}').x * G[u][v]['length2']
                                            for u,v in G.edges()))
        SP['path'] = list()
        for u,v in G.edges():
            if round(BiobjSP.getVarByName(f'X_{u}_{v}').x, 0) == 1:
                SP['path'].append((u,v))
        return SP

    else:
        return dict()


def epsConstraint(G: nx.DiGraph, source: int, sink: int, objVal):
    """
    Solves the biobjective shortest paths problem by using the epsilon-constraint method and returns
    all (weakly) non-dominated points.
    :param G: directed graph
    :param source: Source node in G
    :param sink: Sink node in G
    :param objVal:
    :return: List with objective values and paths
    """
    M = objVal
    result = list()
    while True:
        SP = solveBiobjectiveSP(G, source, sink, M)
        if not SP == dict():
            result.append(SP)
            M = SP['objVal'][1]
        else:
            return result




if __name__ == '__main__':
    # Example: Complete graph on 20 vertices
    G = nx.complete_graph(20).to_directed()
    source, sink = 1, 14
    for a in G.edges():
        G[a[0]][a[1]]['length1'] = rd.randint(1,14)
        G[a[0]][a[1]]['length2'] = rd.randint(1, 14)

    M = sum(G[u][v]['length2'] for u,v in G.edges())
    result = epsConstraint(G, source, sink, M)

    print('Non-dominated points: {}'.format(result))
