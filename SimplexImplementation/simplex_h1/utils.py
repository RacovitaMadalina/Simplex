import pandas as pd


def get_column_names_standard_form(n):
    columns = ['x_' + str(eq_no + 1) for eq_no in range(n-2)]
    columns.append('Comparator')
    columns.append('RHS')
    return columns


def get_column_names_simplex_tableau(n):
    columns = ['x_' + str(eq_no + 1) for eq_no in range(n-1)]
    columns.append('RHS')
    return columns


def get_labels_base_vars_by_index(index_base_vars):
    return ['x_' + str(index + 1) for index in index_base_vars] + ['z']


def get_simplex_tableau_as_matrix(lp_system, cost_function, z_free_term):
    simplex_tableau = [equation[:-2] + [equation[-1]] for equation in lp_system]
    cost_function += [0] * (len(simplex_tableau[0]) - len(cost_function) - 1) + [z_free_term]
    simplex_tableau.append(cost_function)
    return simplex_tableau


def convert_simplex_tableau_to_pd_df(simplex_tableau_as_matrix, index_vars_from_base):
    return pd.DataFrame(simplex_tableau_as_matrix,
                        columns=get_column_names_simplex_tableau(len(simplex_tableau_as_matrix[0])),
                        index=get_labels_base_vars_by_index(index_vars_from_base))


