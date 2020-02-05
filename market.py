import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from config import PERIOD_LENGTH
import algorithm.max_matching as mm


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
        pair[0].partner = pair[1]
        pair[1].partner = pair[0]

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

    def run_period(self, verbose=True, new_participants=list(), new_altruists=list()):
        """
        Runs the matching algorithm for one period
        Updates the market at the end of the period
        :param algorithm: the algorithm to use for the matching
        :param verbose: a boolean indicating whether or not to print relevant information
        :param new_agents: the new agents to add to the market at the end of the matching
        """
        # if verbose:
        #     print("\n\n----------------Update----------------")
        #     print("Time in market: ", self.time)
        #     print("Total number of pairs that have entered the market: ",
        #           self.total_agents)
        #     print("Total number of pairs that have perished: ", len(self.perished))
        #     print("Total number of matched pairs: ", len(self.matched))
        #     print("Total number of agents currently in the market: ", len(self.pairs))
        #     print("Current pairs ", [a.id_num for a in self.pairs])

        # plt.clf()
        # plt.axis('off')
        # if len(self.Graph.nodes()) > 0:
        #     self.graph_pos = nx.spring_layout(self.Graph, k=(1 / (0.9 * np.sqrt(len(
        #         self.Graph.nodes())))))
        # else:
        #     self.graph_pos = nx.spring_layout(self.Graph, k=0)
        # my_labels = {}
        # colours = list()
        # for pair in self.pairs:
        #     my_labels[pair] = pair.recipient_type + ', ' + pair.donor_type
        #     if pair.recipient_type == 'X':
        #         colours.append('w')
        #     elif pair.cpra == 0:
        #         colours.append('b')
        #     elif pair.cpra == 0.25:
        #         colours.append('g')
        #     elif pair.cpra == 0.75:
        #         colours.append('y')
        #     else:
        #         colours.append('r')
        # for altruist in self.altruists:
        #     my_labels[altruist] = altruist.donor_type
        #     colours.append('b')
        # nx.draw_networkx(self.Graph, pos=self.graph_pos, with_labels=True, node_size=1000, node_color=colours,
        #                  labels=my_labels,
        #                  font_size=7.5, font_weight='bold')

        # plt.plot()
        # plt.title("Period " + str(self.period_num) + "\nMatches " + str(len(self.matched)) + " || Perished " + str(
        #   len(self.perished)))
        # plt.show()
        # plt.pause(self.plot_time)

        if verbose:
            print("Running matching algorithm")
        """
        RUN MATCHING ALGORITHM
        """

        bigraph = mm.MaxMatching(self)
        matches = bigraph.maximum_matching()


        matched_pairs = []
        if verbose:
            print("Matched " + str(len(matches)) + " pairs")
        # self.total_matched += len(matches)
        # colour the edges that we have matched

        self.update(added_pairs=new_participants, matched_pairs=matched_pairs, altruists=new_altruists)
        # bigraph.update_bigraph(add_pairs=new_agents, remove_pairs=matched_pairs)
        # for perished in self.perished:
        #   if perished in bigraph.bigraph.participants:
        #      bigraph.update_bigraph(add_pairs=list(), remove_pairs=perished)
        if verbose:
            print("Added " + str(len(new_participants)) + " pairs to the market.")
