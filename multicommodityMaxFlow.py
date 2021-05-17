from gurobipy import *
import networkx as nx
import random as rd


def solveMaximumMulticommodityFlow(G: nx.DiGraph, commodities: dict) -> dict:
    """
    Solves the multicommodity maximum flow problem.
    :param G: directed graph
    :param commodities: Dict of source-sink-pairs
    :return: Dict of edges and flow values
    """
    multicommodityFlow = Model('MulticommodityFlow')

    # Variable
    X = dict()
    B = dict()

    for k in commodities:
        B[k] = multicommodityFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, name=f'B_{k}')
        for a in G.edges():
            X[a, k] = multicommodityFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=G.get_edge_data(*a)['capacity'],
                                                name=f'X_{a}_{k}')

    # Objective function
    multicommodityFlow.setObjective(quicksum(B[k] for k in commodities), sense=GRB.MAXIMIZE)

    # Constraints
    for k, val in commodities.items():
        for v in G.nodes():
            if v == val[0]:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, B[k])
            elif v == val[1]:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, -B[k])
            else:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, 0)

    for a in G.edges():
        multicommodityFlow.addConstr(quicksum(X[a, k] for k in commodities), GRB.LESS_EQUAL,
                                     G.get_edge_data(*a)['capacity'])

    # Solve model
    multicommodityFlow.update()
    multicommodityFlow.optimize()

    if multicommodityFlow.status == GRB.OPTIMAL:
        flows = dict()
        for k in commodities:
            flows[k] = dict()
            for a in G.edges():
                if multicommodityFlow.getVarByName(f'X_{a}_{k}').x > 0:
                    flows[k][a] = multicommodityFlow.getVarByName(f'X_{a}_{k}').x
        return flows

    else:
        return dict()


if __name__ == '__main__':
    # Example: Complete graph on 5 vertices
    G = nx.complete_graph(5).to_directed()
    for a in G.edges():
        G[a[0]][a[1]]['capacity'] = rd.randint(0, 4)

    commodities = {1: [0, 4], 2: [1, 3]}

    flows = solveMaximumMulticommodityFlow(G, commodities)

    for k in commodities:
        print('Max flow edges of commodity {}: {}'.format(k, flows[k]))




