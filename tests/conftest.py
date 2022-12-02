import os
from unittest.mock import Mock

from complex_opinion.core import Opinion_Model

import networkx as nx

import joblib

import numpy as np

import pytest


@pytest.fixture()
def seed():
    seed = np.random.randint(2 ** (4 * 7))
    # seed = 2 ** ( 4 * 3 ) - 1  # quiero que sea siempre la misma
    return seed


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
def mahdi_simulation():

    # abs_path_to_this_file = os.path.dirname(__file__)
    # rel_path = "Mahdi_data"
    # abs_file_path = os.path.join(abs_path_to_this_file, rel_path)

    path = "/home/nate/Devel/complex_opinion/data/Mahdi_data"
    with open(path, "rb") as mh:
        mahdi_simulation = joblib.load(mh)
        return np.array(mahdi_simulation)