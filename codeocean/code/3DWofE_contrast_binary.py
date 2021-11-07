# Contrast and studentized contrast of binary evidential models
# The input is a csv file with the following columns respectively: X, Y, Z, Grade (Target Element), Fac1, Fac2, ...
# -------
import csv
import itertools
import math

# Number of evidential models
input_file = open("/data/Input_Binary.csv")
input_reader = csv.reader(input_file)
for row in input_reader:
    num_fac = len(row)-4
    break
del input_file
del input_reader

# Threshold value for target element and all other evidential models
threshold_target = 0.4
threshold_fac = 0.5

# Number of voxels for different items
# NumT: total number of voxels
input_file = open("/data/Input_Binary.csv")
input_reader = csv.reader(input_file)
NumT = 0
for row in input_reader:
    NumT += 1
del input_file
del input_reader

# NumD: number of known mineralization-bearing voxels
input_file = open("/data/Input_Binary.csv")
input_reader = csv.reader(input_file)
NumD = 0
for row in input_reader:
    if float(row[3]) > threshold_target:
        NumD += 1
del input_file
del input_reader

# NumB: number of anomalous voxels in evidential models
input_file = open("/data/Input_Binary.csv")
input_reader = csv.reader(input_file)
output_file = open("/results/NumB.csv", "wb")
output_writer = csv.writer(output_file)
NumB_temp = [0]*num_fac
for row in input_reader:
    for i in range(num_fac):
        if float(row[i+4]) > threshold_fac:
            NumB_temp[i] += 1
output_writer.writerow(NumB_temp)
del input_file
del input_reader
del output_file
del output_writer

# NumBD: number of intersected mineralization-bearing voxels and anomalous voxels of evidential models
# "_abs" means in the absence of the last parameter before underscore
input_file = open("/data/Input_Binary.csv")
input_reader = csv.reader(input_file)
output1_file = open("/results/NumBD.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("/results/NumB_absD.csv", "wb")
output2_writer = csv.writer(output2_file)
output3_file = open("/results/NumBD_abs.csv", "wb")
output3_writer = csv.writer(output3_file)
output4_file = open("/results/NumB_absD_abs.csv", "wb")
output4_writer = csv.writer(output4_file)
NumBD_temp = [0]*num_fac
NumB_absD_temp = [0]*num_fac
NumBD_abs_temp = [0]*num_fac
NumB_absD_abs_temp = [0]*num_fac
for row in input_reader:
    for i in range(num_fac):
        if float(row[3]) > threshold_target and float(row[i+4]) > threshold_fac:
            NumBD_temp[i] += 1
        elif float(row[3]) > threshold_target and float(row[i+4]) <= threshold_fac:
            NumB_absD_temp[i] += 1
        elif float(row[3]) <= threshold_target and float(row[i+4]) > threshold_fac:
            NumBD_abs_temp[i] += 1
        elif float(row[3]) <= threshold_target and float(row[i+4]) <= threshold_fac:
            NumB_absD_abs_temp[i] += 1
output1_writer.writerow(NumBD_temp)
output2_writer.writerow(NumB_absD_temp)
output3_writer.writerow(NumBD_abs_temp)
output4_writer.writerow(NumB_absD_abs_temp)
del input_file
del input_reader
del output1_file
del output1_writer
del output2_file
del output2_writer
del output3_file
del output3_writer
del output4_file
del output4_writer

# Probabilities, odds and logits
input_file = open("/results/NumBD.csv")
input_reader = csv.reader(input_file)
output_file = open("/results/ProBD.csv", "wb")
output_writer = csv.writer(output_file)
ProBD_temp = []
for row in input_reader:
    for i in range(num_fac):
        ProBD_temp.append(float(row[i])/NumD)
    output_writer.writerow(ProBD_temp)
    ProBD_temp = []
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("/results/NumB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/NumBD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/ProBD_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProBD_abs_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        ProBD_abs_temp.append((float(row1[i])-float(row2[i]))/(NumT-NumD))
    output_writer.writerow(ProBD_abs_temp)
    ProBD_abs_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("/results/NumBD.csv")
input_reader = csv.reader(input_file)
output_file = open("/results/ProB_absD.csv", "wb")
output_writer = csv.writer(output_file)
ProB_absD_temp = []
i = 1
j = 0
for row in input_reader:
    for i in range(num_fac):
        ProB_absD_temp.append((NumD-float(row[i]))/NumD)
    output_writer.writerow(ProB_absD_temp)
    ProB_absD_temp = []
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("/results/NumB.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/NumBD.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/ProB_absD_abs.csv", "wb")
output_writer = csv.writer(output_file)
ProB_absD_abs_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        ProB_absD_abs_temp.append((NumT-float(row1[i])-NumD+float(row2[i]))/(NumT-NumD))
    output_writer.writerow(ProB_absD_abs_temp)
    ProB_absD_abs_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input1_file = open("/results/ProBD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/ProBD_abs.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/LS.csv", "wb")
output_writer = csv.writer(output_file)
LS_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row2[i]) != 0:
            LS_temp.append(float(row1[i])/float(row2[i]))
        else:
            LS_temp.append("Null")
    output_writer.writerow(LS_temp)
    LS_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("/results/LS.csv")
input_reader = csv.reader(input_file)
output_file = open("/results/W_pos.csv", "wb")
output_writer = csv.writer(output_file)
W_pos_temp = []
for row in input_reader:
    for i in range(num_fac):
        if row[i] != "Null" and float(row[i]) != 0:
            W_pos_temp.append(math.log(float(row[i])))
        else:
            W_pos_temp.append("Null")
    output_writer.writerow(W_pos_temp)
    W_pos_temp = []
del input_file
del input_reader
del output_file
del output_writer

input1_file = open("/results/ProB_absD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/ProB_absD_abs.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/LN.csv", "wb")
output_writer = csv.writer(output_file)
LN_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row2[i]) != 0:
            LN_temp.append(float(row1[i])/float(row2[i]))
        else:
            LN_temp.append("Null")
    output_writer.writerow(LN_temp)
    LN_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

input_file = open("/results/LN.csv")
input_reader = csv.reader(input_file)
output_file = open("/results/W_neg.csv", "wb")
output_writer = csv.writer(output_file)
W_neg_temp = []
for row in input_reader:
    for i in range(num_fac):
        if row[i] != "Null" and float(row[i]) != 0:
            W_neg_temp.append(math.log(float(row[i])))
        else:
            W_neg_temp.append("Null")
    output_writer.writerow(W_neg_temp)
    W_neg_temp = []
del input_file
del input_reader
del output_file
del output_writer

# Contrast
input1_file = open("/results/W_pos.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/W_neg.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/Contrast.csv", "wb")
output_writer = csv.writer(output_file)
contrast_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null":
            contrast_temp.append(float(row1[i])-float(row2[i]))
        else:
            contrast_temp.append("Null")
    output_writer.writerow(contrast_temp)
    contrast_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer

# Variance and standard deviation of positive and negative weights
input1_file = open("/results/NumBD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/NumBD_abs.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("/results/Var_W_pos.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("/results/StD_W_pos.csv", "wb")
output2_writer = csv.writer(output2_file)
var_w_pos_temp = []
std_w_pos_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row1[i]) != 0 and float(row2[i]) != 0:
            var_w_pos_temp.append((1/float(row1[i]))+(1/float(row2[i])))
            std_w_pos_temp.append(math.sqrt((1/float(row1[i]))+(1/float(row2[i]))))
        else:
            var_w_pos_temp.append("Null")
            std_w_pos_temp.append("Null")
    output1_writer.writerow(var_w_pos_temp)
    output2_writer.writerow(std_w_pos_temp)
    var_w_pos_temp = []
    std_w_pos_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

input1_file = open("/results/NumB_absD.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/NumB_absD_abs.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("/results/Var_W_neg.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("/results/StD_W_neg.csv", "wb")
output2_writer = csv.writer(output2_file)
var_w_neg_temp = []
std_w_neg_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if float(row1[i]) != 0 and float(row2[i]) != 0:
            var_w_neg_temp.append((1/float(row1[i]))+(1/float(row2[i])))
            std_w_neg_temp.append(math.sqrt((1/float(row1[i]))+(1/float(row2[i]))))
        else:
            var_w_neg_temp.append("Null")
            std_w_neg_temp.append("Null")
    output1_writer.writerow(var_w_neg_temp)
    output2_writer.writerow(std_w_neg_temp)
    var_w_neg_temp = []
    std_w_neg_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

# Variance and standard deviation of contrast
input1_file = open("/results/Var_W_pos.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/Var_W_neg.csv")
input2_reader = csv.reader(input2_file)
output1_file = open("/results/Var_Contrast.csv", "wb")
output1_writer = csv.writer(output1_file)
output2_file = open("/results/StD_Contrast.csv", "wb")
output2_writer = csv.writer(output2_file)
var_contrast_temp = []
std_contrast_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null":
            var_contrast_temp.append(float(row1[i])+float(row2[i]))
            std_contrast_temp.append(math.sqrt(float(row1[i])+float(row2[i])))
        else:
            var_contrast_temp.append("Null")
            std_contrast_temp.append("Null")
    output1_writer.writerow(var_contrast_temp)
    output2_writer.writerow(std_contrast_temp)
    var_contrast_temp = []
    std_contrast_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output1_file
del output1_writer
del output2_file
del output2_writer

# Studentized contrast
input1_file = open("/results/Contrast.csv")
input1_reader = csv.reader(input1_file)
input2_file = open("/results/StD_Contrast.csv")
input2_reader = csv.reader(input2_file)
output_file = open("/results/Contrast_Studentized.csv", "wb")
output_writer = csv.writer(output_file)
contrast_stu_temp = []
for row1, row2 in itertools.izip(input1_reader, input2_reader):
    for i in range(num_fac):
        if row1[i] != "Null" and row2[i] != "Null" and float(row2[i]) != 0:
            contrast_stu_temp.append(float(row1[i])/float(row2[i]))
        else:
            contrast_stu_temp.append("Null")
    output_writer.writerow(contrast_stu_temp)
    contrast_stu_temp = []
del input1_file
del input1_reader
del input2_file
del input2_reader
del output_file
del output_writer
