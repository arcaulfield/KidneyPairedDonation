from participant import Participant
import numpy.random as random
from config import PER_A, PER_B, PER_AB, PER_O, PER_CPRA, CPRA, TIME_TO_CRITICAL, ALT_WEIGHT


class Population:
    """
    A population where pairs are selected from
    ---------
    count: int
        count that keeps track of how many pairs have entered the market and ensures that each pair is given a unique id
    """

    def __init__(self, arrival_rate=40):
        self.arrival_rate = arrival_rate
        self.count = 0

    def generate_pairs(self, num_pairs):
        """
        generates new patient-donor pairs based on the distribution of the population
        :param num_pairs: int - the number of pairs to generate
        :return: a list of tuples of participants in the form (recipient, donor)
        """
        new_pairs = list()
        i = 0
        while i < num_pairs:
            cpra = random.choice(CPRA, p=PER_CPRA)
            donor_type = random.choice(['A', 'B', 'O', 'AB'], p=[PER_A, PER_B, PER_O, PER_AB])
            recipient_type = random.choice(['A', 'B', 'O', 'AB'], p=[PER_A, PER_B, PER_O, PER_AB])
            weight = self.calculate_weight(donor_type, recipient_type, cpra)

            # if they are blood type compatible, only create new participant pairs if they are tissue type incompatible
            if donor_type == 'O' or recipient_type == 'AB' or donor_type == recipient_type:
                if random.choice([True, False], p=[cpra, 1-cpra]):
                    donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra)
                    recipient = Participant(self.count, recipient_type, donor=False, recipient=True, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra)
                    new_pairs.append((recipient, donor))
                    i += 1
                    self.count += 1
            else:
                donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra)
                recipient = Participant(self.count, recipient_type, donor=False, recipient=True, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra)
                new_pairs.append((recipient, donor))
                i += 1
                self.count += 1
        return new_pairs

    def gen_rand_population_size(self):
        """
        gets a random population size centered around the arrival rate
        :return: integer representing a population size
        """
        difference = int(float(self.arrival_rate) / 3.0)
        return random.choice([self.arrival_rate - (difference * 2), self.arrival_rate - difference, self.arrival_rate, self.arrival_rate + difference, self.arrival_rate + (difference * 2)], p=[0.1, 0.2, 0.4, 0.2, 0.1])

    def generate_altruist(self):
        """
        generates an altruistic donor
        :return: a tuple of Participants in the form ("fake recipient", altruisitc donor)
        """
        donor_type = random.choice(['A', 'B', 'O', 'AB'], p=[PER_A, PER_B, PER_O, PER_AB])
        altruistic_donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=ALT_WEIGHT, cpra=0)
        recipient = Participant(self.count, blood_type='X', donor=False, recipient=True,  time_to_critical=TIME_TO_CRITICAL, weight=ALT_WEIGHT, cpra=0)
        self.count += 1
        return recipient, altruistic_donor

    def calculate_weight(self, donor_type, recipient_type, cpra):
        """
        determines the weight of a pair based on blood type of patient and donor and cpra
        :param donor_type: blood type of the donor
        :param recipient_type: blood type of the recipient
        :param cpra: the cpra
        :return: a weight in the form of an int
        """
        weight = 2
        if recipient_type == 'O':
            weight = 50
        elif donor_type == 'A':
            weight = 40
        elif recipient_type == 'B' or recipient_type =='A':
            weight = 10
        elif donor_type == 'AB':
            if cpra == 0.97:
                weight = 25
            elif cpra == 0.75:
                weight = 10
            elif cpra == 0.25:
                weight = 5
            else:
                weight = 2
        return weight

