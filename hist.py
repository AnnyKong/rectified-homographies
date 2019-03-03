# hist.py
# This file is served to produce a table/histogram 
# of specified decomposition (rotation, projective, i.e.)

import json
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate
from collections import OrderedDict
import sys


N = 10
FILENAME_ROTATION = 'rotation_thetas_r1.json'
FILENAME_PROJECTIVE = 'proj_components_r1.json'
WRITE_FILENAME = 'table.txt'
SHOW_TABLE = True
SHOW_HIST = True

def main():
	if len(sys.argv) != 2:
		print("  Please follow the format: python3 hist.py <r/p>")
		exit(0)
	arg = sys.argv[1]

	# open json file
	filename = ""
	if arg.startswith('r'):
		filename = FILENAME_ROTATION
	else:
		filename = FILENAME_PROJECTIVE

	data = open_json(filename)

	# count subjects, subject->count
	count = count_subjects(data)

	# sort by frequency
	count = sort_count(count)

	if SHOW_HIST:
		plot_histogram(count)

	if SHOW_TABLE:
		show_table(count)

	print(filename)

def sort_count(count):
	count = OrderedDict(sorted(count.items(), key=lambda x: float(x[0]), reverse=True))
	return count

def show_table(count):
	# show table
	line = [[k, v] for (k,v) in count.items()]
	header = ['Subject', 'Frequency']
	print('>>>>>>[Table] Show start>>>>>>>')
	print()
	print(tabulate(line, headers = header))
	print()
	print(">>>>>>[Table] Show end>>>>>>>")
	print()
	print(">>>>>>[Table] Write start>>>>>>>")
	with open(WRITE_FILENAME, 'w') as f:
		f.write (str(tabulate(line, headers = header)))
		print('write success!  open table.txt to view')
	print(">>>>>>[Table] Write end>>>>>>>")
	print()

def plot_histogram(count):
	# plot hist
	plt.figure(figsize=(N * 3, 3))
	plt.bar(count.keys(), count.values(), color='g')

	plt.savefig('hist.png')
	plt.close()
	print('>>>>>>[IMG] Histogram created>>>>>>>')
	print('[IMG] view it: open hist.png ')
	print()

def count_subjects(data):
	#index->...
	#       ...
	#       subjects:...
	#				 ...
	subjects_count = {}
	for i in data.keys():
		(img, subject) = data[i]
		if subject not in subjects_count.keys():
			subjects_count[subject] = 0
		subjects_count[subject] += 1
	return subjects_count

def take_first_N(count, n):
	return {k: count[k] for k in list(count)[:n]}

def open_json(filename):
	with open(filename) as f:
		return json.load(f)

if __name__ == '__main__':
	main()
