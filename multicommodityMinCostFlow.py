from gurobipy import *
import networkx as nx
import random as rd


def solveMulticommodityMinCostFlow(G: nx.DiGraph, commodities: dict, demands: dict) -> dict:
    """
    Solves the multicommodity minimum cost flow problem.
    :param G: directed graph
    :param commodities: Dict of source-sink-pairs
    :param demand: Dict of demand values (for each commodity)
    :return: Dict of edges and flow values
    """
    multicommodityFlow = Model('multicommodityMinCostFlow')

    # Variable
    X = dict()

    for k in commodities:
        for a in G.edges():
            X[a, k] = multicommodityFlow.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=G.get_edge_data(*a)['capacity'],
                                                name=f'X_{a}_{k}')

    # Objective function
    multicommodityFlow.setObjective(
        quicksum(quicksum(X[a, k] * G.get_edge_data(*a)['cost'] for a in G.edges()) for k in commodities),
        sense=GRB.MINIMIZE)


    # Constraints
    for k, val in commodities.items():
        for v in G.nodes():
            if v == val[0]:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, demands[k])
            elif v == val[1]:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, -demands[k])
            else:
                multicommodityFlow.addConstr(
                    quicksum(X[a, k] for a in G.out_edges(v)) - quicksum(X[a, k] for a in G.in_edges(v)),
                    GRB.EQUAL, 0)


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
    # Example: Complete graph on 100 vertices
    G = nx.complete_graph(100).to_directed()
    for a in G.edges():
        G[a[0]][a[1]]['capacity'] = rd.randint(1, 14)
        G[a[0]][a[1]]['cost'] = rd.randint(1, 14)

    commodities = {1: [0, 4], 2: [1, 3]}
    demands = {1: 3, 2: 4}

    flows = solveMulticommodityMinCostFlow(G, commodities, demands)

    for k in commodities:
        print('Min cost flow edges of commodity {}: {}'.format(k, flows[k]))


