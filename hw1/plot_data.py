import matplotlib.pyplot as plt
import numpy as np
import math

import csv

trace_names = []

mpki_hashed_perceptron = []

mpki_oracle = []

with open("out/hashed_perceptron/out.csv") as f:
    for row in csv.reader(f):
        trace_names.append(row[0])
        mpki_hashed_perceptron.append(float(row[1]))

with open("out/oracle/out.csv") as f:
    for row in csv.reader(f):
        mpki_oracle.append(float(row[1]))

N = len(trace_names)
ind = np.arange(N)
width = 0.3

################################
# CONDITIONAL MPKI
fig, (mpki) = plt.subplots(ncols=1, figsize=(20, 8), sharex=True, sharey=False)

bar1 = mpki.bar(ind - width / 2, mpki_hashed_perceptron, width, color="r")
bar2 = mpki.bar(ind + width / 2, mpki_oracle, width, color="g")

mpki.set_ylabel("MPKI")
mpki.set_xticks(ind)
mpki.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
mpki.legend((bar1[0], bar2[0]), ("hashed perceptron", "oracle"))

fig.savefig("out/mpki.png", dpi=400)
