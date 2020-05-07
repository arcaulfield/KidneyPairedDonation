class Weights:
    """
    Tracks and updates edge weights for simulations
    Weights are updated after each simulation and remain constant throughout a simulation
    ---------
    first_flag: boolean
        A flag that indicates whether or not it is the first time running a simulation
    w_cpra#: int
        The weight given to participants with has cpra#
    ip_cpra#: float
        The initial proportion of participants with cpra#
    p_cpra#: float
        The proportion of participants with cpra# - updated throughout simulations
    """

    def __init__(self):

        self.first_flag = True

        self.w_cpra1 = 2
        self.w_cpra2 = 2
        self.w_cpra3 = 2
        self.w_cpra4 = 2
        self.w_cpra5 = 2

        # initial proportions

        self.ip_cpra1 = 0.2
        self.ip_cpra2 = 0.2
        self.ip_cpra3 = 0.2
        self.ip_cpra4 = 0.2
        self.ip_cpra5 = 0.2

        # proportion of each weight category

        self.p_cpra1 = 0.2
        self.p_cpra2 = 0.2
        self.p_cpra3 = 0.2
        self.p_cpra4 = 0.2
        self.p_cpra5 = 0.2

    def print_weights(self):
        print("The new weights are: CPRA1 " + str(self.w_cpra1) + " CPRA2 " + str(self.w_cpra2) + " CPRA3 " + str(self.w_cpra3) + " CPRA4 " + str(self.w_cpra4) + " CPRA5 " + str(self.w_cpra5))

    def print_proportions(self):
        print("The new proportions are: CPRA1 " + str(self.p_cpra1) + " CPRA2 " + str(self.p_cpra2) + " CPRA3 " + str(self.p_cpra3) + " CPRA4 " + str(self.p_cpra4) + " CPRA5 " + str(self.p_cpra5))

    def print_init_proportions(self):
        print("The new proportions are: CPRA1 " + str(self.ip_cpra1) + " CPRA2 " + str(self.ip_cpra2) + " CPRA3 " + str(
            self.ip_cpra3) + " CPRA4 " + str(self.ip_cpra4) + " CPRA5 " + str(self.ip_cpra5))

    def update_weights(self):
        self.w_cpra1 = int(self.w_cpra1 + (1 - (self.ip_cpra1 / self.p_cpra1)))
        if self.w_cpra1 < 2:
            self.w_cpra1 = 2
        self.w_cpra2 = int(self.w_cpra2 + (1 - (self.ip_cpra2 / self.p_cpra2)))
        if self.w_cpra2 < 2:
            self.w_cpra2 = 2
        self.w_cpra3 = int(self.w_cpra3 + (1 - (self.ip_cpra3 / self.p_cpra3)))
        if self.w_cpra3 < 2:
            self.w_cpra3 = 2
        self.w_cpra4 = int(self.w_cpra4 + (1 - (self.ip_cpra4 / self.p_cpra4)))
        if self.w_cpra4 < 2:
            self.w_cpra4 = 2
        self.w_cpra5 = int(self.w_cpra5 + (1 - (self.ip_cpra5 / self.p_cpra5)))
        if self.w_cpra5 <= 2:
            self.w_cpra5 = 2
        self.print_weights()

    def set_init_proportions(self, p1, p2, p3, p4, p5):
        self.ip_cpra1 = p1
        self.ip_cpra2 = p2
        self.ip_cpra3 = p3
        self.ip_cpra4 = p4
        self.ip_cpra5 = p5
        self.first_flag = False
        self.print_init_proportions()

    def update_proportions(self, p1, p2, p3, p4, p5):
        self.p_cpra1 = p1
        self.p_cpra2 = p2
        self.p_cpra3 = p3
        self.p_cpra4 = p4
        self.p_cpra5 = p5
        self.print_proportions()

    def reset_flag(self):
        self.first_flag = True
