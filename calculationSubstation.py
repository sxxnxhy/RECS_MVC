import tkinter as tk
from tkinter import messagebox
from tkinter import *
from PIL import Image, ImageTk  # Import the Python Imaging Library
import os
import math

class  CalculationSubstation:
    # Calculation algorithm
    def calculation_a(self, parameter_9_value, parameter_10_value, parameter_5_value):
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
        else:
            parameter_9_1 = 4400000
        result_a = [(parameter_9_1 * parameter_10_value) / (math.sqrt(3) * (parameter_5_value * 1000))]
        return result_a

    def calculation_b(self, parameter_2_value, parameter_3_value, parameter_4_value, parameter_5_value, parameter_8_value, parameter_7_value):
        result_b_1 = (1.1 * ((parameter_5_value)**2)) / (parameter_2_value)
        result_b_2 = (parameter_4_value / 100) * ((parameter_5_value**2) / parameter_3_value)
        result_b_3 = (parameter_8_value) * (parameter_7_value)
        result_b = (1.1 * ((parameter_5_value * 1000)**2)) / (result_b_1 + result_b_2 + result_b_3)

        return [result_b], [result_b_1], [result_b_2], [result_b_3]

    def calculation_c(self, parameter_9_value, parameter_10_value, parameter_7_value, parameter_8_value, parameter_5_value, parameter_6_1_value, parameter_6_2_value):
        parameter_9_2 = 0 #initial default value
        if parameter_9_value == "PD17":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD1.7":
            parameter_9_2 = 5610000
        elif parameter_9_value == "PD16":
            parameter_9_2 = 5280000
        elif parameter_9_value == "PD12":
            parameter_9_2 =  3960000
        elif parameter_9_value == "PK17":
            parameter_9_2 = 2475000


        #Resistance of wires and load currents for overhead lines
        parameter_6 = 0 #initial default value
        if parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.153
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.124
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.099
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.075
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.060
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.258
        elif parameter_6_1_value == "Cu cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x120":
            parameter_6 = 0.253
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x150":
            parameter_6 = 0.205
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x185":
            parameter_6 = 0.164
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x240":
            parameter_6 = 0.125
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x300":
            parameter_6 = 0.1
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x70":
            parameter_6 = 0.443
        elif parameter_6_1_value == "Al cable" and parameter_6_2_value == "3x95":
            parameter_6 = 0.32
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x120":
            parameter_6 = 0.234
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x150":
            parameter_6 = 0.193
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x185":
            parameter_6 = 0.156
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x240":
            parameter_6 = 0.137
        elif parameter_6_1_value == "Overhead AFL-6" and parameter_6_2_value == "3x300":
            parameter_6 = 0.121

        result_c = [((parameter_9_2 * 2 * parameter_10_value) / ((math.sqrt(3)) * (parameter_5_value * 1000) * 0.95)) * (parameter_7_value * ((parameter_6 * 0.95) + (parameter_8_value * math.sqrt(1-0.95*0.95))))]
        return result_c, parameter_9_2

    def calculation_d(self, parameter_5_value, parameter_9_value, parameter_10_value, parameter_7_value, parameter_8_value, parameter_6_1_value, parameter_6_2_value):
        result_c, _ = self.calculation_c(parameter_9_value, parameter_10_value, parameter_7_value, parameter_8_value, parameter_5_value, parameter_6_1_value, parameter_6_2_value) #ignore the second value]
        result_d = [((math.sqrt(3) * result_c[0]) / (parameter_5_value * 1000)) * 100]
        return result_d

    #a bunch of question marks on this equation.!!!!!!!!!!!!!!!!!!!!!!!!!! for k1 and k2
    def calculation_e(self, parameter_9_value, parameter_4_value, parameter_10_value, result_b):
        if parameter_9_value == "PD17":
            parameter_9_1 = 6400000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 53500
            parameter_9_5 = 3
        elif parameter_9_value == "PD1.7":
            parameter_9_1 = 6300000
            parameter_9_2 = 5610000
            parameter_9_3 = 1700
            parameter_9_4 = 38000
            parameter_9_5 = 3
        elif parameter_9_value == "PD16":
            parameter_9_1 = 5850000
            parameter_9_2 = 5280000
            parameter_9_3 = 1600
            parameter_9_4 = 46000
            parameter_9_5 = 3
        elif parameter_9_value == "PD12":
            parameter_9_1 = 5850000
            parameter_9_2 = 3960000
            parameter_9_3 = 1200
            parameter_9_4 = 36000
            parameter_9_5 = 3
        elif parameter_9_value == "PK17":
            parameter_9_1 = 5850000
            parameter_9_2 = 2475000
            parameter_9_3 = 750
            parameter_9_4 = 36000
            parameter_9_5 = 8

        result_e = [(3300+(parameter_9_4/parameter_9_3)*((parameter_9_2/parameter_9_1)**2) + parameter_9_5 * 2) / (1 - (0.38*(parameter_4_value / 100)*(parameter_9_2/parameter_9_1))-(0.26*((parameter_10_value*parameter_9_1)/(result_b[0]))))]
        return result_e, parameter_9_3


    def calculation_g(self, result_e):

        result_g = [(result_e[0][0] - 3300) / result_e[0][0]]
        return result_g

    def calculation_h(self, result_g, parameter_9_value, parameter_4_value, parameter_10_value, result_b):
        _, parameter_9_3 = self.calculation_e(parameter_9_value, parameter_4_value, parameter_10_value, result_b)

        result_h = [(result_g[0] * 3300) / (parameter_10_value * parameter_9_3)]
        return result_h

    def calculation_i(self, result_g, parameter_9_value, parameter_4_value, parameter_10_value, result_b):

        _, parameter_9_3 = self.calculation_e(parameter_9_value, parameter_4_value, parameter_10_value, result_b)

        result_i = [(result_g[0] * 3300) / (parameter_9_3)]
        return result_i