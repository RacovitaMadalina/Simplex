import pandas as pd

from two_phase_algorithm.config import logger
from two_phase_algorithm.simplex_algorithm import exceed_pivotation, update_labels_base_vars_after_pivoting
from two_phase_algorithm.z_conversion import *


def remove_artificial_variables_columns(simplex_tableaux, column_names):
    indexes_col_names_corresponding_to_artificial = [int(label.split('_')[1]) - 1
                                                     for label in column_names if 'y' in label]

    simplex_tableaux_cols_dropped = []
    for eq_index in range(len(simplex_tableaux)):
        simplex_tableaux_cols_dropped.append([])
        for var_index in range(len(simplex_tableaux[0])):
            if var_index not in indexes_col_names_corresponding_to_artificial:
                simplex_tableaux_cols_dropped[-1].append(simplex_tableaux[eq_index][var_index])

    return simplex_tableaux_cols_dropped


def pad_z_with_0_for_slack_excess_vars(simplex_tableaux, z):
    for i in range(len(z), len(simplex_tableaux[-1]) - 1):
        z.append(0)
    return z


def prepare_system_for_phase_two(simplex_tableaux, labels_vars_from_base, column_names, z, z_free_term):
    simplex_tableaux = remove_artificial_variables_columns(simplex_tableaux, column_names)

    z = pad_z_with_0_for_slack_excess_vars(simplex_tableaux, z)

    # replace z with the initial cost function
    simplex_tableaux = replace_z_in_simplex_tableau(simplex_tableaux, z, z_free_term)
    return simplex_tableaux, z, z_free_term, labels_vars_from_base
