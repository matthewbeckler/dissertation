#!/usr/bin/env python
#
# x = ceil(log2(Fmax))
# cycles = ceil(F / k) * Tmax * F
# area =
#   16 * Tmax
#   + 4
#   + 23 * k
#   + 40 * x * Mmax
#   + 2 * x
#   + 20 * Mmax
#   + 3

from math import ceil, log

# NCU - 211 tests, 67124 faults, 10 modules
# TRAX dictionary 21537
Tmax = 211
Fmax = 21537
Mmax = 10
x = ceil(log(Fmax, 2))

total = 500000000

for k in [1000, 5000, 10000]:

    cycles = ceil(Fmax / float(k)) * Tmax + Fmax

    area = (16 * Tmax) + 4 + (23 * k) + (40 * x * Mmax) + (2 * x) * (20 * Mmax) + 3

    area_overhead = 100 * (area / float(total))

    print "K = %d" % k
    print "  cycles:        ", cycles
    print "  area:          ", area
    print "  area overhead: ", area_overhead


