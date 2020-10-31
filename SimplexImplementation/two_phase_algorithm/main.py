import pandas as pd

from two_phase_algorithm.utils import *
from two_phase_algorithm.config import logger
from two_phase_algorithm.standard_form_conversion import *


def run_two_phase_on_instance(lp_system, z, z_free_term, optimization_type):
    if optimization_type == "max":
        z, z_free_term = from_max_to_min_conversion(z, z_free_term)
        optimization_type = "min"

    original_z = z.copy()

    logger.info("Started to prepare the system for the two phase algorithm. \n\n")

    lp_system, labels_vars_from_base = prepare_system_for_two_phase_algorithm(lp_system,
                                                                              initial_no_vars=len(lp_system[0]) - 2)


if __name__ == '__main__':

    logger.info("\n\n-------------------------   EXAMPLE 1 FROM THE SEMINAR   --------------------------------\n\n")
    run_two_phase_on_instance(lp_system=[[1, 1, 1, 'LT', 6],
                                         [-1, 1, 0, 'LT', -1],
                                         [-1, 0, 1, 'LT', -1]],
                              z=[2, -1, 2],
                              z_free_term=0,
                              optimization_type='max')

    logger.info("\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, a)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 1, 'GT', 6],
                                         [2, 3, 'LT', 4]],
                              z=[-1, 0],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, b)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[2, 1, 1, 'E', 4],
                                         [1, 1, 2, 'E', 2]],
                              z=[1, 1, 0],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, c)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 2, -1, 1, 'E', 0],
                                         [2, -2, 3, 3, 'E', 9],
                                         [1, -1, 2, -1, 'E', 6]],
                              z=[-3, 1, 3, -1],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, c)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 1, 'E', 2],
                                         [2, 2, 'E', 4]],
                              z=[1, 2],
                              z_free_term=0,
                              optimization_type='min')



