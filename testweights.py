# from simulations import Simulations
from weights import Weights
import simulations as s
"""
Has all the functionalities for running tests on the affects of altruists in the market
"""


def test_weights():
    print("Starting Simulations with 0 altruists")
    w = Weights()
    run_num = 1
    for i in range(5):
        sim = s.Simulations(altruists=0, per_period=1, weights=w, run_num=run_num)
        sim.run()
        w.update_weights()
        w.reset_flag()
        run_num = run_num + 1

    # for i in [5]:
    #     for j in [1]:
    #         print("Starting Simulations with " + str(i) + " altruists every " + str(j) + " periods")
    #         sim = s.Simulations(altruists=i, per_period=j)
    #         sim.run()


if __name__ == '__main__':
    test_weights()