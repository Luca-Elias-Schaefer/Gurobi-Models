from gurobipy import *
import networkx as nx
import random as rd


def solveQuadraticAssignment(facilities: list, locations: list, weights: dict, distances: dict) -> dict:
    """
    Solves the quadratic assignment problem.
    :param facilities: List of facilities
    :param locations: List of locations
    :param weights: Dict of weights between facilities
    :param distances: Dict of distances between locations
    :return: Dict of assignments
    """
    quadrarticAssignment = Model('QAP')

    # Variable
    X = dict()

    for location in locations:
        for facility in facilities:
            X[location, facility] = quadrarticAssignment.addVar(vtype=GRB.BINARY, name=f'X_{location}_{facility}')

    # Objective function
    quadrarticAssignment.setObjective(quicksum(quicksum(
        weights[a, b] * quicksum(quicksum(distances[i, j] * X[i, a] * X[j, b] for i in locations) for j in locations)
        for a in facilities) for b in facilities), sense=GRB.MINIMIZE)

    # Constraints
    for i in locations:
        quadrarticAssignment.addConstr(quicksum(X[i, a] for a in facilities), GRB.EQUAL, 1)

    for a in facilities:
        quadrarticAssignment.addConstr(quicksum(X[i, a] for i in locations), GRB.EQUAL, 1)

    # Solve model
    quadrarticAssignment.update()
    quadrarticAssignment.optimize()

    if quadrarticAssignment.status == GRB.OPTIMAL:
        assignment = dict()
        for i in locations:
            for j in facilities:
                if quadrarticAssignment.getVarByName(f'X_{i}_{j}').x > 0:
                    assignment[i, j] = quadrarticAssignment.getVarByName(f'X_{i}_{j}').x
        return assignment

    else:
        return dict()




if __name__ == '__main__':
    # Example: 8 facilities, 8 locations
    facilities = [i for i in range(1, 9)]
    locations = [j for j in range(9, 17)]
    weights = {(i, j): rd.randint(1, 10) for i in facilities for j in facilities}
    distances = {(i, j): rd.randint(1, 10) for i in locations for j in locations}

    assignment = solveQuadraticAssignment(facilities, locations, weights, distances)
    for key in assignment.keys():
        print(f'Location {key[0]} is assigned to facility {key[1]}')



