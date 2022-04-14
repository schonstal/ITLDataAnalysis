#!/usr/bin/env python

import json
import numpy
import sys

dump_directory = "itl_2022-04-13-08"

argument_list = sys.argv[1:]
if len(argument_list) > 0:
    dump_directory = argument_list[0]

filename = "%s/leaderboard.json" % dump_directory

percentiles = [1, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 99]
entrants = json.load(open(filename))['entrants']
scores = [entrant['entrant_ranking_points'] for entrant in entrants if entrant['entrant_ranking_points'] != 0]

result = numpy.percentile(scores, percentiles, method='normal_unbiased')
std_deviation = numpy.nanstd(scores)

for index, percentile in enumerate(percentiles):
    print(f"Top {100 - percentile}%: {result[index]}")

print("Standard deviation:", std_deviation)
