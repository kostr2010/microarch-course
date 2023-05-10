import matplotlib.pyplot as plt
import numpy as np
import math

import csv

trace_names = []

ipcs_lru = []
l2_total_lru = []
l2_hit_lru = []
l2_miss_lru = []
l1d_total_lru = []
l1d_hit_lru = []
l1d_miss_lru = []
stlb_total_lru = []
stlb_hit_lru = []
stlb_miss_lru = []
dtlb_total_lru = []
dtlb_hit_lru = []
dtlb_miss_lru = []
llc_total_lru = []
llc_hit_lru = []
llc_miss_lru = []

ipcs_lfu = []
l2_total_lfu = []
l2_hit_lfu = []
l2_miss_lfu = []
l1d_total_lfu = []
l1d_hit_lfu = []
l1d_miss_lfu = []
stlb_total_lfu = []
stlb_hit_lfu = []
stlb_miss_lfu = []
dtlb_total_lfu = []
dtlb_hit_lfu = []
dtlb_miss_lfu = []
llc_total_lfu = []
llc_hit_lfu = []
llc_miss_lfu = []

plot_offset = 0.2

with open("out/lru/out.csv") as f:
    for row in csv.reader(f):
        trace_names.append(row[0])
        ipcs_lru.append(float(row[1]))
        l2_total_lru.append(int(row[2]))
        l2_hit_lru.append(int(row[3]))
        l2_miss_lru.append(int(row[4]))
        l1d_total_lru.append(int(row[5]))
        l1d_hit_lru.append(int(row[6]))
        l1d_miss_lru.append(int(row[7]))
        stlb_total_lru.append(int(row[8]))
        stlb_hit_lru.append(int(row[9]))
        stlb_miss_lru.append(int(row[10]))
        dtlb_total_lru.append(int(row[11]))
        dtlb_hit_lru.append(int(row[12]))
        dtlb_miss_lru.append(int(row[13]))
        llc_total_lru.append(int(row[14]))
        llc_hit_lru.append(int(row[15]))
        llc_miss_lru.append(int(row[16]))

with open("out/lfu/out.csv") as f:
    for row in csv.reader(f):
        ipcs_lfu.append(float(row[1]))
        l2_total_lfu.append(int(row[2]))
        l2_hit_lfu.append(int(row[3]))
        l2_miss_lfu.append(int(row[4]))
        l1d_total_lfu.append(int(row[5]))
        l1d_hit_lfu.append(int(row[6]))
        l1d_miss_lfu.append(int(row[7]))
        stlb_total_lfu.append(int(row[8]))
        stlb_hit_lfu.append(int(row[9]))
        stlb_miss_lfu.append(int(row[10]))
        dtlb_total_lfu.append(int(row[11]))
        dtlb_hit_lfu.append(int(row[12]))
        dtlb_miss_lfu.append(int(row[13]))
        llc_total_lfu.append(int(row[14]))
        llc_hit_lfu.append(int(row[15]))
        llc_miss_lfu.append(int(row[16]))

N = len(trace_names)
ind = np.arange(N)
width = 0.3

################################
# IPC
fig, (ipc) = plt.subplots(nrows=1, figsize=(20, 8), sharex=True, sharey=False)
fig.tight_layout()
bar1 = ipc.bar(ind - width / 2, ipcs_lru, width, color="r")
ipc.bar_label(
    bar1,
    ["d={0:.6f}".format(ipcs_lru[i] - ipcs_lfu[i]) for i in range(N)],
)
bar2 = ipc.bar(ind + width / 2, ipcs_lfu, width, color="g")

ipc.set_ylabel("IPC")
ipc.set_xticks(ind)
ipc.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
ipc.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/ipc.png", dpi=400)

################################
# L2 ACCESS TOTAL, HIT%
fig, (l2_total, l2_hit_miss) = plt.subplots(
    nrows=2, figsize=(20, 15), sharex=True, sharey=False
)
fig.tight_layout()

bar1 = l2_total.bar(
    ind - width / 2, [math.log(i + 1, 10) for i in l2_total_lru], width, color="r"
)
l2_total.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            math.log(l2_total_lru[i] + 1, 10) - math.log(l2_total_lfu[i] + 1, 10)
        )
        for i in range(N)
    ],
)
bar2 = l2_total.bar(
    ind + width / 2, [math.log(i + 1, 10) for i in l2_total_lfu], width, color="g"
)

l2_total.set_ylabel("L2 TOTAL ACCESS, log")
l2_total.set_xticks(ind)
l2_total.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
l2_total.legend((bar1[0], bar2[0]), ("lru", "lfu"))

bar1 = l2_hit_miss.bar(
    ind - width / 2,
    [l2_hit_lru[i] / (1 + l2_total_lru[i]) for i in range(N)],
    width,
    color="r",
)
l2_hit_miss.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            l2_hit_lru[i] / (1 + l2_total_lru[i])
            - l2_hit_lfu[i] / (1 + l2_total_lfu[i])
        )
        for i in range(N)
    ],
)
bar2 = l2_hit_miss.bar(
    ind + width / 2,
    [l2_hit_lfu[i] / (1 + l2_total_lfu[i]) for i in range(N)],
    width,
    color="g",
)

l2_hit_miss.set_ylabel("HIT%")
l2_hit_miss.set_xticks(ind)
l2_hit_miss.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
l2_hit_miss.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/l2_statistics.png", dpi=400)

################################
# L1D ACCESS TOTAL, HIT%
fig, (l1d_total, l1d_hit_miss) = plt.subplots(
    nrows=2, figsize=(20, 15), sharex=True, sharey=False
)
fig.tight_layout()
bar1 = l1d_total.bar(
    ind - width / 2, [math.log(i + 1, 10) for i in l1d_total_lru], width, color="r"
)
l1d_total.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            math.log(l1d_total_lru[i] + 1, 10) - math.log(l1d_total_lfu[i] + 1, 10)
        )
        for i in range(N)
    ],
)
bar2 = l1d_total.bar(
    ind + width / 2, [math.log(i + 1, 10) for i in l1d_total_lfu], width, color="g"
)

l1d_total.set_ylabel("L1D TOTAL ACCESS, log")
l1d_total.set_xticks(ind)
l1d_total.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
l1d_total.legend((bar1[0], bar2[0]), ("lru", "lfu"))

bar1 = l1d_hit_miss.bar(
    ind - width / 2,
    [l1d_hit_lru[i] / (1 + l1d_total_lru[i]) for i in range(N)],
    width,
    color="r",
)
l1d_hit_miss.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            l1d_hit_lru[i] / (1 + l1d_total_lru[i])
            - l1d_hit_lfu[i] / (1 + l1d_total_lfu[i])
        )
        for i in range(N)
    ],
)
bar2 = l1d_hit_miss.bar(
    ind + width / 2,
    [l1d_hit_lfu[i] / (1 + l1d_total_lfu[i]) for i in range(N)],
    width,
    color="g",
)

l1d_hit_miss.set_ylabel("HIT%")
l1d_hit_miss.set_xticks(ind)
l1d_hit_miss.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
l1d_hit_miss.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/l1d_statistics.png", dpi=400)

################################
# STLB ACCESS TOTAL, HIT%
fig, (stlb_total, stlb_hit_miss) = plt.subplots(
    nrows=2, figsize=(20, 15), sharex=True, sharey=False
)
fig.tight_layout()
bar1 = stlb_total.bar(
    ind - width / 2, [math.log(i + 1, 10) for i in stlb_total_lru], width, color="r"
)
stlb_total.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            math.log(stlb_total_lru[i] + 1, 10) - math.log(stlb_total_lfu[i] + 1, 10)
        )
        for i in range(N)
    ],
)
bar2 = stlb_total.bar(
    ind + width / 2, [math.log(i + 1, 10) for i in stlb_total_lfu], width, color="g"
)

stlb_total.set_ylabel("STLB TOTAL ACCESS, log")
stlb_total.set_xticks(ind)
stlb_total.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
stlb_total.legend((bar1[0], bar2[0]), ("lru", "lfu"))

bar1 = stlb_hit_miss.bar(
    ind - width / 2,
    [stlb_hit_lru[i] / (1 + stlb_total_lru[i]) for i in range(N)],
    width,
    color="r",
)
stlb_hit_miss.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            stlb_hit_lru[i] / (1 + stlb_total_lru[i])
            - stlb_hit_lfu[i] / (1 + stlb_total_lfu[i])
        )
        for i in range(N)
    ],
)
bar2 = stlb_hit_miss.bar(
    ind + width / 2,
    [stlb_hit_lfu[i] / (1 + stlb_total_lfu[i]) for i in range(N)],
    width,
    color="g",
)

stlb_hit_miss.set_ylabel("HIT%")
stlb_hit_miss.set_xticks(ind)
stlb_hit_miss.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
stlb_hit_miss.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/stlb_statistics.png", dpi=400)

################################
# DTLB ACCESS TOTAL, HIT%
fig, (dtlb_total, dtlb_hit_miss) = plt.subplots(
    nrows=2, figsize=(20, 15), sharex=True, sharey=False
)
fig.tight_layout()
bar1 = dtlb_total.bar(
    ind - width / 2, [math.log(i + 1, 10) for i in dtlb_total_lru], width, color="r"
)
dtlb_total.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            math.log(dtlb_total_lru[i] + 1, 10) - math.log(dtlb_total_lfu[i] + 1, 10)
        )
        for i in range(N)
    ],
)
bar2 = dtlb_total.bar(
    ind + width / 2, [math.log(i + 1, 10) for i in dtlb_total_lfu], width, color="g"
)

dtlb_total.set_ylabel("DTLB TOTAL ACCESS, log")
dtlb_total.set_xticks(ind)
dtlb_total.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
dtlb_total.legend((bar1[0], bar2[0]), ("lru", "lfu"))

bar1 = dtlb_hit_miss.bar(
    ind - width / 2,
    [dtlb_hit_lru[i] / (1 + dtlb_total_lru[i]) for i in range(N)],
    width,
    color="r",
)
dtlb_hit_miss.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            dtlb_hit_lru[i] / (1 + dtlb_total_lru[i])
            - dtlb_hit_lfu[i] / (1 + dtlb_total_lfu[i])
        )
        for i in range(N)
    ],
)
bar2 = dtlb_hit_miss.bar(
    ind + width / 2,
    [dtlb_hit_lfu[i] / (1 + dtlb_total_lfu[i]) for i in range(N)],
    width,
    color="g",
)

dtlb_hit_miss.set_ylabel("HIT%")
dtlb_hit_miss.set_xticks(ind)
dtlb_hit_miss.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
dtlb_hit_miss.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/dtlb_statistics.png", dpi=400)

################################
# LLC ACCESS TOTAL, HIT%
fig, (llc_total, llc_hit_miss) = plt.subplots(
    nrows=2, figsize=(20, 15), sharex=True, sharey=False
)
fig.tight_layout()
bar1 = llc_total.bar(
    ind - width / 2, [math.log(i + 1, 10) for i in llc_total_lru], width, color="r"
)
llc_total.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            math.log(llc_total_lru[i] + 1, 10) - math.log(llc_total_lfu[i] + 1, 10)
        )
        for i in range(N)
    ],
)
bar2 = llc_total.bar(
    ind + width / 2, [math.log(i + 1, 10) for i in llc_total_lfu], width, color="g"
)

llc_total.set_ylabel("LLC TOTAL ACCESS, log")
llc_total.set_xticks(ind)
llc_total.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
llc_total.legend((bar1[0], bar2[0]), ("lru", "lfu"))

bar1 = llc_hit_miss.bar(
    ind - width / 2,
    [llc_hit_lru[i] / (1 + llc_total_lru[i]) for i in range(N)],
    width,
    color="r",
)
llc_hit_miss.bar_label(
    bar1,
    [
        "d={0:.6f}".format(
            llc_hit_lru[i] / (1 + llc_total_lru[i])
            - llc_hit_lfu[i] / (1 + llc_total_lfu[i])
        )
        for i in range(N)
    ],
)
bar2 = llc_hit_miss.bar(
    ind + width / 2,
    [llc_hit_lfu[i] / (1 + llc_total_lfu[i]) for i in range(N)],
    width,
    color="g",
)

llc_hit_miss.set_ylabel("HIT%")
llc_hit_miss.set_xticks(ind)
llc_hit_miss.set_xticklabels([trace[:3] for trace in trace_names], rotation=45)
llc_hit_miss.legend((bar1[0], bar2[0]), ("lru", "lfu"))

fig.savefig("out/llc_statistics.png", dpi=400)
