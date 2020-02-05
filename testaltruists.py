from simulations import Simulations
"""
Has all the functionalities for running tests on the affects of altruists in the market
"""
def test_altruists():
    sim = Simulations(altruists=0, per_period=0)
    for i in range(1, 2, 3):
        for j in (1, 2, 3):
            sim = Simulations(altruists=i, per_period=j)
            sim.run()
