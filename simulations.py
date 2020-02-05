from market import Market
from population import Population
from config import START_SIZE, NUM_PERIODS


class Simulations:
    """
    Initializes and runs simulations, with a certain number of altruists and participants
    ----------
    population: Population
        a population from which new participants are created
    altruists: int
        the number of altruists that enter the market every "per_period" periods
    per_period: int
        altruists enter the market every "per_period"
    market: Market
        the kidney exchange market that we run simulations on
    """
    def __init__(self, altruists, per_period):
        self.population = Population()
        self.altruists = altruists
        self.per_period = per_period
        self.market = Market(self.population.generate_pairs(START_SIZE), self.altruists, self.per_period)

    def run(self):
        """
        runs the simulations
        adds participants every matching period and adds altruists depending on settings
        """
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

