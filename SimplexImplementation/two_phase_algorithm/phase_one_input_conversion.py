from two_phase_algorithm.config import logger
from two_phase_algorithm.utils import *


def add_slack_excess_column_to_equations(lp_system):
    new_matrix = []
    for equation in lp_system:
        equation.append(equation[-1])
        equation[-2] = equation[-3]
        equation[-3] = 0
        new_matrix.append(equation)
    return new_matrix


def from_max_to_min_conversion(z, z_free_term):
    return [(-1) * cost for cost in z], (-1) * z_free_term


def reverse_if_rhs_negative(lp_system):
    for i in range(len(lp_system)):
        if lp_system[i][-1] < 0:
            lp_system[i] = [(-1) * term for term in lp_system[i][:-2]] + ['E'] + [(-1) * lp_system[i][-1]]
    return lp_system


def convert_system_to_standard_form(lp_system, initial_no_vars):
    logger.info("Starting converting the system to its standard form.")

    # add columns corresponding to the slack variables
    # the slack variables are going to consist the base of the system
    for equation in lp_system:
        if 'LT' in equation or 'GT' in equation:
            lp_system = add_slack_excess_column_to_equations(lp_system)
    
    logger.info('Added columns for the slack / excess variables.')

    # convert each equation to standard form
    slack_excess_var_index_start = initial_no_vars
    labels_base = []

    for i in range(len(lp_system)):
        if 'LT' in lp_system[i] or 'GT' in lp_system[i]:
            if 'LT' in lp_system[i]:
                labels_base.append(slack_excess_var_index_start + 1)

            lp_system[i] = add_additional_variable(lp_system[i], slack_excess_var_index_start)
            slack_excess_var_index_start += 1  # increase the slack/excess var index

    lp_system = reverse_if_rhs_negative(lp_system)

    logger.info('Coverted the equations to their standard form.\n\n')
    return lp_system, labels_base


def add_artificial_variables_to_system(lp_system, initial_no_vars):
    no_of_eq = len(lp_system)
    transpose = [[lp_system[j][i] for j in range(len(lp_system))] for i in range(len(lp_system[0]))]

    artifical_var_index_start = len(lp_system[0]) - 2
    labels_base = []
    index_col = 0

    for column in transpose[-len(lp_system[0])-2: -2]:
        if column.count(0) == len(column) - 1 and column.count(1) == 1:
            labels_base.append('x_' + str(index_col + 1))
        index_col += 1

    if len(labels_base) < no_of_eq:  # this means we need to add some artificial variables:
        # if we sum the columns corresponding to the already existent variables we are going to see which columns
        # from the identity matrix are missing
        summed_var_base_columns = [0 for i in range(len(lp_system))]
        index_cols_base = [int(label.split('_')[1]) - 1 for label in labels_base]
        for index in index_cols_base:
            for i in range(len(summed_var_base_columns)):
                summed_var_base_columns[i] += transpose[index][i]
        print(summed_var_base_columns)

        # for the indexes which in summed_var_base_columns are 0 we need to add artificial variable to form a complete
        # identity matrix
        for index_eq in range(len(summed_var_base_columns)):
            if summed_var_base_columns[index_eq] == 0:
                lp_system = add_slack_excess_column_to_equations(lp_system)
                lp_system[index_eq] = add_additional_variable(lp_system[index_eq], artifical_var_index_start, artificial=True)
                labels_base.append('y_' + str(artifical_var_index_start + 1))
                artifical_var_index_start += 1
            if len(labels_base) == no_of_eq:
                break

    return lp_system, labels_base


def add_additional_variable(equation, slack_excess_var_index_start, artificial=False):

    if equation[-2] == 'LT':
        equation[slack_excess_var_index_start] = 1
        equation[-2] = 'E'
        return equation

    if equation[-2] == 'E':
        if artificial:
            equation[slack_excess_var_index_start] = 1
        return equation

    if equation[-2] == 'GT':
        equation[slack_excess_var_index_start] = -1
        equation[-2] = 'E'
        return equation


def prepare_system_for_phase_one(lp_system, initial_no_vars):
    lp_system, labels_vars_from_base = convert_system_to_standard_form(lp_system, initial_no_vars)
    lp_system, labels_vars_from_base = add_artificial_variables_to_system(lp_system, initial_no_vars)

    logger.info('The system after converting to standard form and after adding the artificial variables is: \n\n' +
                str(pd.DataFrame(lp_system,
                                 columns=get_column_names_input_conversion(len(lp_system[0]), labels_vars_from_base),
                                 index=labels_vars_from_base)) + '\n\n')

    return lp_system, labels_vars_from_base


def get_number_of_artificial_variables(labels_vars_from_base):
    return sum([1 for label in labels_vars_from_base if 'y' in label])


def retrieve_new_z_as_sum_of_artificial_variables(lp_system, labels_vars_from_base):
    no_of_artificial_vars = get_number_of_artificial_variables(labels_vars_from_base)
    if no_of_artificial_vars == 0:
        return None

    # initialize the new z
    z = [0] * (len(lp_system[0]) - 2 - no_of_artificial_vars)
    z += [0]  # z - free term

    for index_eq in range(len(labels_vars_from_base)):
        if 'y_' in labels_vars_from_base[index_eq]:  # meaning that the current label is an artificial variable
            index_artificial = labels_vars_from_base[index_eq].split('_')[1]

            z[-1] -= lp_system[index_eq][-1]
            for index_term in range(len(lp_system[index_eq][:- 2 - no_of_artificial_vars])):
                if index_term != index_artificial:
                    z[index_term] -= lp_system[index_eq][index_term]
    return z