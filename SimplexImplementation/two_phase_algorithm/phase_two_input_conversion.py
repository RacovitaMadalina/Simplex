import pandas as pd


def remove_artificial_variables_columns(simplex_tableaux, column_names):
    indexes_col_names_corresponding_to_artificial = [int(label.split('_')[1]) for label in column_names if 'y' in label]

    simplex_tableaux_cols_dropped = []
    for eq_index in range(len(simplex_tableaux)):
        simplex_tableaux_cols_dropped.append([])
        for var_index in range(len(simplex_tableaux[0])):
            if var_index not in indexes_col_names_corresponding_to_artificial:
                simplex_tableaux_cols_dropped[-1].append(simplex_tableaux[eq_index][var_index])

    return simplex_tableaux_cols_dropped


def replace_z_with_initial_cost_function(simplex_tableaux, z, z_free_term):
    simplex_tableaux[-1][-1] = z_free_term
    for i in range(len(z)):
        simplex_tableaux[-1][i] = z[i]
    for i in range(len(z), len(simplex_tableaux[-1]) - 1):
        simplex_tableaux[-1][i] = 0
    return simplex_tableaux


def prepare_system_for_phase_two(simplex_tableaux, column_names, z, z_free_term):
    simplex_tableaux = remove_artificial_variables_columns(simplex_tableaux, column_names)
    simplex_tableaux = replace_z_with_initial_cost_function(simplex_tableaux, z, z_free_term)
    return simplex_tableaux
