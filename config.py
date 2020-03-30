

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
ARRIVAL_RATE = 3
#kpd start size is 100
START_SIZE = 50
# length of a period of a matching cycle (in months)
PERIOD_LENGTH = 4
# standard number of matching periods is 100
NUM_PERIODS = 2

# matching algorithm used
# either 'HA' for hungarian algorithm (doesn't restrict cycle size) or 'LP' for linear program
ALGORITHM = "HA"

# edge weights used
# either 'KPD' for the current Canadian KPD weights, 'OPT' for the optimized weights, 'CONST' for constant weights
WEIGHTS = "KPD"