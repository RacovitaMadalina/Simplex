import pandas as pd


def get_column_names_input_conversion(n, labels_vars_from_base):
    columns = []
    for col_no in range(n - 2):
        col_name = 'y_' + str(col_no + 1)
        if col_name in labels_vars_from_base:
            columns.append(col_name)
        else:
            columns.append(col_name.replace('y', 'x'))
    columns.append('Comparator')
    columns.append('RHS')
    return columns


def get_column_names_simplex_tableau(n, labels_vars_from_base):
    column_names = get_column_names_input_conversion(n, labels_vars_from_base)
    column_names.remove('Comparator')
    return column_names


def get_labels_simplex_tableau(labels_vars_from_base):
    return labels_vars_from_base + ['z']


def get_simplex_tableau_as_matrix(lp_system, cost_function, z_free_term):
    simplex_tableau = [equation[:-2] + [equation[-1]] for equation in lp_system]
    cost_function += [0] * (len(simplex_tableau[0]) - len(cost_function) - 1) + [z_free_term]
    simplex_tableau.append(cost_function)
    return simplex_tableau


def convert_simplex_tableau_to_pd_df(simplex_tableau_as_matrix, labels_vars_from_base):
    return pd.DataFrame(simplex_tableau_as_matrix,
                        columns=get_column_names_simplex_tableau(len(simplex_tableau_as_matrix[0]) + 1,
                                                                 labels_vars_from_base),
                        index=get_labels_simplex_tableau(labels_vars_from_base))


