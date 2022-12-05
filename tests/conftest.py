import os
from unittest.mock import Mock

from complex_opinion.core import Opinion_Model

import networkx as nx

import joblib

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
def H():
    H = 0.2
    return H


@pytest.fixture()
def T():
    T = 0.2
    return T


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
    N = 500
    k = 5
    p = 0.01
    G = nx.watts_strogatz_graph(N, k, p, seed=896803)  # 896803
    small_world_society = Opinion_Model(G)
    return small_world_society


# @pytest.fixture()
# def mahdi_simulation():
#     file_name = "Mahdi_data"
#     mahdi_simulation = joblib.load(file_name)
#     return np.array(mahdi_simulation)


@pytest.fixture()
def mahdi_simulation_1():
    """
    Provides the equivalent to M_vs_mcs__avg
    of Mahdi's code (with the limitation of 
    not being able to average over the same initial condition).
    The parameters (in my notation) used in Mahdi's code to
    generate this example were:
    
    number_of_initial_conditions = 1
    num_sim_per_in_cond = 1
    num_MC_steps = 10000


    H = 0.2
    T = 0.2
    p_1 = 1.0

    mc_seed = 2 ** ( 4 * 3 ) - 1
    initial_cond_seed = 12345

    N = 500
    k = 5
    p = 0.01
    G = nx.watts_strogatz_graph( N , k , p , seed = 896803 )
    """

    path = "/home/nate/Devel/2complex_opinion/data/Mahdi_data_1"
    with open(path, "rb") as mh:
        mahdi_simulation = joblib.load(mh)
        return np.array(mahdi_simulation)

@pytest.fixture()
def mahdi_simulation_2():
    """
    Provides the equivalent to M_vs_mcs__avg
    of Mahdi's code (with the limitation of 
    not being able to average over the same initial condition).
    The parameters (in my notation) used in Mahdi's code to
    generate this example were:
    
    number_of_initial_conditions = 50
    num_sim_per_in_cond = 1
    num_MC_steps = 10000


    H = 0.2
    T = 0.2
    p_1 = 1.0

    mc_seed = 2 ** ( 4 * 3 ) - 1
    initial_cond_seed = 12345

    N = 500
    k = 5
    p = 0.01
    G = nx.watts_strogatz_graph( N , k , p , seed = 896803 )
    """

    path = "/home/nate/Devel/2complex_opinion/data/Mahdi_data_2"
    with open(path, "rb") as mh:
        mahdi_simulation = joblib.load(mh)
        return np.array(mahdi_simulation)
