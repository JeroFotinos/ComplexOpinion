from unittest.mock import Mock

from complex_opinion.core import OpinionModel

import joblib

import networkx as nx


import numpy as np

import pytest


@pytest.fixture()
def mc_seed():
    mc_seed = np.random.randint(2 ** (4 * 7))
    return mc_seed


@pytest.fixture()
def initial_cond_seed():
    initial_cond_seed = np.random.randint(2 ** (4 * 7))
    return initial_cond_seed


@pytest.fixture()
def h_field():
    h_field = 0.2
    return h_field


@pytest.fixture()
def temperature():
    temperature = 0.2
    return temperature


@pytest.fixture()
def p_1():
    p_1 = 1.0
    return p_1


@pytest.fixture()
def zero_nodes_graph():
    zero_nodes_graph = Mock()
    zero_nodes_graph.number_of_nodes.return_value = 0
    zero_nodes_graph.number_of_edges.return_value = 1
    return zero_nodes_graph


@pytest.fixture()
def zero_edges_graph():
    zero_edges_graph = Mock()
    zero_edges_graph.number_of_nodes.return_value = 1
    zero_edges_graph.number_of_edges.return_value = 0
    return zero_edges_graph


@pytest.fixture()
def small_world_society():
    number_of_nodes = 500
    k = 5
    p = 0.01
    graph = nx.watts_strogatz_graph(number_of_nodes, k, p, seed=896803)
    small_world_society = OpinionModel(graph)
    return small_world_society


@pytest.fixture()
def mahdi_simulation_1():
    """
    Provides the equivalent to m_vs_mcs__avg
    of Mahdi's code (with the limitation of
    not being able to average over the same initial condition).
    The parameters (in my notation) used in Mahdi's code to
    generate this example were:

    number_of_initial_conditions = 1
    num_sim_per_in_cond = 1
    num_mc_steps = 10000


    h_field = 0.2
    temperature = 0.2
    p_1 = 1.0

    mc_seed = 2 ** ( 4 * 3 ) - 1
    initial_cond_seed = 12345

    number_of_nodes = 500
    k = 5
    p = 0.01
    graph = nx.watts_strogatz_graph( number_of_nodes , k , p , seed = 896803 )
    """

    path = "/home/nate/Devel/2complex_opinion/data/Mahdi_data_1"
    with open(path, "rb") as mh:
        mahdi_simulation = joblib.load(mh)
        return np.array(mahdi_simulation)


@pytest.fixture()
def mahdi_simulation_2():
    """
    Provides the equivalent to m_vs_mcs__avg
    of Mahdi's code (with the limitation of
    not being able to average over the same initial condition).
    The parameters (in my notation) used in Mahdi's code to
    generate this example were:

    number_of_initial_conditions = 50
    num_sim_per_in_cond = 1
    num_mc_steps = 10000


    h_field = 0.2
    temperature = 0.2
    p_1 = 1.0

    mc_seed = 2 ** ( 4 * 3 ) - 1
    initial_cond_seed = 12345

    number_of_nodes = 500
    k = 5
    p = 0.01
    graph = nx.watts_strogatz_graph( number_of_nodes , k , p , seed = 896803 )
    """

    path = "/home/nate/Devel/2complex_opinion/data/Mahdi_data_2"
    with open(path, "rb") as mh:
        mahdi_simulation = joblib.load(mh)
        return np.array(mahdi_simulation)
