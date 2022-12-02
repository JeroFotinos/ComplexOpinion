from complex_opinion.core import Opinion_Model

import networkx as nx

import numpy as np

import pytest


def test_zero_nodes(zero_nodes_graph):
    with pytest.raises(ValueError):
        m = Opinion_Model(zero_nodes_graph)


def test_zero_edges(zero_edges_graph):
    with pytest.raises(ValueError):
        m = Opinion_Model(zero_edges_graph)


@pytest.mark.xfail
def test_reproduce_mahdi_simulation(mahdi_simulation, small_world_society):
    number_of_initial_conditions = 10
    num_sim_per_in_cond = 1
    num_MC_steps = 10000

    H = 0.2
    T = 0.2
    p_1 = 1.0

    # seed = np.random.randint( 2 ** ( 4 * 7 ))  # original Mahdi
    seed = 2 ** ( 4 * 3 ) - 1  # quiero que sea siempre la misma

    t, M = small_world_society.opinion_dynamics(
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_MC_steps,
        H,
        T,
        p_1,
        seed,
    )

    assert np.allclose(M, mahdi_simulation, rtol=0.01, atol=0.1)


# np.isclose documentation:
# https://numpy.org/doc/stable/reference/generated/numpy.isclose.html


# @pytest.mark.skip(reason="Passes but slow")
@pytest.mark.slow
@pytest.mark.parametrize("number_of_initial_conditions", [1, 5])
@pytest.mark.parametrize("num_sim_per_in_cond", [1, 5])
@pytest.mark.parametrize("num_MC_steps", [10000])
def test_abs_mag_leq_one(
    number_of_initial_conditions,
    num_sim_per_in_cond,
    num_MC_steps,
    H,
    T,
    p_1,
    seed,
    small_world_society,
):
    t, M = small_world_society.opinion_dynamics(
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_MC_steps,
        H,
        T,
        p_1,
        seed,
    )
    for i in range(num_MC_steps):
        assert M[i] <= 1
        assert M[i] >= -1