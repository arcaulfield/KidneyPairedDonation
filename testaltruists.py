from simulations import Simulations
"""
Has all the functionalities for running tests on the affects of altruists in the market
"""


def test_altruists():
    print("Starting Simulations with 0 altruists")
    sim = Simulations(altruists=0, per_period=1)
    sim.run()
    for i in range(1, 2, 1):
        for j in range(1, 2, 1):
            print("Starting Simulations with " + str(i) + " altruists every " + str(j) + " periods")
            sim = Simulations(altruists=i, per_period=j)
            sim.run()


if __name__ == '__main__':
    test_altruists()
