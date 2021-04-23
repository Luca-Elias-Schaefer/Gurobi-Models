from gurobipy import *
import random as rd


def solveHubLocation(customers: list, weights: dict, distances: dict, discountFactor: float, numHubs: int):
    """
    Solves the uncapacitated multiple allocation p-Hub median location problem.
    :param customers: List of customers
    :param weights: Dict of weights
    :param distances: Dict of distances (satisfying triangle inequality)
    :param discountFactor: Discount factor between 0 and 1
    :param numHubs: Number of hubs (smaller or equal number of customers)
    :return: Optimal hubs and routing through resulting hub network
    """
    HubLocation = Model('HubLocation')

    # Assignment variables
    X = dict()
    # Hub variables
    Y = dict()

    for i in customers:
        Y[i] = HubLocation.addVar(vtype=GRB.BINARY, name=f'Y_{i}')
        for j in customers:
            for k in customers:
                for l in customers:
                    X[i, j, k, l] = HubLocation.addVar(vtype=GRB.CONTINUOUS, lb=0, ub=1, name=f'X_{i}_{j}_{k}_{l}')

    # Objective function
    HubLocation.setObjective(quicksum(quicksum(quicksum(quicksum(X[i, j, k, l]*weights[i,j]*(distances[i, k] + discountFactor*distances[k, l] + distances[l, j]) for l in customers) for k in customers) for j in customers) for i in customers), sense=GRB.MINIMIZE)

    # Constraints
    for i in customers:
        for j in customers:
            HubLocation.addConstr(quicksum(quicksum(X[i, j, k, l] for k in customers) for l in customers), GRB.EQUAL, 1)

    HubLocation.addConstr(quicksum(Y[i] for i in customers), GRB.EQUAL, numHubs)

    for i in customers:
        for j in customers:
            for k in customers:
                HubLocation.addConstr(quicksum(X[i, j, k, l] for l in customers), GRB.LESS_EQUAL, Y[k])
                HubLocation.addConstr(quicksum(X[i, j, l, k] for l in customers), GRB.LESS_EQUAL, Y[k])


    # Solve model
    HubLocation.update()
    HubLocation.optimize()

    if HubLocation.status == GRB.OPTIMAL:
        assignment = dict()
        hubs = list()

        for i in customers:
            if round(HubLocation.getVarByName(f'Y_{i}').x, 0) == 1:
                hubs.append(i)
            for j in customers:
                for k in customers:
                    for l in customers:
                        if HubLocation.getVarByName(f'X_{i}_{j}_{k}_{l}').x > 0:
                            assignment[i, j, k, l] = HubLocation.getVarByName(f'X_{i}_{j}_{k}_{l}').x

        return assignment, hubs

    else:
        return None, None


if __name__ == '__main__':

    customers = [i for i in range(10)]
    weights = {(i, j): rd.randint(5, 15) for i in customers for j in customers}
    distances = {(i,j): rd.randint(3,36) for i in customers for j in customers}
    discountFactor = 0.2
    numHubs = 3

    assignment, hubs = solveHubLocation(customers, weights, distances, discountFactor, numHubs)
    print('Assignment: {}'.format(assignment))
    print('Hubs: {}'.format(hubs))





