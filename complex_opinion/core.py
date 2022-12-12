"""Core module of complex_opinion package.

Contains the OpinionModel class and a variable for the fpb module
of f90_opinion.f90.
"""

# import f90opinion as fpb
from complex_opinion import f90opinion as fpb

# esta línea reemplaza a la anterior, porque si no,
# al hacer los tests, importamos core pero este
# trata de importar f90opinion y no puede porque no está en la carpeta tests
import numpy as np

fpb = fpb.fpb
# variable fpb = en el import fpb buscá el módulo fpb
# me convendría tener un módulo diferente por objeto? i.e.,
# ¿conviene que fbp sea un atributo más de los objetos de clase OpinionModel?
# ¿Cómo me conviene implementar eso? Lo que me da cosa es que fpb guarda estado


class OpinionModel:
    """Simulations of opinion dynamics on flexible topologies.

    The OpinionModel class allows to simulate different opinion dynamics
    (such as the voter's model) by wrapping a generic Networkx graph.
    It uses a Montecarlo method taking into account the neighbours of a
    given node.

    Attributes
    ----------
    topology : networkx.Graph
        Graph to be used as the topology.

    Methods
    -------
    opinion_dynamics
        Implements the voter's model dynamics taking into account which
        nodes are neighbours.

    """

    def __init__(self, topology):
        """Constructor.

        It recives a topology as attribute, checks that it has at least
        one node and one edge, calculates arrays that represent the graph
        and store them as attributes.

        Parameters
        ----------
        topology : networkx.Graph
            Graph to be used as the topology. Must have at least one node
            and one edge.

        Attributes
        ----------
        sorted_nodes : list
            A list of all nodes in ascending order.
        de_begins : list of int
            Cumulative degrees. A list beginning with 1, where the next
            item is obtained by adding the degree of the nodes in
            sorted_nodes, in order. Used to select a neighbour of a given node.
        de_sources : list
            List where all of the node numbers are listed a number of times
            equal to their degree.
        de_targets : list
            list of node numbers such that the k-th element of de_targets is
            a neighbor of de_sources. the set of all tuples
            (self.de_sources[k], self.de_targets[k]) is the set of edges.

        Raises
        ------
        ValueError
            If topology is not a graph or if it does not have at least
            one node and one edge.
        """
        self.topology = topology

        if not self.topology.number_of_nodes() > 0:
            raise ValueError("Number of nodes must be a positive integer")

        if not self.topology.number_of_edges() > 0:
            raise ValueError("Number of edges must be a positive integer")

        # All of this should probably be private attributes

        self.sorted_nodes = sorted(topology.nodes())
        self.enumerated_nodes = {n: i for i, n in enumerate(self.sorted_nodes)}

        self.de_begins = [1]
        # cumulative degrees (necessary? yes)
        self.de_sources = []
        # list where all of the node numbers are listed a
        # number of times equal to their degree
        self.de_targets = []
        # list of node numbers such that the k-th element of
        # self.de_targets is a neighbor of self.de_sources

        # Basically, the set of all tuples
        # (self.de_sources[k], self.de_targets[k])
        # is the set of edges

        for v in self.sorted_nodes:
            i = self.enumerated_nodes[v]
            self.de_begins.append(topology.degree(v) + self.de_begins[-1])
            for u in sorted(topology.neighbors(v)):
                j = self.enumerated_nodes[u]
                self.de_sources.append(
                    i + 1
                )  # The "+ 1" since i ranges from 0.
                self.de_targets.append(
                    j + 1
                )  # The "+ 1" since j ranges from 0.
        self.de_begins = np.array(self.de_begins, dtype=np.int32)
        self.de_sources = np.array(self.de_sources, dtype=np.int32)
        self.de_targets = np.array(self.de_targets, dtype=np.int32)

    def opinion_dynamics(
        self,
        number_of_initial_conditions,
        num_sim_per_in_cond,
        num_mc_steps,
        h_field,
        temperature,
        p_1,
        mc_seed,
        initial_cond_seed,
    ):
        """Simulation of Voter's Model on a complex network.

        It simulates the opinion dynamics of the voter's model a given number
        of times, for a specified number of initial conditions and returns the
        average evolution. The simulation uses a Montecarlo method with a
        specified number of steps. All seeds can be set.

        Parameters
        ----------
        number_of_initial_conditions : int
            Number of initial conditions for the system to be simulated a
            specified number of times and then averaged.
        num_sim_per_in_cond : int
            Number of simulations to average for the same initial condition.
        num_mc_steps : int
            Number of Montecarlo steps for every simulation.
        h_field : float
            H field module or intensity of the propaganda.
        temperature : float
            Social temperature. It increases the probability of a node
            randomly changing its state.
        p_1 : float
            Contagion probability.
        mc_seed : int
            Montecarlo seed. It is used as seed for the mzran RNG used in
            the simulations.
        initial_cond_seed : int
            Seed for the numpy RNG used to initialize the states of the system.

        Returns
        -------
        mcs : list of int
            Numpy array with the number of element as element. This is to
            be used as domain for the average magnetization or opinion.
        m_vs_mcs__avg : list of float
            Numpy array with the average magnetization or opinion of all
            simulations (of every initial condition) at each step.
        """
        # ---------- To be added to docstring ----------

        # Notes
        # -----
        # See [1] for more on the voter's model.

        # References
        # ----------
        # .. [1] Paper about the voter's model.

        # ----------------------------------------------

        ic_rng = np.random.default_rng(initial_cond_seed)
        # RNG for generating the initial conditions

        mcs = np.zeros(num_mc_steps)
        # Montecarlo steps (time)
        m_vs_mcs__avg = np.zeros(num_mc_steps)
        # average magnetization evolution over initial conditions
        m_vs_mcs_avg_in_cond = np.zeros(num_mc_steps)
        # average magnetization evolution over simulations from the
        # same initial condition

        fpb.de_begins = self.de_begins
        fpb.de_sources = self.de_sources
        fpb.de_targets = self.de_targets

        fpb.init(mc_seed)

        number_of_nodes = self.topology.number_of_nodes()
        # M = self.topology.number_of_edges()

        fpb.set_parameters_opinion_dynamics(h_field, temperature, p_1)

        # loop sobre distintas condiciones iniciales
        for initial_condition in range(number_of_initial_conditions):

            # we initialize the states
            # (the seed was set when instanciating ic_rng)
            in_cond = ic_rng.integers(2, size=number_of_nodes)

            # loop sobre misma condición inicial, pero
            # distintas evoluciones monte carlo

            # import ipdb; ipdb.set_trace()

            m_vs_mcs_avg_in_cond = np.zeros(num_mc_steps)

            for simulation in range(num_sim_per_in_cond):
                fpb.states = in_cond
                m_vs_mcs_simulation = fpb.opinion_dynamics(num_mc_steps)
                for i in range(num_mc_steps):
                    m_vs_mcs_avg_in_cond[i] += m_vs_mcs_simulation[i]

            for i in range(num_mc_steps):
                m_vs_mcs_avg_in_cond[i] = (
                    m_vs_mcs_avg_in_cond[i] / num_sim_per_in_cond
                )

            for i in range(num_mc_steps):
                m_vs_mcs__avg[i] += m_vs_mcs_avg_in_cond[i]
        # Divide cada elemento por el número de simulaciones para normalizar
        for i in range(num_mc_steps):
            m_vs_mcs__avg[i] = m_vs_mcs__avg[i] / number_of_initial_conditions

        # genera un array con los pasos que sirva como dominio para el plot
        for i in range(num_mc_steps):
            mcs[i] = i

        return mcs, m_vs_mcs__avg
