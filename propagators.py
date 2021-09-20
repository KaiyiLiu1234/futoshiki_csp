#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.
import itertools
'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''
    #IMPLEMENT
    list_of_values_pruned = []
    if newVar:
        all_constraints = csp.get_cons_with_var(newVar)
    else:
        all_constraints = csp.get_all_cons()
    for constraint in all_constraints:
        if constraint.get_n_unasgn() == 1: # one unassigned variable
            unassigned_var = constraint.get_unasgn_vars()[0]
            unassigned_var_index = None
            vals = []
            for index, var in enumerate(constraint.get_scope()):
                if var.name != unassigned_var.name:
                    vals.append(var.get_assigned_value())
                else:
                    unassigned_var_index = index
            current_domain = unassigned_var.cur_domain()
            for value in current_domain:
                vals.insert(unassigned_var_index, value)
                if not constraint.check(vals):
                    unassigned_var.prune_value(value)
                    list_of_values_pruned.append((unassigned_var, value))
                vals.pop(unassigned_var_index)
            if unassigned_var.cur_domain_size() == 0: # all values have been pruned
                return False, list_of_values_pruned

    return True, list_of_values_pruned


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''
    #IMPLEMENT
    gac_queue = []
    list_of_values_pruned = []
    if newVar:
        # assume that newVar has been assigned
        gac_queue.extend(csp.get_cons_with_var(newVar))
    else: # if newVar does not exist
        gac_queue.extend(csp.get_all_cons())

    while gac_queue: # while gac_queue is not empty
        constraint = gac_queue.pop(0) # retrieve first element
        variables = constraint.get_scope() # retrieve all variables in constraint
        for var in variables:
            #print(var)
            for value in var.cur_domain():
                # if constraint has a support, no pruning is necessary
                #print(constraint.has_support(var, value), value)
                if not constraint.has_support(var, value):
                    # check if value has support given variable and value
                    possible_comb = []
                    for var_two in constraint.get_scope():
                        if var_two is not var:
                            possible_comb.append(var_two.cur_domain())
                        else:
                            possible_comb.append([value])
                    combinations = itertools.product(*possible_comb)

                    solution_list = list(filter(lambda comb: constraint.check(comb), combinations))
                    if not solution_list:
                        var.prune_value(value)
                        list_of_values_pruned.append((var, value))
                        # add constraints with the variable back into the queue
                        for constraint in csp.get_cons_with_var(var):
                            if constraint not in gac_queue:
                                #print(value)
                                #print(constraint)
                                gac_queue.append(constraint)



            if var.cur_domain_size() == 0: # Domain Wipeout if a variable has no more values
                return False, list_of_values_pruned

    # if we make it out of the queue without encountering a domain wipeout
    # we have succeeded in pruning everything
    #print(list_of_values_pruned)
    return True, list_of_values_pruned


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    #IMPLEMENT
    all_variables_in_csp = csp.get_all_unasgn_vars()
    minimum_variable_tuple = min([(var, var.cur_domain_size()) for var in all_variables_in_csp], key=lambda x: x[1])
    return minimum_variable_tuple[0]

