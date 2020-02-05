import xlsxwriter
import os
from config import RESULTS_PATH, CPRA

class Metrics:
    """
    Stores all the metrics to track a market. Has all the functionality necessary for writing to excel files.
    In particular, writes to tables based on results.
    """
    def __init__(self, num_altruists, per_period):
        self.num_altruists = num_altruists
        self.per_period = per_period
        self.donor_o_patient_o = 0
        self.donor_a_patient_o = 0
        self.donor_b_patient_o = 0
        self.donor_ab_patient_o = 0
        self.donor_o_patient_ab = 0
        self.donor_a_patient_ab = 0
        self.donor_b_patient_ab = 0
        self.donor_ab_patient_ab = 0
        self.donor_o_patient_a = 0
        self.donor_a_patient_a = 0
        self.donor_b_patient_a = 0
        self.donor_ab_patient_a = 0
        self.donor_o_patient_b = 0
        self.donor_a_patient_b = 0
        self.donor_b_patient_b = 0
        self.donor_ab_patient_b = 0
        self.cpra_1 = 0
        self.cpra_2 = 0
        self.cpra_3 = 0
        self.cpra_4 = 0
        self.total_num_perished = 0
        self.total_num_matched = 0
        self.total_num_participants = 0
        self.period_num = 0
        # self.market = market
        # Create an new Excel file and add a worksheet.
        results_file_path = os.path.join(RESULTS_PATH, str(self.num_altruists) + "AltruistsPer" + str(self.per_period) + "periods.xlsx")
        self.workbook = xlsxwriter.Workbook(results_file_path)
        self.worksheet = self.workbook.add_worksheet()
        self.initialize_table()

    def update_blood_type_composition(self, pair, remove):
        """
        Updates the ongoing count of the different type blood types currently in the market
        :param pair: a tuple of Participants, in the form (recipient, donor) a patient-donor pair that we are adding/removing
        :param remove: false if adding to the market, true if removing from the market
        """
        # don't log altruist blood types here
        if pair[0].blood_type == 'X':
            return
        if remove:
            var = -1
        else:
            var = 1
        if pair[1].blood_type == 'O':
            if pair[0].blood_type == 'O':
                self.donor_o_patient_o += var
            if pair[0].blood_type == 'A':
                self.donor_o_patient_a += var
            if pair[0].blood_type == 'AB':
                self.donor_o_patient_ab += var
            if pair[0].blood_type == 'B':
                self.donor_o_patient_b += var
        if pair[1].blood_type == 'A':
            if pair[0].blood_type == 'O':
                self.donor_a_patient_o += var
            if pair[0].blood_type == 'A':
                self.donor_a_patient_a += var
            if pair[0].blood_type == 'AB':
                self.donor_a_patient_ab += var
            if pair[0].blood_type == 'B':
                self.donor_a_patient_b += var
        if pair[1].blood_type == 'AB':
            if pair[0].blood_type == 'O':
                self.donor_ab_patient_o += var
            if pair[0].blood_type == 'A':
                self.donor_ab_patient_a += var
            if pair[0].blood_type == 'AB':
                self.donor_ab_patient_ab += var
            if pair[0].blood_type == 'B':
                self.donor_ab_patient_b += var
        if pair[1].blood_type == 'B':
            if pair[0].blood_type == 'O':
                self.donor_b_patient_o += var
            if pair[0].blood_type == 'A':
                self.donor_b_patient_a += var
            if pair[0].blood_type == 'AB':
                self.donor_b_patient_ab += var
            if pair[0].blood_type == 'B':
                self.donor_b_patient_b += var

    def update_cpra_composition(self, pair, remove):
        """
        updates the ongoing count of the different cpra rates in the market
        :param pair: a tuple of participants, in the form (recipient, donor) patient-donor pair that we are adding/removing
        :param remove: false if adding to the market, true if removing from the market
        """
        if pair[0].blood_type == 'X':
            return
        if remove:
            var = -1
        else:
            var = 1
        if pair[0].cpra == 0:
            self.cpra_1 += var
        elif pair[0].cpra == 0.25:
            self.cpra_2 += var
        elif pair[0].cpra == 0.75:
            self.cpra_3 += var
        elif pair[0].cpra == 0.97:
            self.cpra_4 +=var

    def initialize_table(self):
        # Widen the first column to make the text clearer.
        self.worksheet.set_column('A:AA', 20)

        # Add a bold format to use to highlight cells.
        bold = self.workbook.add_format({'bold': True})

        # Write some simple text.
        self.worksheet.write('A1', 'Period Number', bold)
        # Write some simple text.
        self.worksheet.write('B1', 'Matches in Period', bold)
        self.worksheet.write('C1', 'Participants in Period', bold)
        self.worksheet.write('D1', 'Total Num Participants', bold)
        self.worksheet.write('E1', 'Total Num Matches', bold)
        self.worksheet.write('F1', 'Current # (A, O)', bold) # (recipient, donor)
        self.worksheet.write('G1', 'Current # (A, A)', bold)
        self.worksheet.write('H1', 'Current # (A, B)', bold)
        self.worksheet.write('I1', 'Current # (A, AB)', bold)
        self.worksheet.write('J1', 'Current # (B, O)', bold)
        self.worksheet.write('K1', 'Current # (B, A)', bold)
        self.worksheet.write('L1', 'Current # (B, B)', bold)
        self.worksheet.write('M1', 'Current # (B, AB)', bold)
        self.worksheet.write('N1', 'Current # (AB, O)', bold)
        self.worksheet.write('O1', 'Current # (AB, A)', bold)
        self.worksheet.write('P1', 'Current # (AB, B)', bold)
        self.worksheet.write('Q1', 'Current # (AB, AB)', bold)
        self.worksheet.write('R1', 'Current # (O, O)', bold)
        self.worksheet.write('S1', 'Current # (O, A)', bold)
        self.worksheet.write('T1', 'Current # (O, B)', bold)
        self.worksheet.write('U1', 'Current # (O, AB)', bold)
        self.worksheet.write('V1', 'Current # CPRA: ' + str(CPRA[0]), bold)
        self.worksheet.write('W1', 'Current # CPRA: ' + str(CPRA[1]), bold)
        self.worksheet.write('X1', 'Current # CPRA: ' + str(CPRA[2]), bold)
        self.worksheet.write('Y1', 'Current # CPRA: ' + str(CPRA[3]), bold)
        self.worksheet.write('Z1', 'Num Altruists in Market', bold)
        self.worksheet.write('AA1', 'Num Altruists in Matching', bold)

    def update_table(self, num_matches, num_participants, num_added, num_altruists_in_market, num_altruists_in_matching):
        self.period_num = self.period_num + 1
        # Add a bold format to use to highlight cells.
        self.total_num_matched = self.total_num_matched + num_matches
        if self.total_num_participants == 0:
            self.total_num_participants = num_participants
        else:
            self.total_num_participants = self.total_num_participants + num_added
        # Write some numbers, with row/column notation.
        self.worksheet.write(self.period_num, 0, self.period_num)
        self.worksheet.write(self.period_num, 1, num_matches)
        self.worksheet.write(self.period_num, 2, num_participants)
        self.worksheet.write(self.period_num, 3, self.total_num_participants)
        self.worksheet.write(self.period_num, 4, self.total_num_matched)
        self.worksheet.write(self.period_num, 5, self.donor_o_patient_a)
        self.worksheet.write(self.period_num, 6, self.donor_a_patient_a)
        self.worksheet.write(self.period_num, 7, self.donor_b_patient_a)
        self.worksheet.write(self.period_num, 8, self.donor_ab_patient_a)
        self.worksheet.write(self.period_num, 9, self.donor_o_patient_b)
        self.worksheet.write(self.period_num, 10, self.donor_a_patient_b)
        self.worksheet.write(self.period_num, 11, self.donor_b_patient_b)
        self.worksheet.write(self.period_num, 12, self.donor_ab_patient_b)
        self.worksheet.write(self.period_num, 13, self.donor_o_patient_ab)
        self.worksheet.write(self.period_num, 14, self.donor_a_patient_ab)
        self.worksheet.write(self.period_num, 15, self.donor_b_patient_ab)
        self.worksheet.write(self.period_num, 16, self.donor_ab_patient_ab)
        self.worksheet.write(self.period_num, 17, self.donor_o_patient_o)
        self.worksheet.write(self.period_num, 18, self.donor_a_patient_o)
        self.worksheet.write(self.period_num, 19, self.donor_b_patient_o)
        self.worksheet.write(self.period_num, 20, self.donor_ab_patient_o)
        self.worksheet.write(self.period_num, 21, self.cpra_1)
        self.worksheet.write(self.period_num, 22, self.cpra_2)
        self.worksheet.write(self.period_num, 23, self.cpra_3)
        self.worksheet.write(self.period_num, 24, self.cpra_4)
        self.worksheet.write(self.period_num, 25, num_altruists_in_market)
        self.worksheet.write(self.period_num, 26, num_altruists_in_matching)

    def close_table(self):
        self.workbook.close()

