from participant import Participant
import numpy.random as random
import os
from config import PER_A, PER_B, PER_AB, PER_O, PER_CPRA, CPRA, TIME_TO_CRITICAL, ALT_WEIGHT, ARRIVAL_RATE, WEIGHTS, DATA_PATH, PER_BC, PER_AL, PER_SK, PER_MN, PER_ON, PER_QC, PER_NS, PER_NB, PER_PEI, PER_NFL
import numpy as np


class Population:
    """
    A population where pairs are selected from
    ---------
    count: int
        count that keeps track of how many pairs have entered the market and ensures that each pair is given a unique id
    """

    def __init__(self, weights=None):
        self.count = 0
        dialysis_days_file_path = os.path.join(DATA_PATH, "patient_days_bootstring.npy")
        donor_ages_file_path = os.path.join(DATA_PATH, "donor_ages_bootstring.npy")
        patient_ages_file_path = os.path.join(DATA_PATH, "patient_ages_bootstring.npy")

        self.dialysis_days = np.load(dialysis_days_file_path)
        self.donor_ages = np.load(donor_ages_file_path)
        self.patient_ages = np.load(patient_ages_file_path)

        self.weights = weights



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

            dialysis_day = np.random.choice(self.dialysis_days)
            donor_age = np.random.choice(self.donor_ages)
            patient_age = np.random.choice(self.patient_ages)

            province = random.choice(['BC', 'AL', 'SK', 'MN', 'ON', 'QC', 'NS', 'NB', 'PEI', 'NFL'], p=[PER_BC, PER_AL, PER_SK, PER_MN, PER_ON, PER_QC, PER_NS, PER_NB, PER_PEI, PER_NFL])

            # if they are blood type compatible, only create new participant pairs if they are tissue type incompatible
            if donor_type == 'O' or recipient_type == 'AB' or donor_type == recipient_type:
                if random.choice([True, False], p=[cpra, 1-cpra]):
                    donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra, age=donor_age, dialysis_days=dialysis_day, province=province)
                    recipient = Participant(self.count, recipient_type, donor=False, recipient=True, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra, age=patient_age, dialysis_days=dialysis_day, province=province)
                    new_pairs.append((recipient, donor))
                    i += 1
                    self.count += 1
            else:
                donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra, age=donor_age, dialysis_days=dialysis_day, province=province)
                recipient = Participant(self.count, recipient_type, donor=False, recipient=True, time_to_critical=TIME_TO_CRITICAL, weight=weight, cpra=cpra, age=patient_age, dialysis_days=dialysis_day,province=province)
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
        donor_age = np.random.choice(self.donor_ages)
        donor_type = random.choice(['A', 'B', 'O', 'AB'], p=[PER_A, PER_B, PER_O, PER_AB])
        altruistic_donor = Participant(self.count, donor_type, donor=True, recipient=False, time_to_critical=TIME_TO_CRITICAL, weight=ALT_WEIGHT, cpra=0, age=donor_age, dialysis_days=0)
        recipient = Participant(self.count, blood_type='X', donor=False, recipient=True,  time_to_critical=TIME_TO_CRITICAL, weight=ALT_WEIGHT, cpra=0, dialysis_days=0)
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
        elif WEIGHTS == "OPT":
            assert self.weights is not None
            if cpra == CPRA[0][1]:
                return self.weights.w_cpra1
            elif cpra <= CPRA[1][1]:
                return self.weights.w_cpra2
            elif cpra <= CPRA[2][1]:
                return self.weights.w_cpra3
            elif cpra <= CPRA[3][1]:
                return self.weights.w_cpra4
            elif cpra <= CPRA[4][1]:
                return self.weights.w_cpra5
        return 2

