# scatter-2.py
# This file is served to produce a scatter plot
# of specified decomposition (rotation and projective)
# for complete/

import json
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

FILENAME_ROTATION_GOOD = 'json/rotation_thetas_r2_good.json'
FILENAME_PROJECTIVE_GOOD = 'json/proj_components_r2_good.json'
FILENAME_ROTATION_BAD = 'json/rotation_thetas_r2_bad.json'
FILENAME_PROJECTIVE_BAD = 'json/proj_components_r2_bad.json'
FILENAME_ROTATION_BORDER = 'json/rotation_thetas_r2_border.json'
FILENAME_PROJECTIVE_BORDER = 'json/proj_components_r2_border.json'

FILENAME_ROTATION = 'json/rotation_thetas_r2_10075'
FILENAME_PROJECTIVE = 'json/proj_components_r2_10075.json'

WRITE_FILENAME = 'scatter.png'
SHOW_TABLE = True
SHOW_HIST = True

def main():
	# open json file
	data_good = parse_json(FILENAME_ROTATION_GOOD, FILENAME_PROJECTIVE_GOOD)
	data_bad = parse_json(FILENAME_ROTATION_BAD, FILENAME_PROJECTIVE_BAD)
	data_border = parse_json(FILENAME_ROTATION_BORDER, FILENAME_PROJECTIVE_BORDER)

	data = parse_json(FILENAME_ROTATION, FILENAME_PROJECTIVE)

	if SHOW_HIST:
		plot_histogram(data)
	# if SHOW_TABLE:
	# 	show_table(count)

def parse_json(fn1, fn2):
	rot_data = open_json(fn1)
	proj_data = open_json(fn2)
	data = combine(rot_data, proj_data)
	return data

def combine(rot_data, proj_data):
	data = {}
	for i in rot_data.keys():
		(rot_img, rot_val) = rot_data[i]
		(proj_img, proj_val) = proj_data[i]
		data[i] = (rot_img, rot_val, proj_val)
	return data

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

def plot_xy(ax, data, c, l):
	xs = [data[i][1] for i in data.keys()] #rot
	ys = [data[i][2] for i in data.keys()] #proj
	ax.scatter(xs, ys, color=c, label=l) #

def plot_histogram(data):
	# plot scatter
	fig, ax = plt.subplots()
	plot_xy(ax, data, 'green', 'data')

	legend = ax.legend(loc='upper center', shadow=False, fontsize='x-large')
	legend.get_frame().set_facecolor('white')
	ax.set_xlabel(r'Rotation indicator', fontsize=15)
	ax.set_ylabel(r'Projective indicator', fontsize=15)
	ax.set_title('Rotation v.s. Projective')

	ax.grid(True)
	fig.tight_layout()
	plt.show()

	plt.savefig(WRITE_FILENAME)
	plt.close()
	print('>>>>>>[IMG] Histogram created>>>>>>>')
	print('[IMG] view it: open ' + WRITE_FILENAME)
	print()

def plot_histogram(data_good, data_bad, data_border):
	# plot scatter
	fig, ax = plt.subplots()
	plot_xy(ax, data_good, 'green', 'good')
	plot_xy(ax, data_bad, 'red', 'bad')
	plot_xy(ax, data_border, 'blue', 'border')

	legend = ax.legend(loc='upper center', shadow=False, fontsize='x-large')
	legend.get_frame().set_facecolor('white')
	ax.set_xlabel(r'Rotation indicator', fontsize=15)
	ax.set_ylabel(r'Projective indicator', fontsize=15)
	ax.set_title('Rotation v.s. Projective')

	ax.grid(True)
	fig.tight_layout()
	plt.show()

	plt.savefig(WRITE_FILENAME)
	plt.close()
	print('>>>>>>[IMG] Histogram created>>>>>>>')
	print('[IMG] view it: open ' + WRITE_FILENAME)
	print()

def open_json(filename):
	with open(filename) as f:
		return json.load(f)

if __name__ == '__main__':
	main()
