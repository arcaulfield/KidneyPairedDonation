import market as Market
from algorithms import hungarian_algorithm as HA
import networkx as nx
from config import ALGORITHM
from algorithms.LP.linear_program import solve_KEP
import algorithms.kidney_solver.kidney_digraph as kidney_digraph
import time

import algorithms.kidney_solver.kidney_ip as kidney_ip
import algorithms.kidney_solver.kidney_utils as kidney_utils
import algorithms.kidney_solver.kidney_ndds as kidney_nnds


class MaxMatching:
    """
    Finds maximum weight matching in a kidney exchange market, useing the hungarian algorithms
    The kidney exchange market is represented as a bipartite graph
    """

    def __init__(self, market, max_cycle_path_size=3):
        """
        :param market: a Market instance which is a kidney exchange market
        """
        self.bigraph = market
        self.cycle_lengths = None
        self.max_cycle_path_size=max_cycle_path_size

    def maximum_matching(self):
        if ALGORITHM == "HA":
            return self.HA_maximum_matching()
        elif ALGORITHM == "LP":
            return self.LP_maximum_matching()
        elif ALGORITHM == "FAST":
            return self.FAST_maximum_matching()

    def HA_maximum_matching(self):
        """
        finds matching using the hungarian algorithm
        :return: a set of all the edges in the matching
        """
        edges = set()
        participant_list = self.bigraph.participants.copy()
        new_graph = self.bigraph.graph.copy()
        for participant in self.bigraph.participants:
            if participant.donor and len(participant.neighbours) == 0:
                to_remove = None
                for (p1, p2) in new_graph.edges():
                    if p2 == participant:
                        to_remove = p1
                        participant_list.remove(p1)
                if to_remove is not None:
                    new_graph.remove_node(to_remove)
                if participant in new_graph.nodes():
                    new_graph.remove_node(participant)
                participant_list.remove(participant)
        if len(participant_list) == 0:
            return edges
        matrix = (nx.adjacency_matrix(new_graph)).todense().tolist()
        for n in range(len(matrix)):
            matrix[n] = [-100000 if x == 0 else x for x in matrix[n]]
        # give a score of 1 between pairs
        for n in range(int(len(matrix) / 2)):
            matrix[(n * 2) + 1][(n*2)] = 1
            matrix[(n * 2)][n * 2 + 1] = 1
        matching = HA.max_weight_matching(matrix)
        if matching[2] <= (len(self.bigraph.participants) / 2):
            return edges
        else:
            # identify the participants in the matching
            for p in matching[0].keys():
                participant1 = participant_list[p]
                participant2 = participant_list[matching[0][p]]
                if not (participant1.partner == participant2):
                    edge = (participant1, participant2)
                    edges.add(edge)
            return edges

    def LP_maximum_matching(self):
        """
        finds a matching using a linear program
        :return: a set of all the edges in the matching
        """
        G, pair_dict, weights, _ = self.bigraph.get_adj_list()
        #altruist_list = self.bigraph.get_alt_list()
        OPT, cpu_time, _, _, _, chains, cycles = solve_KEP(G, self.max_cycle_path_size, self.max_cycle_path_size, weights=weights)
        edges = set()
        cycle_path_lengths = ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
        for cycle in cycles:
            cur_cycle = True
            for i in range(len(cycle) - 1):
                pair1 = pair_dict[cycle[i]]
                pair2 = pair_dict[cycle[i+1]]
                edge1 = (pair1.partner, pair1)
                edge2 = (pair1, pair2.partner)
                edges.add(edge1)
                edges.add(edge2)
                if pair1.blood_type == 'X' or pair1.partner.blood_type == 'X':
                    cur_cycle = False
            pair1 = pair_dict[cycle[(len(cycle) - 1)]]
            pair2 = pair_dict[cycle[0]]
            edge1 = (pair1.partner, pair1)
            edge2 = (pair1, pair2.partner)
            edges.add(edge1)
            edges.add(edge2)
            if pair1.blood_type == 'X' or pair1.partner.blood_type == 'X':
                cur_cycle = False
            j = 0
            if not cur_cycle:
                j = 1
            if len(cycle) > 6:
                cycle_path_lengths[j][4] += 1
            else:
                cycle_path_lengths[j][len(cycle) - 2] += 1
        self.cycle_lengths = cycle_path_lengths
        return edges


    def FAST_maximum_matching(self):
        """
        finds a matching using a faster linear program
        :return: a set of all the edges in the matching
        """
        digraph_lines = list()
        G, pair_dict, weights, vertex_list = self.bigraph.get_adj_list()
        digraph_lines.append(str(len(G.keys())) + "\t" + str(len(weights)) + "\n")
        for key in G.keys():
            for val in G[key]:
                digraph_lines.append(str(key) + "\t" + str(val) + "\t" + str(weights[(key, val)]) + "\n")
        digraph_lines.append(str(-1) + "\t" + str(-1) + "\t" + str(-1) + "\n")
        d = kidney_digraph.read_digraph(digraph_lines, vertices=vertex_list)
        start_time = time.time()
        cfg = kidney_ip.OptConfig(d, [], self.max_cycle_path_size, self.max_cycle_path_size)
        opt_solution = solve_kep(cfg, formulation="picef", use_relabelled=False)
        time_taken = time.time() - start_time
        print(("ip_vars: {}".format(opt_solution.ip_model.numVars)))
        print(("ip_constrs: {}".format(opt_solution.ip_model.numConstrs)))
        print(("total_time: {}".format(time_taken)))
        print(("ip_solve_time: {}".format(opt_solution.ip_model.runtime)))
        print(("solver_status: {}".format(opt_solution.ip_model.status)))
        print(("total_score: {}".format(opt_solution.total_score)))
        cycles = opt_solution.display()
        edges = set()
        cycle_path_lengths = ([0, 0, 0, 0, 0], [0, 0, 0, 0, 0])
        for cycle in cycles:
            cur_cycle = True
            for i in range(len(cycle) - 1):
                pair1 = pair_dict[cycle[i]]
                pair2 = pair_dict[cycle[i + 1]]
                edge1 = (pair1.partner, pair1)
                edge2 = (pair1, pair2.partner)
                edges.add(edge1)
                edges.add(edge2)
                if pair1.blood_type == 'X' or pair1.partner.blood_type == 'X':
                    cur_cycle = False
            pair1 = pair_dict[cycle[(len(cycle) - 1)]]
            pair2 = pair_dict[cycle[0]]
            edge1 = (pair1.partner, pair1)
            edge2 = (pair1, pair2.partner)
            edges.add(edge1)
            edges.add(edge2)
            if pair1.blood_type == 'X' or pair1.partner.blood_type == 'X':
                cur_cycle = False
            j = 0
            if not cur_cycle:
                j = 1
            if len(cycle) > 6:
                cycle_path_lengths[j][4] += 1
            else:
                cycle_path_lengths[j][len(cycle) - 2] += 1
        self.cycle_lengths = cycle_path_lengths
        return edges


def solve_kep(cfg, formulation, use_relabelled=True):
    formulations = {
        "uef": ("Uncapped edge formulation", kidney_ip.optimise_uuef),
        "eef": ("EEF", kidney_ip.optimise_eef),
        "eef_full_red": ("EEF with full reduction by cycle generation", kidney_ip.optimise_eef_full_red),
        "hpief_prime": ("HPIEF'", kidney_ip.optimise_hpief_prime),
        "hpief_prime_full_red": (
        "HPIEF' with full reduction by cycle generation", kidney_ip.optimise_hpief_prime_full_red),
        "hpief_2prime": ("HPIEF''", kidney_ip.optimise_hpief_2prime),
        "hpief_2prime_full_red": (
        "HPIEF'' with full reduction by cycle generation", kidney_ip.optimise_hpief_2prime_full_red),
        "picef": ("PICEF", kidney_ip.optimise_picef),
        "cf": ("Cycle formulation",
               kidney_ip.optimise_ccf)
    }

    if formulation in formulations:
        formulation_name, formulation_fun = formulations[formulation]
        if use_relabelled:
            opt_result = kidney_ip.optimise_relabelled(formulation_fun, cfg)
        else:
            opt_result = formulation_fun(cfg)
        kidney_utils.check_validity(opt_result, cfg.digraph, cfg.ndds, cfg.max_cycle, cfg.max_chain)
        opt_result.formulation_name = formulation_name
        return opt_result
    else:
        raise ValueError("Unrecognised IP formulation name")
