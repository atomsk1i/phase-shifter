#####################################################################################
# 
# software: Python 2.7
# file:     constellation2x2.py, meaning that digital step is 2
# author:   Aleksandar Vukovic
# mail:     va183034m@student.etf.bg.ac.rs
#
#####################################################################################

import csv  # for importing data
import os   # for pwd operation
import math # for log10() function

# for plotting TODO:
# import numpy as np
# import matplotlib.pyplot as plt

script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
rel_path = "constellation2x2.csv"
abs_file_path = os.path.join(script_dir, rel_path)
# print abs_file_path

# input information from Cadence Virtuoso
SIMULATION_STEP = 2         # step through the digital control
DIGITAL_CTRL = 256          # total digital control of the I and Q path
ERROR_dB = 0.5             # magnitude error allowed in dB 
NO_BITS_PRECISION = 6       # bits of precision to test


NO_POINTS = DIGITAL_CTRL**2/SIMULATION_STEP**2
RAW_MATRIX_WIDTH = NO_POINTS + 8
RAW_MATRIX_HEIGHT = 7
TOTAL_DEG = 360.0


# point in the polar coordinate system
class Point:
  def __init__(self, I_CTRL, Q_CTRL, phase_deg, magnitude): # constructor
    self.I_CTRL = I_CTRL
    self.Q_CTRL = Q_CTRL
    self.phase_deg = phase_deg
    self.magnitude = magnitude
    self.mag_dB = 20*math.log10(magnitude)
  def print_elements(self):                 # print the data 
      print("Magnitude: " + str(self.magnitude) + " and in dB: " + str(self.mag_dB) + "\nPhase in degrees:" + str(self.phase_deg) + "\nI_CTRL:" + str(self.I_CTRL) + " & Q_CTRL:" + str(self.Q_CTRL) + "\n" ) ;
    

def generate_list_phase_degs(no_bits):  # generate the list of ideal phase degrees for the phase shifter
    no_phase_points = 2**no_bits
    deg_step = TOTAL_DEG/no_phase_points
    
    phase_list_deg = []
    cur_phase = -180.0
    for i in range(no_phase_points+1):
        phase_list_deg.append(cur_phase)
        cur_phase = cur_phase + deg_step

    return phase_list_deg


# empty list of points 
list_of_points = []

# how to create and populate a list
# lists = [0 for x in range(4)]
# how to create and [p]
# input raw matrix
raw_matrix = [[0 for x in range(RAW_MATRIX_HEIGHT)] for y in range(RAW_MATRIX_WIDTH)] 

i = 0;
# HARDCODED with open('C:\\Users\\aleksandarv\\Documents\\Python_scripts\\constellation8x8.csv','rt') as f:
with open(abs_file_path,'rt') as f:
    data = csv.reader(f)
    for row in data:
        raw_matrix[i] = row
        i = i + 1
        # print i


for i in range(NO_POINTS):
    list_of_points.append(Point(int(raw_matrix[1][i + RAW_MATRIX_WIDTH - NO_POINTS]), int(raw_matrix[2][i + RAW_MATRIX_WIDTH - NO_POINTS]), float(raw_matrix[5][i + RAW_MATRIX_WIDTH - NO_POINTS]), float(raw_matrix[6][i + RAW_MATRIX_WIDTH - NO_POINTS])));


# get the average total gain of phase shifter
sum_of_mag_dB = 0;
for i in range(NO_POINTS):
    sum_of_mag_dB = sum_of_mag_dB + list_of_points[i].mag_dB
average_mag_dB = sum_of_mag_dB/NO_POINTS;


# extract the phase degrees into a list witch magnitude is close to the average, not important to be near the average
count_points = 0
phase_deg_list = []
for i in range(NO_POINTS):
    if list_of_points[i].mag_dB > average_mag_dB - ERROR_dB/2 and list_of_points[i].mag_dB < average_mag_dB + ERROR_dB/2:
        count_points = count_points + 1
        phase_deg_list.append(list_of_points[i].phase_deg)


# sort the list for no real reason
phase_deg_list.sort()
# print raw_matrix
# print phase_deg_list
max_diff = 0;



# print len(phase_deg_list)

# show the steps between the phase points 
# for i in range(len(phase_deg_list)-1):
    # print phase_deg_list[i+1] - phase_deg_list[i];


print "List of discrete ideal phase shifts (phase deg): "
print generate_list_phase_degs(NO_BITS_PRECISION);
list_of_ideal_points = generate_list_phase_degs(NO_BITS_PRECISION);


# calculate minimum derivation for every ideal phase from the phase shifter 
min_dev_list = []
for i in range(len(list_of_ideal_points)):
    min_dev = 180;
    for j in range(len(phase_deg_list)):
        if abs(list_of_ideal_points[i] - phase_deg_list[j]) < min_dev:
            min_dev = abs(list_of_ideal_points[i] - phase_deg_list[j])
    min_dev_list.append(round(min_dev,2))


print "List of errors (phase deg):" 
print min_dev_list

# and among them maximum deviation is:
print "Maximum error (phase deg): " + str(max(min_dev_list))

rms_sum = 0;
for i in range(len(min_dev_list)):
    rms_sum = rms_sum + min_dev_list[i]**2

min_dev_rms = math.sqrt(rms_sum/len(min_dev_list));

print "RMS error (phase deg): " + str(min_dev_rms)