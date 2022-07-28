# Kidney Paired Donation Similator
This repository implements a Kidney Paired Donation program simulator, which can be used to test the impacts of various factors on the number of patients matched over time in a Kidney Paired Donation program. Starting with a randomly generated population of patient-donor pairs, the simulator works by repeating the following steps to mimic a Kidney Paired Donation program working over the course of a desired number of years:
1. identifying potiental matchces (i.e. edges) in the current population
2. use a matching algorithm to decide the matches to perform
3. remove matched pairs
4. generate and add new patient-donor pairs, as well as non-deterministic donors

The simulator is highly configurable, with multiple different parameters that can be modified. Furthermore, the simulator can be used to learn weights to be assigned to patient-donor pairs in order to optimize the number of matches. It has the functionality to learn weights based on an update rule that takes as input how the composition of the population of patient-donor pairs changes over the course of the simulations.

The parameters that can be modified include: 
- the percentage of each blood type in the population
- the distribution of CPRA rates in the population
- the matching algorithm used to identify kidney donations (or matches)
- the priority (or weight) assigned to each patient-donor pair by the matching algorithm
- the number of non-deterministic donors in the population and the rate in which they join the population
- the starting size of the population and the rate in which new patient-donor pairs enter the population
- the maximum cycle and path sizes allowed to be identified by the matching algorithm

Outcomes measured by the tests include: 
- the total number of matches
- the composition of the population (the number of patients/donors with each blood type and CPRA rate)
- the time patients wait in the market before they receive a match

## How to run the simulator
### Setting parameters
Parameters for the similations can be set within `config.py`. Before running any tests:
1. indicate the file path to write result in `RESULTS_PATH`. Results will be output as an excel file.
2. specify where data will be stored using variable `DATA_PATH`. Add "patient_days_bootstring.npy", "donor_ages_bootstring.npy" and "patient_ages_bootstring.npy" to this folder. These numpy arrays store information on the number of days that a patient has been on dialysis, as well as the ages of the donors and patients respectively. 
3. indicate the starting population size with `START_SIZE` and the number of patient-donor pairs added after each period in `ARRIVAL_RATE`. 
4. specify the population distribution using variables `PER_A`, `PER_B`, `PER_AB` and `PER_O`, which indicate the percentage of the population with each different blood type, and variables`PER_CPRA` and `CPRA` to indicate the percentage of the population with each different CPRA rate. 
5. indicate the number of periods used per simulation in `NUM_PERIODS` and the length of time for each period in `PERIOD_LENGTH`.
6. specify the average number of non-deterministic donors that will enter the market after each period in `NUM_ALTRUISTS`. 
7. `WEIGHTS` specifies the weighting scheme used by the matching algorithm. Currently, the supported schemes are:
    - `"KPD"`: mimics the current Canadian Kidney Paired Donation program
    - `"OPT"` uses the weights specified in variables `CPRA1` through `CPRA5`
    - `"CONST"` for constant weights (all participants recieve the same weight)
8. choose the weight assigned to non-deterministic donours using `ALT_WEIGHT`. 
9. choose the maximum cycle and chain length that the matching algorithm can use during the simulation with variables `cycle_cap` and `chain_cap`.
10. indicate the matching algorithm to be used in `ALGORITHM`. Currently, only `"FAST"` is a valid option as it's the only supported algorithm. However, should more algorithms be supported, you can choose them here. The algorithm is implemented in `max_matching.py`.
    
### Training weights
Weights can be trained by running the main function in `trainweights.py`. This will run 50 sets of simulations, updating the weights after each simulation based on an update rule that takes into account the rate at which different types of participants change throughout the simulation. Be sure to set `WEIGHTS="OPT"` before training weights. The trained weights will be output to `weights.txt` in the path specified in `RESULTS_PATH`. To test the impacts of these weights, set `WEIGHTS="OPT"` and update variables `CPRA1` through `CPRA5` with the weights output by training and then run simulations. You can modify the update rule, by changing the `update_weights` function within `weights.py`.  

### Running simulations
`Simulations.py` contains all functionality needed to run simulations. Tests that run through different sets of parameters can be created using this class. There are already test functions in place that enable running a set of simulations, which iterate through different parameters, within `testaltruists.py`. There are two key functions:
 -   `test_altruists()` this will perform `NUM_ALTRUIST` many simulations. It iterates through the different numbers of average non-deterministic donors that enter the market, starting with 0 and finishing with `NUM_ALTRUIST` - 1. 
 -   `test_altruists_with_seeds()` calls  `test_altruists()` 50 times with 50 different random seeds. It will print out an excel file with only the data at the end of a set of simulations. 
Currently, the main funciton of `testaltruists.py` will trigger `test_altruists_with_seeds()`.

## Acknowledgementts
The matching algorithm in `algorithms/kidney_solver` contains code which comes from: https://github.com/jamestrimble/kidney_solver 
