from complex_opinion.core import OpinionModel

import numpy as np

import pytest


def test_zero_nodes(zero_nodes_graph):
    with pytest.raises(ValueError):
        OpinionModel(zero_nodes_graph)


def test_zero_edges(zero_edges_graph):
    with pytest.raises(ValueError):
        OpinionModel(zero_edges_graph)


def test_reproduce_mahdi_simulation_1(mahdi_simulation_1, small_world_society):
    number_of_initial_conditions = 1
    num_sim_per_in_cond = 1
    num_mc_steps = 10000

    h_field = 0.2
    temperature = 0.2
    p_1 = 1.0

    mc_seed = 2 ** (4 * 3) - 1
    initial_cond_seed = 12345

    t, m = small_world_society.opinion_dynamics(
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_mc_steps,
        h_field,
        temperature,
        p_1,
        mc_seed,
        initial_cond_seed,
    )

    assert np.allclose(m, mahdi_simulation_1)  # rtol=1e-05, atol=1e-08


def test_reproduce_mahdi_simulation_2(mahdi_simulation_2, small_world_society):
    number_of_initial_conditions = 50
    num_sim_per_in_cond = 1
    num_mc_steps = 10000

    h_field = 0.2
    temperature = 0.2
    p_1 = 1.0

    mc_seed = 2 ** (4 * 3) - 1
    initial_cond_seed = 12345

    t, m = small_world_society.opinion_dynamics(
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_mc_steps,
        h_field,
        temperature,
        p_1,
        mc_seed,
        initial_cond_seed,
    )

    assert np.allclose(m, mahdi_simulation_2)  # rtol=1e-05, atol=1e-08


# np.allclose documentation:
# https://numpy.org/doc/stable/reference/generated/numpy.allclose.html


@pytest.mark.slow
@pytest.mark.parametrize("number_of_initial_conditions", [1, 5])
@pytest.mark.parametrize("num_sim_per_in_cond", [1, 5])
@pytest.mark.parametrize("num_mc_steps", [10000])
def test_abs_mag_leq_one(
    number_of_initial_conditions,
    num_sim_per_in_cond,
    num_mc_steps,
    h_field,
    temperature,
    p_1,
    mc_seed,
    initial_cond_seed,
    small_world_society,
):
    t, m = small_world_society.opinion_dynamics(
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_mc_steps,
        h_field,
        temperature,
        p_1,
        mc_seed,
        initial_cond_seed,
    )
    for i in range(num_mc_steps):
        assert m[i] <= 1
        assert m[i] >= -1
