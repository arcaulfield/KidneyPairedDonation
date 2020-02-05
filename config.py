

### The distribution of the population ###

# percentage of the population with blood type A
PER_A = 0.42
# percentage of the population with blood type B
PER_B = 0.09
# percentage of the population with blood type AB
PER_AB = 0.03
# percentage of the population with blood type O
PER_O = 0.46

# percertage with each CPRA level
PER_CPRA = [0.40, 0.35, 0.20, 0.05]
# CPRA levels
CPRA = [0, 0.25, 0.75, 0.97]

# the edge weight to give an altruistic donor
ALT_WEIGHT = -6

# boolean indicating whether or not to take in account perishing
PERISH = False
# on average, the amount of time a patient stays in the market
TIME_TO_CRITICAL = 80

### File IO ###
RESULTS_PATH = "results"

### Simulation stats ###
ARRIVAL_RATE = 4
START_SIZE = 4
# length of a period of a matching cycle (in months)
PERIOD_LENGTH = 4
NUM_PERIODS = 3
