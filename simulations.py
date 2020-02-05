from participant import Participant
from market import Market
from population import Population
from config import ARRIVAL_RATE, START_SIZE, PERIOD_LENGTH, NUM_PERIODS
from market_metrics import Metrics
import numpy.random as random


class Simulations:

    def __init__(self, altruists=3, per_period=1):
        self.population = Population()
        self.altruists = altruists
        self.per_period = per_period
        self.market = Market(self.population.generate_pairs(START_SIZE), self.altruists, self.per_period)

    def run(self):
        for i in range(NUM_PERIODS):
            print("Starting period " + str(i))
            new_pairs = self.population.generate_pairs(self.population.gen_rand_population_size())
            altruists = list()
            if i % self.per_period == 0:
                for j in range(self.altruists):
                    altruists.append(self.population.generate_altruist())
            self.market.run_period(new_participants=new_pairs,
                                   new_altruists=altruists)
        self.market.metrics.close_table()


if __name__ == "__main__":
    s = Simulations()
    s.run()
