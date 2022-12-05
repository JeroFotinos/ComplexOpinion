# import f90opinion as fpb
from complex_opinion import f90opinion as fpb  # esta línea reemplaza a la

# anterior porque si no al hacer los tests, importamos core pero este
# trata de importar f90opinion y no puede porque no está en la carpeta tests
import numpy as np

# podría heredar de networkx
# class Opinion_Model(nx.classes.graph.Graph)

# ¿cómo le paso los métodos y atributos del grafo
# al modelo de opinión?
# creo que lo más fácil es heredar, aunque no me gusta
# porque habría que inicializar especificando el grafo
# es más cómodo instanciar con un grafo ya hecho.
# Debo poder decirle "si no encontrás lo que te
# pido, buscalo en topology"

# variable fpb = en el import fpb buscá el módulo fpb

fpb = fpb.fpb
# me convendría tener un módulo diferente por objeto? i.e.,
# ¿conviene que fbp sea un atributo más de los objetos de clase Opinion_Model?
# ¿Cómo me conviene implementar eso?


class Opinion_Model:
    def __init__(self, topology):
        self.topology = topology

        if not self.topology.number_of_nodes() > 0:
            raise ValueError("Number of nodes must be a positive integer")

        if not self.topology.number_of_edges() > 0:
            raise ValueError("Number of edges must be a positive integer")

        self.sorted_nodes = sorted(topology.nodes())
        self.enumerated_nodes = {n: i for i, n in enumerate(self.sorted_nodes)}

        self.de_begins = [1]
        # cumulative degrees (necessary?)
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
        num_MC_steps,
        H,
        T,
        p_1,
        mc_seed,
        initial_cond_seed,
    ):

        ic_rng = np.random.default_rng(initial_cond_seed)
        # RNG for generating the initial conditions

        mcs = np.zeros(num_MC_steps)
        # Montecarlo steps (time)
        M_vs_mcs__avg = np.zeros(num_MC_steps)
        # average magnetization evolution over initial conditions
        M_vs_mcs_avg_in_cond = np.zeros(num_MC_steps)
        # average magnetization evolution over simulations from the
        # same initial condition

        fpb.de_begins = self.de_begins
        fpb.de_sources = self.de_sources
        fpb.de_targets = self.de_targets

        fpb.init(mc_seed)

        N = self.topology.number_of_nodes()
        # M = self.topology.number_of_edges()

        fpb.set_parameters_opinion_dynamics(H, T, p_1)

        # loop sobre distintas condiciones iniciales
        for initial_condition in range(number_of_initial_conditions):

            # we initialize the states
            # (the seed was set when instanciating ic_rng)
            in_cond = ic_rng.integers(2, size=N)

            # loop sobre misma condición inicial, pero
            # distintas evoluciones monte carlo

            # import ipdb; ipdb.set_trace()

            M_vs_mcs_avg_in_cond = np.zeros(num_MC_steps)

            for simulation in range(num_sim_per_in_cond):
                fpb.states = in_cond
                M_vs_mcs_simulation = fpb.opinion_dynamics(num_MC_steps)
                for i in range(num_MC_steps):
                    M_vs_mcs_avg_in_cond[i] += M_vs_mcs_simulation[i]

            for i in range(num_MC_steps):
                M_vs_mcs_avg_in_cond[i] = (
                    M_vs_mcs_avg_in_cond[i] / num_sim_per_in_cond
                )

            for i in range(num_MC_steps):
                M_vs_mcs__avg[i] += M_vs_mcs_avg_in_cond[i]
        # Divide cada elemento por el número de simulaciones para normalizar
        for i in range(num_MC_steps):
            M_vs_mcs__avg[i] = M_vs_mcs__avg[i] / number_of_initial_conditions

        # genera un array con los pasos que sirva como dominio para el plot
        for i in range(num_MC_steps):
            mcs[i] = i

        return mcs, M_vs_mcs__avg
