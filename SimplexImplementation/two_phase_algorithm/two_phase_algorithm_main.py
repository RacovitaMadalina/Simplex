from two_phase_algorithm.phase_one_input_conversion import *
from two_phase_algorithm.phase_two_input_conversion import *
from two_phase_algorithm.simplex_algorithm import *


def run_two_phase_on_instance(lp_system, z, z_free_term, optimization_type):
    if optimization_type == "max":
        z, z_free_term = from_max_to_min_conversion(z, z_free_term)
        optimization_type = "min"

    original_z = z.copy()

    logger.info("Started to prepare the system for the two phase algorithm. \n\n")

    lp_system, labels_vars_from_base = prepare_system_for_phase_one(lp_system,
                                                                    initial_no_vars=len(lp_system[0]) - 2)

    z_phase_1 = retrieve_new_z_as_sum_of_artificial_variables(lp_system, labels_vars_from_base)

    if z_phase_1 != None:
        logger.info("Since we have artificial variables added, the new "
                    "cost function to be optimized is the following: \n" +
                    "z = " + str(z_phase_1) + '\n\n')

        logger.info("\n\n-------------------------   PHASE 1   --------------------------------\n\n")
        simplex_matrix, column_names, labels_vars_from_base, solution = run_simplex_on_instance(
            lp_system, labels_vars_from_base, z=z_phase_1[:-1], z_free_term=z_phase_1[-1], phase_one=True)

        if solution != None:
            simplex_tableau_phase_two, z, z_free_term, labels_vars_from_base = prepare_system_for_phase_two(
                simplex_matrix, labels_vars_from_base, column_names, z, z_free_term)

            column_names = [col_name for col_name in column_names if 'y_' not in col_name]

            logger.info('The system for the second phase after removing the artificial variables \n'
                        'and after replacing the initial cost function is: \n' +
                        str(pd.DataFrame(simplex_tableau_phase_two,
                                         columns=column_names,
                                         index=labels_vars_from_base)) + '\n\n')
            simplex_matrix, column_names, labels_vars_from_base, solution = run_simplex_on_instance(
                simplex_tableau_phase_two, labels_vars_from_base, z=z, z_free_term=z_free_term,
                already_tableau=True, column_names=column_names, search_alternative=True)
    else:
        logger.info("Phase one can't be executed since no artificial variables were added.")
        simplex_matrix, column_names, labels_vars_from_base, solution = run_simplex_on_instance(
            lp_system, labels_vars_from_base, z=z, z_free_term=z_free_term, phase_one=False)


if __name__ == '__main__':
    run_two_phase_on_instance(lp_system=[[1, 1, "LT", 2]], z=[1, 1], z_free_term=0, optimization_type="max")

    run_two_phase_on_instance(lp_system=[[1.0, -2.0, 2.0, 1, 0, 0, 'E', 6.0], [1.0, 1.0, 2.0, 0, 1, 0, 'E', 8.0],
                                         [0, 1, 0, -1, 0, 1, 'E', 0]], z=[1.0, -1.0, 2.0, 0, 0, 0], z_free_term=0,
                              optimization_type="min")

    logger.info("\n\n-------------------------   EXAMPLE 1 FROM THE SEMINAR   --------------------------------\n\n")
    run_two_phase_on_instance(lp_system=[[1, 1, 1, 'LT', 6],
                                         [-1, 1, 0, 'LT', -1],
                                         [-1, 0, 1, 'LT', -1]],
                              z=[2, -1, 2],
                              z_free_term=0,
                              optimization_type='max')

    logger.info("\n\n\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, a)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 1, 'GT', 6],
                                         [2, 3, 'LT', 4]],
                              z=[-1, 0],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, b)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[2, 1, 1, 'E', 4],
                                         [1, 1, 2, 'E', 2]],
                              z=[1, 1, 0],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, c)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 2, -1, 1, 'E', 0],
                                         [2, -2, 3, 3, 'E', 9],
                                         [1, -1, 2, -1, 'E', 6]],
                              z=[-3, 1, 3, -1],
                              z_free_term=0,
                              optimization_type='min')

    logger.info("\n\n\n\n--------------------   EXAMPLE 2 / HOMEWORK 2.1, ex.2, c)   -----------------------\n\n")

    run_two_phase_on_instance(lp_system=[[1, 1, 'E', 2],
                                         [2, 2, 'E', 4]],
                              z=[1, 2],
                              z_free_term=0,
                              optimization_type='min')

