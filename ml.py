# ml.py
# This file is used to train homography matrices 
# to learn to distinguish good and bad images

import peek
import cv2
import math
import json

trainN = 100
validN = 40
testN = 100

ROTATION_BORDER = 5
PROJECTIVE_BORDER = 1.1

LOG = True
SHOW_RESULT = True

def getThetas():
	rotation_thetas = {}
	for i in range(trainN):
		img_paths = peek.getAllImgPaths()
		Hl, Hr = peek.readmat(img_paths[i], i)
		## derive rotation angle from homography
		theta = - math.atan2(Hl[0,1], Hl[0,0]) * 180 / math.pi
		theta_abs = round(abs(theta),2)
		
		rotation_thetas[i] = theta_abs
		if LOG: 
			print("[Rotation][" + \
				str(i) + ":" + img_paths[i] + "] " + \
				str(theta_abs) + " degree(s)")
	with open('rotation_thetas_r2.json', 'w') as outfile:
		json.dump(rotation_thetas, outfile)
	
	return rotation_thetas

def getProjComponents():
	proj_components = {}
	for i in range(trainN):
		img_paths = peek.getAllImgPaths()
		Hl, Hr = peek.readmat(img_paths[i], i)
		## derive rotation angle from homography
		p1_abs = abs(Hl[0,2])
		p2_abs = abs(Hl[1,2])
		p3_abs = abs(Hl[2,2])
		# close = abs((p1_abs - 0) + (p2_abs - 0) + (p3_abs - 1))
		s = 1 / p3_abs
		close = abs(s*(p1_abs - 0) + s*(p2_abs - 0))

		close_log = round(-math.log10(close),2)
		proj_components[i] = close_log
		if LOG: 
			print("[Projective][" + \
				str(i) + ":" + img_paths[i] + "]" + \
				str(close_log))

	with open('proj_components_r2.json', 'w') as outfile:
		json.dump(proj_components, outfile)
	
	return proj_components

def ml_rotation():
	rotation_thetas = getThetas()
	good = 0
	bad = 0
	goods = []
	bads = []
	for i in rotation_thetas.keys():
		if rotation_thetas[i] < ROTATION_BORDER:
			good += 1
			goods.append(i)
		else:
			bad += 1
			bads.append(i)

	if SHOW_RESULT:
		print("[Rotation] good=" + str(good) + \
			" bad=" + str(bad) + ",\ngoods=" + str(goods) +\
			"\nbads=" + str(bads) + "\ngoods/all =" + \
			str(good/(good+bad)))


def ml_projective():
	proj_components = getProjComponents()
	good = 0
	bad = 0
	goods = []
	bads = []
	for i in proj_components.keys():
		close_log = proj_components[i]
		if close_log >= PROJECTIVE_BORDER:
			good += 1
			goods.append(i)
		else:
			bad += 1
			bads.append(i)

	if SHOW_RESULT: 
		print("[Projective] good=" + str(good) + \
			" bad=" + str(bad) + ",\ngoods=" + str(goods) +\
			" \nbads=" + str(bads) + "\ngoods/all =" + \
			str(good/(good+bad)))

def ml():
	ml_rotation()
	ml_projective()

if __name__ == '__main__':
	ml()