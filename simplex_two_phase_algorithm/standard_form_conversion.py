from simplex_two_phase_algorithm.config import logger


def add_slack_excess_column_to_equations(lp_system):
    new_matrix = []
    for equation in lp_system:
        equation.append(equation[-1])
        equation[-2] = equation[-3]
        equation[-3] = 0
        new_matrix.append(equation)
    return new_matrix

def convert_system_to_standard_form(lp_system, initial_no_vars):
    logger.info("Starting converting the system to its standard form.")

    # add columns corresponding to the slack variables
    # the slack variables are going to consist the base of the system
    for equation in lp_system:
        if 'LT' in equation or 'GT' in equation:
            lp_system = add_slack_excess_column_to_equations(lp_system)
    
    logger.info('Added columns for the slack / excess variables.')

    # convert each equation to standard form
    new_matrix = []
    slack_excess_var_index_start = initial_no_vars
    labels_base = []

    for equation in lp_system:
        if 'LT' in equation:
            new_matrix.append(convert_equation_to_standard_form(equation, slack_excess_var_index_start))
            labels_base.append(slack_excess_var_index_start)
            slack_excess_var_index_start += 1 # increase the slack var index

    logger.info('Coverted the equations to their standard form.')
    return lp_system, labels_base


def convert_equation_to_standard_form(equation, slack_excess_var_index_start):
    if equation[-2] == 'LT':
        equation[slack_excess_var_index_start] = 1
        equation[-2] = 'E'
        return equation
    if equation[-2] == 'E':
        return equation
    if equation[-2] == 'GT':
        equation[slack_excess_var_index_start] = -1
        equation[-2] = 'E'
        return equation
