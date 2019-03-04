# peek.py
# This file is served as utilities to 
# read homography matrix of a specified image

import scipy.io
import sys
import glob
import os
import pdb

FOLDER_PATH = '../processed_dataset/cmp/complete/'
path_len = len(FOLDER_PATH)
suffix = -5

# read mat
def readmat(img_path, i):
	x = scipy.io.loadmat(img_path + 'rectification_mats.mat')
	Hl = x['tl']
	Hr = x['tr']
	return Hl, Hr

def printmat(img_path, i):
	Hl, Hr = readmat(img_path, i)
	print(">>> [" + str(i) + "] Peek " + img_path + " >>>")
	print("> Left Homography:\n" + str(Hl))
	print("> Right Homography:\n" + str(Hr))
	print()

def sortKeyFunc(s):
	global path_len
	# from pdb import set_trace as st
	# st()
	return int(s[path_len:suffix])

def getAllImgPaths(path):
	global path_len
	if path is None:
		path = FOLDER_PATH
	imgs = glob.glob(path + "*.jpg/")
	path_len = len(path)
	suffix = -5
	imgs.sort(key=sortKeyFunc)
	return imgs

def getAllImgs(type): # type = bad/good/borderline
	global path_len
	path_dir = "classified_vis/"
	imgs = glob.glob(path_dir + type + "/*.png")
	path_len = len(path_dir) + len(type) + 1
	suffix = - len(".png")
	imgs.sort(key=sortKeyFunc)
	imgs = [imgs[i][path_len:suffix] for i in range(len(imgs))]
	return imgs

def peek():
	imgs = getAllImgPaths()
	# parse arg
	if len(sys.argv) != 2:
		print("  Please follow the format: python3 peek.py <N or img(.jpg)>")
		exit(0)
	arg = sys.argv[1]
	N = 0
	img_path = ""
	if arg.endswith(".jpg"):
		img_path = FOLDER_PATH + arg + '/'
		printmat(img_path)
	else:
		N = int(arg)
		for i in range(min(N, len(imgs))):
			printmat(imgs[i], i)

if __name__ == '__main__':
	peek()

