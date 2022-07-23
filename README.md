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

