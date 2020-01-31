import numpy.random as random


class Participant:
    """
        A participant in a kidney paired donation program
        This could be either a patient or donor of a patient donor pair or an altruistic donor
        It could also be a "fake participant", which is used for the implementation of altruists
        Attributes
        ---------
        id_num: int
            unique identification number of the pair, which the participant is in
        blood_type: char
            blood type of the participant
            if it is a donor or recipient, then this will be 'A', 'B', 'O' or 'AB'
            if it is a "fake participant", then this will be 'X'
        partner: Participant
            the other participant in the patient-donor pair
            if this is an altruist, they will be paired with a "fake participant"
        donor: boolean
            True if the node is a donor type
        recipient: boolean
            True if the node is a recipient type
        neighbours: list<Participant>
            list of all the nodes that can be reached from this node
            if this is a recipient in a patient-donor pair, the only node that can be reached will be the donor
        time_to_critical: int
            the time the participant can stay in the market
        time_in_market: int
            the total time the participant has been in the market
        cpra: float
            the calculated panel reactive antibodies of the participant
            this is only important for the recipient
        weight: float
            the weight given to the outgoing edge of this participant
        """
    def __init__(self, id_num, blood_type, donor, recipient, time_to_critical, weight, cpra=0):
        self.id_num = id_num
        self.blood_type = blood_type
        self.partner = None
        self.donor = donor
        self.recipient = recipient
        self.neighbours = list()
        self.time_in_market = 0
        self.time_to_critical = time_to_critical
        self.weight = weight
        self.cpra = cpra

    def add_neighbour(self, neighbour):
        """
        Adds a neighbour to the participant
        :param neighbour: a Participant
        """
        self.neighbours.append(neighbour)

    def remove_neighbour(self, neighbour):
        """
        Removes a neighbour from self.neighbour
        :param neighbour: a participant
        """
        if neighbour in self.neighbours:
            self.neighbours.remove(neighbour)

    def compatible(self, participant):
        """
        checks if this Participant is blood-type and tissue-type compatible with the participant
        :param participant: Participant
        :return: a boolean. True if this participant is compatible with the participant
        """
        if self.recipient:
            if self.blood_type == 'X' and participant.partner.blood_type == 'X':
                return False
            elif self.blood_type == 'X':
                return True
            elif self.blood_type == participant.blood_type or self.blood_type == 'AB' or participant.blood_type == 'O':
                return random.choice([False, True], p=[self.cpra, 1 - self.cpra])
        else:
            # checks if you are an altruistic donor - altruistic donors can't have dummy nodes as neighbours
            if participant.blood_type == 'X' and self.partner.blood_type == 'X':
                return False
            elif participant.blood_type == 'X':
                return True
            elif self.blood_type == participant.blood_type or participant.blood_type == 'AB' or self.blood_type == 'O':
                return random.choice([False, True], p=[participant.cpra, 1 - participant.cpra])
        return False

