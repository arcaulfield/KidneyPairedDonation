from participant import Participant
import numpy.random as random
from config import PER_A, PER_B, PER_AB, PER_O, PER_CPRA, CPRA, TIME_TO_CRITICAL, ALT_WEIGHT, ARRIVAL_RATE, WEIGHTS


class Population:
    """
    A population where pairs are selected from
    ---------
    count: int
        count that keeps track of how many pairs have entered the market and ensures that each pair is given a unique id
    """

    def __init__(self):
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
            index = random.choice(len(CPRA), p=PER_CPRA)
            cpra_range = CPRA[index]
            cpra = random.uniform(cpra_range[0], cpra_range[1])
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
        difference = int(float(ARRIVAL_RATE) / 3.0)
        return random.choice([ARRIVAL_RATE - (difference * 2), ARRIVAL_RATE - difference, ARRIVAL_RATE, ARRIVAL_RATE + difference, ARRIVAL_RATE + (difference * 2)], p=[0.1, 0.2, 0.4, 0.2, 0.1])

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
        if WEIGHTS == "CONST":
            return 2
        return 2

