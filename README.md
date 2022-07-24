# Kidney Paired Donation Similator
This repository implements a Kidney Paired Donation program simulator. It enables tests to be performed on the long term impact of a variety of parameters on the number of patients matched. Starting with a population of patient-donor pairs (randomly generated using a specified population distribution), the simulator repeats the following steps to mimic a Kidney Paired Donation program working over the course of a desired number of years:
1. identify potiental matchces (i.e. edges) in the current population
2. use a matching algorithm to decide the matches to perform
3. remove matched pairs
4. generate and add new patient-donor pairs, as well as non-deterministic donors
Results of the simulation are outputed in an excel document after the simulations have been performed. This repository also contains functionality to learn weights based on how the population composition changes over the course of the simulations. These learnt weights can then be used to perform tests.

Parameters that can be modified include: 
- the percentage of each blood type in the population
- the distribution of CPRA rates in the population
- the matching algorithm used to kidney donations (or matches) that will be performed
- the priority (or weight) assigned to each patient and donor pair by the matching algorithm
- the number of non-deterministic donors in the population and the rate in which they join the population
- the starting size of the population and the rate in which new patient-donor pairs enter the population
- the maximum cycle and path sizes allowed to be identified by the matching algorithm

Outcomes measured by the tests include: 
- the total number of matches
- the composition of the population
- the time patients wait in the market before they receive a time

## How to run the simulator
### Setting parameters
Parameters for the similations can be set within `config.py`. Before running any tests:
1. indicate the file path to write result in `RESULTS_PATH`
2. specify where data will be stored using variable `DATA_PATH`. Add "patient_days_bootstring.npy", "donor_ages_bootstring.npy" and "patient_ages_bootstring.npy" to this folder. These numpy arrays store information on the number of days that a patient has been on dialysis, as well as the ages of the donors and patients respectiely. The data isn't included in this repo for privacy issues. 
3. indicate the starting population size with `START_SIZE` and the number of patient donor pairs added after each period in `ARRIVAL_RATE`. 
4. specify the population distribution using variables `PER_A`, `PER_B`, `PER_AB` and `PER_O`, which indicate the percentage of the population with each different blood type, and variables`PER_CPRA` and `CPRA` to indicate the percentage of the population with each different CPRA rate. 
5. indicate the number of periods used per simulation in `NUM_PERIODS` and the length of time for each period in `PERIOD_LENGHT`.
6. if you would like participants to leave the market after a specified amount of time, you can set the boolean variable `PERISH` to `True`.
7. specify the average number of altruists that will enter the market after each period in `NUM_ALTRUISTS`. 
8. `WEIGHTS` is used to specify the weighting scheme used by the matching algorithm. Currently, the supported schemes are:
    - `"KPD"`: mimics the current Canadian KPD program
    - `"OPT"` uses the weights specified in variables `CPRA1` through `CPRA5` (see note below to understand how who these weights are assigned to)
    - `"CONST"` for constant weights (all participants recieve the same weight)
9. choose the weight assigned to non-deterministic donours using `ALT_WEIGHT`. 
10. choose the maximum cycle and chain length that the matching algorithm can use during the simulation with variables `cycle_cap` and `chain_cap`.
11. indicate the matching algorithm to be used in `ALGORITHM`. Currently, only `"FAST"` is a valid option as it's the only supported algorithm. However, should more algorithms be supported, you can choose them here. The algorithm is implemented in `max_matching.py`.
    
### Training weights
Weights can be tried by running the main function in `trainweights.py`. This will run 50 sets of simulations, updating the weights after each simulation based on an update rule that takes into account the rate at which different types of participants changes throughout the simulation. Be sure to set `WEIGHTS="OPT"` before training weights. The trained weights will be output to `weights.txt` in the path specified in `RESULTS_PATH`. To test the impacts of these weights, set `WEIGHTS="OPT"` and update variables `CPRA1` through `CPRA5` with the weights output by training, before running any simulations. You can modify the update rule, by changing the `update_weights` function within `weights.py`.  

### Running simulations
`Simulations.py` has contains all functionality need to run simulations and tests can be created that run through different sets of parameters. There are test functions already in place that enable running a set of simulations iterating through different parameters and outputing results, within `testaltruists.py`. There are two key functions:
 -   `test_altruists()` this will perform `NUM_ALTRUIST` many simulations, one simulation for each of 0 through NUM_ALTRUIST many iterations. 
 -   `test_altruists_with_seeds()` calls  `test_altruists()` 50 times with 50 different random seeds. It will print out an excel file with only the data at the end of a set of simulations. 
Currently, the main funciton of `testaltruists.py` will trigger `test_altruists_with_seeds()`.

## Directory Structure

Simulations works through a set of matching sycles

algorithms/kidney_solver implements the matching algorithm. This repo comes from: https://github.com/jamestrimble/kidney_solver 
Populaiton manages functionality related to the population
participant is a participant (either donor, patient or non-deterministic donor)
market_metrics tracks the market metrics, writing to an excel table 
algorithms/max_matching.py runs the matching algorithm specified in config.py. Either HA (hungarian algorithm). Note this is unused legacy code and has broken 


This project was developed with the help of @linyid.
