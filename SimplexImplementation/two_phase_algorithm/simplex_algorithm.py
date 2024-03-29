from two_phase_algorithm.utils import *
from two_phase_algorithm.z_conversion import *


def get_index_negative_cost(simplex_matrix):
    cost_line = simplex_matrix[-1][:-1]
    for index in range(len(cost_line)):
        if cost_line[index] < 0:
            return index
    return -1


def get_pivot_given_index(simplex_matrix, index_cost_negative):
    positive_per_rhs = []
    indexes_positive = []
    for index_equation in range(len(simplex_matrix[:-1])):
        if simplex_matrix[index_equation][index_cost_negative] > 0:
            positive_per_rhs.append(simplex_matrix[index_equation][-1] /
                                    simplex_matrix[index_equation][index_cost_negative])
            indexes_positive.append(index_equation)

    if len(indexes_positive) != 0:
        # here we apply Bland's rule
        return indexes_positive[positive_per_rhs.index(min(positive_per_rhs))]
    return -1


def exceed_pivotation(simplex_matrix, pivot_index, index_cost_negative_chosen):
    for index_line in range(len(simplex_matrix)):
        if index_line != pivot_index:
            for index_column in range(len(simplex_matrix[0])):
                if index_column != index_cost_negative_chosen:
                    simplex_matrix[index_line][index_column] = \
                        (simplex_matrix[index_line][index_column] *
                         simplex_matrix[pivot_index][index_cost_negative_chosen] -
                         simplex_matrix[index_line][index_cost_negative_chosen] *
                         simplex_matrix[pivot_index][index_column]) / \
                        simplex_matrix[pivot_index][index_cost_negative_chosen]
                    if simplex_matrix[index_line][index_column] == 0:
                        simplex_matrix[index_line][index_column] = 0

    for index_line in range(len(simplex_matrix)):
        if index_line != pivot_index:
            simplex_matrix[index_line][index_cost_negative_chosen] = 0

    for index_column in range(len(simplex_matrix[0])):
        if index_column != index_cost_negative_chosen:
            simplex_matrix[pivot_index][index_column] = simplex_matrix[pivot_index][index_column] / \
                                                        simplex_matrix[pivot_index][index_cost_negative_chosen]
            if simplex_matrix[pivot_index][index_column] == 0:
                simplex_matrix[pivot_index][index_column] = 0

    simplex_matrix[pivot_index][index_cost_negative_chosen] = 1.0
    return simplex_matrix


def update_labels_base_vars_after_pivoting(column_names, labels_vars_from_base,
                                           pivot_index, index_cost_negative_chosen):
    in_var = column_names[index_cost_negative_chosen]
    labels_vars_from_base[pivot_index] = in_var
    return labels_vars_from_base


def get_solution(simplex_matrix, labels_vars_from_base, column_names):
    solution = []
    for index_var in range(len(column_names) - 1):
        if column_names[index_var] in labels_vars_from_base:
            solution.append(
                (column_names[index_var], simplex_matrix[labels_vars_from_base.index(column_names[index_var])][-1]))
        else:
            solution.append((column_names[index_var], 0))
    return solution


def prettify_solution(solution):
    str_solution = 'The solution of the system is: \n'
    for var_tuple in solution:
        str_solution += var_tuple[0] + ' = ' + str(var_tuple[1]) + '\n'
    return str_solution


def get_cost_value_based_on_solution(solution, z, z_free_term):
    z_value = 0
    for index in range(len(z)):
        z_value += z[index] * solution[index][1]
    z_value -= z_free_term
    return z_value


def check_for_alternative_solution(simplex_matrix, labels_vars_from_base):
    indexes_bars_from_base = [int(label.split('_')[1]) - 1 for label in labels_vars_from_base[:-1]]
    for i in range(len(simplex_matrix[-1])):
        if i not in indexes_bars_from_base and simplex_matrix[-1][i] == 0:
            logger.info("The system has an alternative solution. Another pivoting step can be done.")
            return i
    logger.info("This is the unique optima solution.")
    return -1


def check_if_simplex_tableau_is_optimal(simplex_matrix, labels_vars_from_base):
    indexes_base_vars = [int(label.split('_')[1]) - 1 for label in labels_vars_from_base[:-1]]
    cost_line = simplex_matrix[-1]

    for index in indexes_base_vars:
        if cost_line[index] != 0:
           return False
    return True


def get_simplex_solution(simplex_matrix, labels_vars_from_base, column_names, z, z_free_term):
    solution = get_solution(simplex_matrix, labels_vars_from_base, column_names)
    logger.info(prettify_solution(solution))
    logger.info("The value for z is : " + str(get_cost_value_based_on_solution(solution, z, z_free_term)))
    return solution


def get_non_negative_x_value_on_line(simplex_tableaux, column_names, index_eq):
    for index_term in range(len(simplex_tableaux[index_eq][:-1])):
        if column_names[index_term].startswith('x') and simplex_tableaux[index_eq][index_term] != 0:
            return index_term
    return None


def remove_artificial_variables_from_base(simplex_tableaux, column_names, labels_vars_from_base):
    flag_there_are_redundant_eq = False
    modified_simplex_tableau = []
    for index_eq in range(len(labels_vars_from_base)):
        # we have currently an artificial variable in base
        if labels_vars_from_base[index_eq].startswith('y'):

            # we iterate through that line search for values != 0 for x-es
            idx_non_negative_x = get_non_negative_x_value_on_line(simplex_tableaux, column_names, index_eq)

            if idx_non_negative_x == None:
                # it means that eq is redundant so we can omit it for phase 2
                flag_there_are_redundant_eq = True
                continue
            else:
                to_be_removed = labels_vars_from_base[index_eq]
                simplex_tableaux = exceed_pivotation(simplex_tableaux, index_eq, idx_non_negative_x)
                labels_vars_from_base = update_labels_base_vars_after_pivoting(column_names, labels_vars_from_base,
                                                                               index_eq, idx_non_negative_x)
                logger.info('The system after the removing the variable ' + to_be_removed +
                            ' from base is  \n\n' + str(pd.DataFrame(simplex_tableaux,
                                                                     columns=column_names,
                                                                     index=labels_vars_from_base)) + '\n\n')
                modified_simplex_tableau.append(simplex_tableaux[index_eq])
        else:
            modified_simplex_tableau.append(simplex_tableaux[index_eq])

    if flag_there_are_redundant_eq:
        labels_vars_from_base = [label for label in labels_vars_from_base if 'y' not in label]

        logger.info('The system after the removing all the redundant equations is  \n\n' +
                    str(pd.DataFrame(modified_simplex_tableau, columns=column_names,
                                     index=labels_vars_from_base)) + '\n\n')

    return modified_simplex_tableau, labels_vars_from_base


def search_for_alternative_solution(simplex_matrix, labels_vars_from_base, column_names, z, z_free_term):
    # check for alternative solutions
    i_zero_alternative = check_for_alternative_solution(simplex_matrix, labels_vars_from_base)

    if i_zero_alternative != -1:
        pivot_index = get_pivot_given_index(simplex_matrix, i_zero_alternative)

        if pivot_index != -1:
            simplex_matrix = exceed_pivotation(simplex_matrix, pivot_index, i_zero_alternative)
            labels_vars_from_base = update_labels_base_vars_after_pivoting(column_names, labels_vars_from_base,
                                                                           pivot_index, i_zero_alternative)

            logger.info('The system after the pivoting step is: \n\n' +
                        str(pd.DataFrame(simplex_matrix,
                                         columns=column_names,
                                         index=labels_vars_from_base)) + '\n\n')

            solution = get_simplex_solution(simplex_matrix, labels_vars_from_base, column_names, z, z_free_term)
            return solution

    return None


def finish_simplex_step(simplex_matrix, column_names, labels_vars_from_base, z, z_free_term,
                        search_alternative=False, phase_one=False):

    simplex_matrix, labels_vars_from_base = remove_artificial_variables_from_base(simplex_matrix, column_names,
                                                                                  labels_vars_from_base)

    if phase_one and simplex_matrix[-1][-1] != 0:
        logger.info("The value for z is different than 0. The problem is infeasible. The second phase is "
                    "not going to be executed. \n\n")
        return None, None, None, None

    if phase_one and simplex_matrix[-1][-1] == 0:
        logger.info("The simplex tableau is optimal. The initial problem is feasible. The second phase is "
                    "going to be started.\n\n")
    else:
        logger.info("The simplex tableau is optimal.\n\n")

    solution = get_simplex_solution(simplex_matrix, labels_vars_from_base, column_names, z, z_free_term)
    if search_alternative:
        solution_alternative = search_for_alternative_solution(simplex_matrix, labels_vars_from_base, column_names,
                                                               z, z_free_term)
    logger.info("The simplex iterations are finished. \n\n")
    return simplex_matrix, column_names, labels_vars_from_base, solution


def simplex_algorithm(simplex_matrix, column_names, labels_vars_from_base, z, z_free_term,
                      search_alternative=False, phase_one=False):
    index_cost_negative = get_index_negative_cost(simplex_matrix)

    if index_cost_negative == -1:
        optimal = check_if_simplex_tableau_is_optimal(simplex_matrix, labels_vars_from_base)
        if not optimal:
            logger.info("The simplex tableau is not optimal. The system has no solution. \n\n")
            return None, None, None, None
        else:
            return finish_simplex_step(simplex_matrix, column_names, labels_vars_from_base, z, z_free_term,
                                       search_alternative, phase_one)

    while index_cost_negative != -1:
        pivot_index = get_pivot_given_index(simplex_matrix, index_cost_negative)
        if pivot_index == -1:
            logger.info(f"The system has an unbounded solution.\n\n")
            return None, None, None, None

        logger.info(f"The pivot chosed based in the Bland's rule is: simplex_matrix[%s][%s] = %s"
                    % (pivot_index, index_cost_negative,
                       simplex_matrix[pivot_index][index_cost_negative]))

        simplex_matrix = exceed_pivotation(simplex_matrix, pivot_index, index_cost_negative)
        labels_vars_from_base = update_labels_base_vars_after_pivoting(column_names, labels_vars_from_base,
                                                                       pivot_index, index_cost_negative)

        logger.info('The system after the pivoting step is: \n\n' +
                    str(pd.DataFrame(simplex_matrix,
                                     columns=column_names,
                                     index=labels_vars_from_base)) + '\n\n')

        if phase_one and simplex_matrix[-1][-1] == 0:
            return finish_simplex_step(simplex_matrix, column_names, labels_vars_from_base, z, z_free_term,
                                       search_alternative, phase_one)

        index_cost_negative = get_index_negative_cost(simplex_matrix)
        if index_cost_negative == -1:
            return finish_simplex_step(simplex_matrix, column_names, labels_vars_from_base, z, z_free_term,
                                       search_alternative, phase_one)


def run_simplex_on_instance(lp_system, labels_vars_from_base, z, z_free_term,
                            already_tableau=False, column_names=None, search_alternative=False, phase_one=False):
    original_z = z.copy()
    original_free_term = z_free_term

    if not already_tableau:
        simplex_tableau_as_matrix = get_simplex_tableau_as_matrix(lp_system, z, z_free_term)
        simplex_pd_df = convert_simplex_tableau_to_pd_df(simplex_tableau_as_matrix, labels_vars_from_base)
    else:
        simplex_tableau_as_matrix = lp_system
        simplex_pd_df = pd.DataFrame(lp_system,
                                     columns=column_names,
                                     index=labels_vars_from_base)

    logger.info('The simplex tableau is: \n\n' + str(simplex_pd_df) + '\n\n')

    if not already_tableau:
        labels_vars_from_base = get_labels_simplex_tableau(labels_vars_from_base)
        column_names = get_column_names_simplex_tableau(len(lp_system[0]), labels_vars_from_base)

    simplex_tableau_as_matrix, z, z_free_term = modify_z_if_vars_from_base_have_zero_cost(simplex_tableau_as_matrix,
                                                                                          labels_vars_from_base, column_names,
                                                                                          z, z_free_term)

    simplex_tableau_as_matrix, column_names, labels_vars_from_base, solution = simplex_algorithm(simplex_tableau_as_matrix,
                                                                                                  column_names,
                                                                                                  labels_vars_from_base,
                                                                                                  original_z, original_free_term,
                                                                                                  search_alternative,
                                                                                                  phase_one)
    return simplex_tableau_as_matrix, column_names, labels_vars_from_base, solution
