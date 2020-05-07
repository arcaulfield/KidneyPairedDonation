

### POPULATION DISTRIBUTION ###

# percentage of the population with blood type A
PER_A = 0.42
# percentage of the population with blood type B
PER_B = 0.09
# percentage of the population with blood type AB
PER_AB = 0.03
# percentage of the population with blood type O
PER_O = 0.46

# percertage with each CPRA level
PER_CPRA = [0.24, 0.29, 0.24, 0.1, 0.13]
# CPRA levels - note: these represent
CPRA = [(0, 0), (0.01, 0.50), (0.51, 0.94), (0.95, 0.96), (0.97, 1)]

#percentage in each province

#includes Yukon
PER_BC = 0.2508833922261484

PER_AL = 0.11749116607773852
PER_SK = 0.028268551236749116
PER_MN = 0.046819787985865724
PER_ON = 0.37809187279151946
PER_QC = 0.10865724381625441
PER_NS = 0.026501766784452298
PER_NB = 0.023851590106007067
PER_PEI = 0.0035335689045936395
PER_NFL = 0.015901060070671377


# the edge weight to given to altruistic donors - NOTE this cannot be 0
ALT_WEIGHT = -2

# boolean indicating whether or not to take in account perishing
PERISH = False
# on average, the amount of time a patient stays in the market
TIME_TO_CRITICAL = 80

### FILE I/O ###

RESULTS_PATH = "results"
DATA_PATH = "data"

### SIMULATION CONFIGURATIONS ###

#kpd arrival rate is 37
ARRIVAL_RATE = 37
#kpd start size is 100
START_SIZE = 100
# length of a period of a matching cycle (in months)
# kpd period length is 4 months
PERIOD_LENGTH = 4
# standard number of matching periods is 100
NUM_PERIODS =10

# matching algorithm used
# either 'HA' for hungarian algorithm (doesn't restrict cycle size) or 'LP' for linear program or 'FAST' for faster cycle
ALGORITHM = "FAST"

# edge weights used
# either 'KPD' for the current Canadian KPD weights, 'OPT' for the optimized weights, 'CONST' for constant weights
WEIGHTS = "KPD"

