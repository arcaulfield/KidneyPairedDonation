import market as Market
from algorithm import hungarian_algorithm as HA
import networkx as nx


class MaxMatching:
    """
    Finds maximum weight matching in a kidney exchange market, useing the hungarian algorithm
    The kidney exchange market is represented as a bipartite graph
    """

    def __init__(self, market):
        """
        :param market: a Market instance which is a kidney exchange market
        """
        self.bigraph = market

    def maximum_matching(self):
        """
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
            matrix[n] = [-1000 if x == 0 else x for x in matrix[n]]
        # give a score of 1 between pairs
        for n in range(int(len(matrix) / 2)):
            matrix[(n * 2) + 1][(n*2)] = 1
            matrix[(n * 2)][n * 2 + 1] = 1
        matching = HA.max_weight_matching(matrix)
        # WHY DO WE DO THIS???
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

    def filter_matches(self, matches):
        """
        filters out matches that don't include hard-to-match pairs
        :param matches: a set of matches that only include hard-to-match pairs
        :return DOESNT WORK
        """
        pair = None
        found_incompatible_pair = False
        cycle = set()
        for (p1, p2) in matches:
            if pair is None:
                pair = p1
            cycle.add((p1, p2))
            if p1.compatible == 0:
                found_incompatible_pair = True
            if p2 == pair:
                pair = None
                if not found_incompatible_pair:
                    matches = matches - cycle
                cycle = set()
        return matches

