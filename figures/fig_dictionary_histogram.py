#!/usr/bin/env python

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches
import subprocess

# copy-paste data from spreadsheet
data = """
c432    1.000000000 0.142857143 0.106238698 0.040687161 0.016274864
c499    1.000000000 0.031250000 0.026864035 0.015899123 0.003152412
c1355   1.000000000 0.031250000 0.028878891 0.014196255 0.000060798
c1908   1.000000000 0.040000000 0.032249135 0.020761246 0.006435986
c2670   1.000000000 0.016666667 0.012925852 0.005911824 0.001102204
c3540   1.000000000 0.045454545 0.035986265 0.012953016 0.002277827
c5315   1.000000000 0.009090909 0.008474719 0.003502997 0.000409386
c7552   1.000000000 0.010526316 0.009606929 0.003970686 0.000913677
b12 1.000000000 0.008403361 0.006551773 0.002385700 0.001099380
b14_opt 1.000000000 0.004081633 0.003456831 0.001219452 0.000499231
b14 1.000000000 0.004081633 0.003287831 0.000934007 0.000246352
b15 1.000000000 0.002227171 0.001655805 0.000527446 0.000202434
b17_opt 1.000000000 0.000692521 0.000522533 0.000161452 0.000086318
b18_opt 1.000000000 0.000303767 0.000247291 0.000088780 0.000024158
b22 1.000000000 0.001321004 0.001038543 0.000274056 0.000068370
L2B 1.000000000 0.000425894 0.000369164 0.000175679 0.000048559
NCU 1.000000000 0.000062422 0.000049256 0.000036828 0.000020028
epflDiv 1.000000000 0.007812500 0.002936137 0.002204044 0.000034948
epflMult    1.000000000 0.007812500 0.004847543 0.002629355 0.000000773
epflSqrt    1.000000000 0.015625000 0.007311679 0.003572941 0.000001904
epflSquare  1.000000000 0.007936508 0.005191311 0.004380263 0.000001118
epflMemCtrl 1.000000000 0.000813008 0.000453632 0.000138034 0.000033052
"""

names = []
full_resp = []
pass_fail = []
pass_fail_tf = []
pass_fail_trax_nh = []
pass_fail_trax = []
log_fix_multiplier = 10000000
for line in data.strip().split("\n"):
    items = line.split()
    names.append(items[0])
    full_resp.append(log_fix_multiplier * float(items[1]))
    pass_fail.append(log_fix_multiplier * float(items[2]))
    pass_fail_tf.append(log_fix_multiplier * float(items[3]))
    pass_fail_trax_nh.append(log_fix_multiplier * float(items[4]))
    pass_fail_trax.append(log_fix_multiplier * float(items[5]))
N = len(names)
print "N: %d" % N

# weird log scaling to stop freaking out the set_yscale("log")
full_resp = np.log(full_resp) / np.log(log_fix_multiplier)
pass_fail = np.log(pass_fail) / np.log(log_fix_multiplier)
pass_fail_tf = np.log(pass_fail_tf) / np.log(log_fix_multiplier)
pass_fail_trax_nh = np.log(pass_fail_trax_nh) / np.log(log_fix_multiplier)
pass_fail_trax = np.log(pass_fail_trax) / np.log(log_fix_multiplier)

ind = np.arange(N) # x locations for the groups
width = (1/6.0) # width of the bars
offset = width

print "ind:", ind

blue="#709ECF"
red="#FF8F8F"
violet="#AC88B2"
green="#8AE133"
yellow="#FFFD98"
edgecolor="#000000"

fig = plt.figure(figsize=(12,6))
ax1 = fig.add_axes([0.1, 0.3, 0.88, 0.65])
ax1.set_axisbelow(True)
ax1.yaxis.grid(True, linestyle='-', which='major', color='black')
ax1.set_ylabel('Relative size', weight='bold')
ax1.set_xlabel('Benchmark circuit', weight='bold')
ax1.get_xaxis().tick_bottom()
plt.yticks((1, (6/7.0), (5/7.0), (4/7.0), (3/7.0), (2/7.0), (1/7.0), 0.0), ("1", "0.1", "0.01", "0.001", "0.0001", "0.00001", "0.000001", "0.0000001"), weight='bold')
plt.xticks(offset + ind + 2 * width, names, weight='bold')

# plot the bars
rects1 = ax1.bar(offset + ind            , full_resp,           width, edgecolor=edgecolor, color=blue)
rects2 = ax1.bar(offset + ind + 1 * width, pass_fail,           width, edgecolor=edgecolor, color=red)
rects3 = ax1.bar(offset + ind + 2 * width, pass_fail_tf,        width, edgecolor=edgecolor, color=violet)
rects4 = ax1.bar(offset + ind + 3 * width, pass_fail_trax_nh,   width, edgecolor=edgecolor, color=green)
rects5 = ax1.bar(offset + ind + 4 * width, pass_fail_trax,      width, edgecolor=edgecolor, color=yellow)

ax1.set_ylim([0.000001, 1.0])
# tweak the ends of the x-axis to give us a little padding on the left and right (so bars don't touch the plot area bounding box)
ax1.set_xlim([0.0, N])

ax1.set_xticklabels(ax1.xaxis.get_majorticklabels(), rotation=90)

plt.figlegend(
        (matplotlib.patches.Patch(fc=blue, edgecolor=edgecolor), matplotlib.patches.Patch(fc=red, edgecolor=edgecolor), matplotlib.patches.Patch(fc=violet, edgecolor=edgecolor), matplotlib.patches.Patch(fc=green, edgecolor=edgecolor), matplotlib.patches.Patch(fc=yellow, edgecolor=edgecolor)),
        ("1. Full-response", "2. Pass/fail", "3. Pass/fail, collapsed, TF", "4. Pass/fail, collapsed, UTF", "5. Pass/fail, collapsed, TRAX"),
        loc='lower center',
        ncol=5,
        frameon=False,
    )

# save as svg
plt.savefig("fig_dictionary_histogram.svg", transparent=True)

make_png = False
if make_png:
    # Rendering to PDF happens as part of the paper build script, but in case you want to do this standalone:
    subprocess.call(["inkscape", "-z", "-e", "fig_dictionary_histogram.png", "-D", "-f", "fig_dictionary_histogram.svg", "-w", "2000", "-y", "1"])

    # open png file
    subprocess.call(["xdg-open", "fig_dictionary_histogram.png"])



