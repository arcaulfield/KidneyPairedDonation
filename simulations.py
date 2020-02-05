from participant import Participant
from market import Market
from population import Population
from market_metrics import Metrics
import numpy.random as random


class Simulations:

    def __init__(self, periods=10, verbose=False, log_data=False,
                 matching_algorithm=None, start_size=10,
                 compatible=True, pair_arrival_rate=10, period_length=4, plot_time=0.5, print_comp=False, altruists=3):
        self.periods = periods
        self.verbose = verbose
        self.log_date = log_data
        self.matching_algorithm = matching_algorithm
        self.start_size = start_size
        self.population = Population(pair_arrival_rate)
        self.compatible = compatible
        self.pair_arrival_rate = pair_arrival_rate
        self.period_length = period_length
        self.plot_time = plot_time
        self.print_comp = print_comp
        self.altruists = altruists
        self.market = Market(self.population.generate_pairs(self.start_size), self.altruists)

    def run(self):
        for i in range(self.periods):
            print("Starting period " + str(i))
            new_pairs = self.population.generate_pairs(self.population.gen_rand_population_size())
            altruists = list()
            for j in range(self.altruists):
                altruists.append(self.population.generate_altruist())
            self.market.run_period(new_participants=new_pairs,
                                   new_altruists=altruists)
        self.market.metrics.close_table()


if __name__ == "__main__":
    s = Simulations()
    s.run()
