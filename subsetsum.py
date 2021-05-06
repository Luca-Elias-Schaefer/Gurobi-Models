from gurobipy import *
import random as rd


def solveSubsetSum(set: dict, target: int) -> dict:
    """
    Solves the subset sum problem.
    :param set: Dict of elements (keys) and integers (values)
    :param target: Target value (int)
    :return: Dict of elements along with their keys.
    """
    subsetsum = Model('subsetsum')

    # Variable
    X = {}

    for a in set.keys():
        X[a] = subsetsum.addVar(vtype=GRB.BINARY, name=f'X_{a}')

    # Objective function
    subsetsum.setObjective(0)

    # Constraint
    subsetsum.addConstr(quicksum(set[a] * X[a] for a in set.keys()), GRB.EQUAL, target)

    # Solve model
    subsetsum.update()
    subsetsum.optimize()

    if subsetsum.status == GRB.OPTIMAL:
        solution = dict()
        for a in set.keys():
            if round(subsetsum.getVarByName(f'X_{a}').x, 0) == 1:
                solution[a] = set[a]
        return solution

    else:
        return None



if __name__ == '__main__':
    # Example: 10 integer numbers between 1 and 10
    target = 20
    set = {a: rd.randint(0, 10) for a in range(1, 11)}

    solution = solveSubsetSum(set, target)
    print('Chosen integers: {}'.format(solution))
