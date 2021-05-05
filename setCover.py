from gurobipy import *
import random as rd


def solveSetCover(S: list, C: list) -> list:
    """
    Solves the set cover problem.
    :param S: List of elements (ground set)
    :param C: List of lists over elements in S (collection of subsets)
    :return: List of lists.
    """
    setCover = Model('setCover')

    # Variable
    Y = {}

    for i in range(len(C)):
        Y[i] = setCover.addVar(vtype=GRB.BINARY, name=f'Y_{i}')

    # Objective function
    setCover.setObjective(quicksum(Y[i] for i in range(len(C))), sense=GRB.MINIMIZE)

    # Constraint
    for s in S:
        setCover.addConstr(1, GRB.LESS_EQUAL, quicksum(Y[i] for i in range(len(C)) if s in C[i]))

    # Solve model
    setCover.update()
    setCover.optimize()

    if setCover.status == GRB.OPTIMAL:
        solution = list()
        for i in range(len(C)):
            if round(setCover.getVarByName(f'Y_{i}').x, 0) == 1:
                solution.append(C[i])
        return solution

    else:
        return None




if __name__ == '__main__':
    # Example: Set of 20 elements, collection C of 25 subsets of S
    S = list(range(20))
    C = []
    for i in range(25):
        number = rd.randint(1, 4)
        C.append(rd.sample(S, number))

    if {x for l in C for x in l} == set(S):
        sets = solveSetCover(S, C)
        print(sets)

    else:
        print('No feasible solution.')

