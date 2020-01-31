from participant import Participant
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt
import numpy as np


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

    def __init__(self, pairs):
        self.graph = nx.DiGraph()
        self.participants = list()
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
            for p in self.participants:
                if p.recipient and p.abo_compatible(participant):
                    participant.remove_neighbour(p)
        else:
            for p in self.participants:
                if p.donor and participant.abo_compatible(p):
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
        self.add_participant(pair[1])
        self.add_participant(pair[0])
        self.graph.add_weighted_edges_from([(pair[0], pair[1], 1)])

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
