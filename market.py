import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from config import PERIOD_LENGTH
import algorithm.max_matching as mm
import market_metrics as met


class Market:
    """
    A kidney paired donation market represented as a bipartite graph
    Participants are the nodes of the graph and edges represent potential kidney exchanges
    Attributes
    ----------
    participants: list<participant>
        a list of all the participants in the market
    graph: Digraph
        a networkx directed graph
    """

    def __init__(self, pairs, num_altruists):
        self.graph = nx.DiGraph()
        self.participants = list()
        self.metrics = met.Metrics(num_altruists=num_altruists)
        for (recipient, donor) in pairs:
            self.add_pair((recipient, donor))

    def add_participant(self, participant):
        """
        adds a participant to the market
        :param participant: a participant to add to the market
        """
        if not (participant in list(self.graph.nodes())):
            self.add_node_to_graph(participant)
        if participant.donor:
            for p in self.participants:
                if p.recipient and participant.compatible(p) and (not participant.partner == p):
                    participant.add_neighbour(p)
                    # weight is determined by the recipient when determining who to match
                    self.graph.add_weighted_edges_from([(participant, p, p.weight)])
        else:
            for p in self.participants:
                if p.donor and participant.compatible(p) and (not participant.partner == p):
                    p.add_neighbour(participant)
                    # weight is determined by the recipient when determining who to match
                    self.graph.add_weighted_edges_from([(p, participant, participant.weight)])

    def add_node_to_graph(self, participant):
        """
        adds a participant to the networkx bipartite graph
        :param participant: participant to add to the graph
        """
        if participant.donor:
            self.graph.add_nodes_from([participant], bipartite=1)
        elif participant.recipient:
            self.graph.add_nodes_from([participant], bipartite=0)
        self.participants.append(participant)

    def remove_participant(self, participant):
        """
        removes a participant from the market
        :param participant: a participant to remove from the market
        """
        if participant.donor:
            # only update metrics for donors, so we don't update more than once
            self.metrics.update_blood_type_composition((participant, participant.partner), remove=True)
            self.metrics.update_cpra_composition((participant, participant.partner), remove=True)
            for p in self.participants:
                if p.recipient and p.compatible(participant):
                    participant.remove_neighbour(p)
        else:
            for p in self.participants:
                if p.donor and participant.compatible(p):
                    p.remove_neighbour(participant)
        if participant in self.graph.nodes():
            self.graph.remove_node(participant)

    def draw_market(self):
        if len(self.graph.nodes()) > 0:
            graph_pos = nx.spring_layout(self.graph, k=(1 / (0.9 * np.sqrt(len(
                self.graph.nodes())))))
        else:
            graph_pos = nx.spring_layout(self.graph, k=0)
        plt.clf()
        plt.axis('off')
        my_labels = {}
        colours = list()
        for participant in self.participants:
            my_labels[participant] = participant.blood_type
            if participant.donor:
                colours.append('y')
            elif participant.recipient:
                colours.append('g')
            else:
                colours.append('b')
        nx.draw_networkx(self.graph, pos=graph_pos, with_labels=True, node_size=1000, node_color=colours, labels=my_labels,
                         font_size=7.5, font_weight='bold')

    def add_pair(self, pair):
        """
        adds a patient-donor pair to the market
        pair is a tuple in the form (recipient, participant)
        :param recipient: Participant - the recipient of the patient-donor pair
        :param donor: Participant - the donor of the patient-donor pair
        """
        pair[0].add_neighbour(pair[1])
        pair[0].partner = pair[1]
        pair[1].partner = pair[0]
        self.add_participant(pair[1])
        self.add_participant(pair[0])
        self.graph.add_weighted_edges_from([(pair[0], pair[1], 1)])
        self.metrics.update_blood_type_composition(pair, remove=False)
        self.metrics.update_cpra_composition(pair, remove=False)

    def get_adj_list(self):
        """
        gets the adjacency matrix of the bipartite graph of this market
        :return: the adjacency matrix
        """
        return nx.adjacency_matrix(self.graph)

    def to_bipartite(self):
        """
        creates a bipartite graph
        :return: bipartite graph
        """
        donors = list(filter(lambda x: x.donor, self.participants))
        recipients = list(filter(lambda x: x.recipient, self.participants))
        B = nx.DiGraph()
        B.add_nodes_from(recipients, bipartite=0)
        B.add_nodes_from(donors, bipartite=1)
        for participant in self.participants:
            for neighbour in participant.neighbours:
                if participant.recipient:
                    B.add_weighted_edges_from([(participant, neighbour, 0)])
                else:
                    B.add_weighted_edges_from([(participant, neighbour, 1)])
        return B

    def remove_perished(self):
        """
        removes pairs from the market that have been in the market for their time_to_critical amount of time
        """
        participants = self.participants
        perished = list()
        for p in participants:
            if p.time_in_market >= p.time_to_critical:
                perished.append(p)
        for p in perished:
            if p in participants:
                self.participants.remove(p)

    def update(self, added_pairs=list(), matched_pairs=list(), altruists=list()):
        """
        updates the market by adding pairs, removing perished pairs, removing matched pairs, and adding altruists
        :param added_pairs: a list of tuples of participants in the form (recipiant, donor) that are to be added to the market
        :param matched_pairs: a list of pairs that need to be removed from the market
        :param altruists: a list of altruists to add to the market
        :return:
        """
        for p in self.participants:
            p.time_in_market = p.time_in_market + PERIOD_LENGTH
        self.remove_perished()
        for pair in added_pairs:
            self.add_pair(pair)
        for pair in matched_pairs:
            self.remove_participant(pair[0])
            self.remove_participant(pair[1])
        for a in altruists:
            self.add_pair(a)

    def run_period(self, new_participants=list(), new_altruists=list()):
        """
        Runs the matching algorithm for one period
        Updates the market at the end of the period
        :param new_participants: the new agents to add to the market at the end of the matching
        """
        """
        RUN MATCHING ALGORITHM
        """
        bigraph = mm.MaxMatching(self)
        matches = bigraph.maximum_matching()
        self.metrics.update_table(num_matches=len(matches), num_participants=len(self.participants))
        self.update(added_pairs=new_participants, matched_pairs=matches, altruists=new_altruists)

