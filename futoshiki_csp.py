#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = futoshiki_csp_model_1(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the Futoshiki puzzle.

1. futoshiki_csp_model_1 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only
      binary not-equal constraints for both the row and column constraints.

2. futoshiki_csp_model_2 (worth 20/100 marks)
    - A model of a Futoshiki grid built using only n-ary
      all-different constraints for both the row and column constraints.

'''
from cspbase import *
import itertools

def futoshiki_csp_model_1(futo_grid):
    # Part 1: Record Variables
    list_of_list_of_variables = []
    futoshiki_grid = []
    list_of_constraints = []
    domain = [value for value in range(1, len(futo_grid) + 1)]
    for i in range(len(futo_grid)):
        variables_in_a_row = []
        elements_in_a_row = []
        for j, column in enumerate(futo_grid[i]):
            if column == 0: # an unassigned variable
                new_var = Variable("V-" + str(i) + str(j), domain)
                variables_in_a_row.append(new_var)
                elements_in_a_row.append(new_var)
            elif type(column) != str and column != 0:
                new_var = Variable("V-" + str(i) + str(j), [column])
                new_var.assign(column)
                variables_in_a_row.append(new_var)
                elements_in_a_row.append(new_var)
            else:
                elements_in_a_row.append(column)
        list_of_list_of_variables.append(variables_in_a_row)
        futoshiki_grid.append(elements_in_a_row)
    #print(list_of_list_of_variables)
    # Part 2: Record binary inequality constraints
    for i in range(len(futoshiki_grid)):
        for j, column in enumerate(futoshiki_grid[i]):
            if column == '>' or column == '<': # greater than binary constraint
                var_scope = (futoshiki_grid[i][j-1], futoshiki_grid[i][j+1])
                new_constraint = Constraint("C-ineq-" + str(i) + str(j), var_scope)
                # generate cartesian product of domains twice
                if column == '>':
                    list_of_satisfy_tuples = [comb for comb in list(itertools.product(var_scope[0].cur_domain(), var_scope[1].cur_domain())) if comb[0] > comb[1]]
                else:
                    list_of_satisfy_tuples = [comb for comb in list(itertools.product(var_scope[0].cur_domain(), var_scope[1].cur_domain())) if comb[0] < comb[1]]
                new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
                list_of_constraints.append(new_constraint)
    # Part 3: Record Binary Row Constraints
    # list of domain combinations which aren't equal to one another (these are tuples which will satisfy the row and column constraints)
    list_of_satisfy_tuples = [comb for comb in list(itertools.product(domain, repeat=2)) if comb[0] != comb[1]]
    for index, row in enumerate(list_of_list_of_variables):
        for variable_combination in list(itertools.combinations(row, 2)):
            new_constraint = Constraint("C-row-" + str(index), variable_combination)
            new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
            list_of_constraints.append(new_constraint)
    # Part 4: Record Binary Column Constraints

    list_of_columns = []
    for j in range(len(list_of_list_of_variables)):
        column = []
        for i in range(len(list_of_list_of_variables)):
            column.append(list_of_list_of_variables[i][j])
        list_of_columns.append(column)

    for index, column in enumerate(list_of_columns):
        combinations = list(itertools.combinations(column, 2))
        for variable_combination in combinations:
            new_constraint = Constraint("C-column-" + str(index), variable_combination)
            new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
            list_of_constraints.append(new_constraint)
    # Create CSP
    new_csp = CSP("ModelOneCSP")
    for index in range(len(list_of_list_of_variables)):
        for variable in list_of_list_of_variables[index]:
            new_csp.add_var(variable)

    for constraint in list_of_constraints:
        new_csp.add_constraint(constraint)

    return new_csp, list_of_list_of_variables


def futoshiki_csp_model_2(futo_grid):
    # Part 1: Record Variables
    list_of_list_of_variables = []
    futoshiki_grid = []
    list_of_constraints = []
    domain = [value for value in range(1, len(futo_grid) + 1)]
    for i in range(len(futo_grid)):
        variables_in_a_row = []
        elements_in_a_row = []
        for j, column in enumerate(futo_grid[i]):
            if column == 0: # an unassigned variable
                new_var = Variable("V-" + str(i) + str(j), domain)
                variables_in_a_row.append(new_var)
                elements_in_a_row.append(new_var)
            elif type(column) != str and column != 0:
                new_var = Variable("V-" + str(i) + str(j), [column])
                new_var.assign(column)
                variables_in_a_row.append(new_var)
                elements_in_a_row.append(new_var)
            else:
                elements_in_a_row.append(column)
        list_of_list_of_variables.append(variables_in_a_row)
        futoshiki_grid.append(elements_in_a_row)
    #print(list_of_list_of_variables)
    # Part 2: Record binary inequality constraints
    for i in range(len(futoshiki_grid)):
        for j, column in enumerate(futoshiki_grid[i]):
            if column == '>' or column == '<': # greater than binary constraint
                var_scope = (futoshiki_grid[i][j-1], futoshiki_grid[i][j+1])
                new_constraint = Constraint("C-ineq-" + str(i) + str(j), var_scope)
                # generate cartesian product of domains twice
                if column == '>':
                    list_of_satisfy_tuples = [comb for comb in list(itertools.product(var_scope[0].cur_domain(), var_scope[1].cur_domain())) if comb[0] > comb[1]]
                else:
                    list_of_satisfy_tuples = [comb for comb in list(itertools.product(var_scope[0].cur_domain(), var_scope[1].cur_domain())) if comb[0] < comb[1]]
                new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
                list_of_constraints.append(new_constraint)
    # Part 3: Record n-ary Row Constraints
    # list of domain combinations which aren't equal to one another (these are tuples which will satisfy the row and column constraints)
    list_of_satisfy_tuples = list(itertools.permutations(domain))
    for index, row in enumerate(list_of_list_of_variables):
        new_constraint = Constraint("C-row-" + str(index), row)
        new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
        list_of_constraints.append(new_constraint)
    # Part 4: Record n-ary Column Constraints
    list_of_columns = []
    for j in range(len(list_of_list_of_variables)):
        column = []
        for i in range(len(list_of_list_of_variables)):
            column.append(list_of_list_of_variables[i][j])
        list_of_columns.append(column)

    for index, column in enumerate(list_of_columns):
        new_constraint = Constraint("C-column-" + str(index), column)
        new_constraint.add_satisfying_tuples(list_of_satisfy_tuples)
        list_of_constraints.append(new_constraint)
    # Create CSP
    new_csp = CSP("ModelTwoCSP")
    for index in range(len(list_of_list_of_variables)):
        for variable in list_of_list_of_variables[index]:
            new_csp.add_var(variable)

    for constraint in list_of_constraints:
        new_csp.add_constraint(constraint)

    return new_csp, list_of_list_of_variables

