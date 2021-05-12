from gurobipy import *
import random as rd


def solveKnaosack(items: list, profits: dict, weights: dict, capacity: int) -> list:
    """
    Solves the binary knapsack problem.
    :param items: List of items
    :param profits: Profit values of the items
    :param weights: Weight values of the items
    :param capacity: Knapsack capacity
    :return: List of items
    """
    knapsack = Model('knapsack')

    # Variable
    X = dict()

    for i in items:
        X[i] = knapsack.addVar(vtype=GRB.BINARY, name=f'X_{i}')

    # Objective function
    knapsack.setObjective(quicksum(profits[i] * X[i] for i in items), GRB.MAXIMIZE)

    # Constraint
    knapsack.addConstr(quicksum(X[i] * weights[i] for i in items), GRB.LESS_EQUAL, capacity)

    # Solve model
    knapsack.update()
    knapsack.optimize()


    if knapsack.status == GRB.OPTIMAL:
        optitems = list()
        for i in items:
            if round(knapsack.getVarByName(f'X_{i}').x, 0) == 1:
                optitems.append(i)
        return optitems

    else:
        return list()



if __name__ == '__main__':
    # Example with 10 knapsack items
    items = [i for i in range(1, 11)]
    profits = {i: rd.randint(0, 10) for i in items}
    weights = {i: rd.randint(0, 10) for i in items}
    capacity = 15

    optitems = solveKnaosack(items, profits, weights, capacity)
    print('Optimal items: {}'.format(optitems))

