import pandas as pd
from two_phase_algorithm.config import logger


def replace_z_in_simplex_tableau(simplex_tableaux, z, z_free_term):
    simplex_tableaux[-1][-1] = z_free_term
    for i in range(len(simplex_tableaux[-1]) - 1):
        simplex_tableaux[-1][i] = z[i]
    return simplex_tableaux


def replace_vars_not_zero_cost_within_z(simplex_tableaux, labels_vars_from_base, z, z_free_term,
                                        indexes_vars_should_be_replaced_in_z):
    index_equation = 0

    # for each var that has not zero reduced cost, we replace it in the cost function
    for label in labels_vars_from_base[:-1]:
        current_base_var_idx = int(label.split('_')[1]) - 1

        if current_base_var_idx in indexes_vars_should_be_replaced_in_z:
            # this means that from this equation we have to get x_i with z_i != 0
            z_free_term += (-1) * z[current_base_var_idx] * simplex_tableaux[index_equation][-1]

            for index_var_in_eq in range(len(simplex_tableaux[index_equation]) - 1):
                if index_var_in_eq != current_base_var_idx:
                    z[index_var_in_eq] -= z[current_base_var_idx] * simplex_tableaux[index_equation][index_var_in_eq]

        index_equation += 1

    # put 0 in z on the position occupied by each var from the base that has not zero reduced cost
    for index in indexes_vars_should_be_replaced_in_z:
        z[index] = 0

    return z, z_free_term


def modify_z_if_vars_from_base_have_zero_cost(simplex_tableaux, labels_vars_from_base, column_names, z, z_free_term):
    indexes_base_vars = [int(label.split('_')[1]) - 1 for label in labels_vars_from_base[:-1]]
    cost_line = simplex_tableaux[-1]

    indexes_vars_should_be_replaced_in_z = []
    for index in indexes_base_vars:
        if cost_line[index] != 0:
            indexes_vars_should_be_replaced_in_z.append(index)

    if len(indexes_vars_should_be_replaced_in_z) != 0:
        logger.info('Variables that have not zero reduced cost have to be replaced within the cost function.')

        z, z_free_term = replace_vars_not_zero_cost_within_z(simplex_tableaux, labels_vars_from_base, z, z_free_term,
                                                             indexes_vars_should_be_replaced_in_z)
        # replace z with the new z function
        simplex_tableaux = replace_z_in_simplex_tableau(simplex_tableaux, z, z_free_term)
        logger.info('Replaced successfully the vars. The tableau is now an optimal Simplex tableau. \n\n')

        logger.info('The system after replacing z is: \n\n' +
                    str(pd.DataFrame(simplex_tableaux,
                                     columns=column_names,
                                     index=labels_vars_from_base)) + '\n\n')

        return simplex_tableaux, z, z_free_term

    return simplex_tableaux, z, z_free_term