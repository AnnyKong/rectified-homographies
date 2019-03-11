# based on ml-5.py
# for complete/ borderline 3.4-3.75
# take out shearing from rotation matrix
import peek
# import cv2
import math
import json
import sys

TRAIN_N = 10075 # 10075-complete 18773-incomplete

ROTATION_BORDER = 5 # < border is good
PROJECTIVE_BORDER = 3.5 # >= border is good
PROJECTIVE_BORDER_UP = 3.75 # >= 3.75 is good
PROJECTIVE_BORDER_DOWN = 3.4 # < 3.4 is bad


TRAIN_PATH = "../processed_dataset/cmp/complete/"
path_len = len(TRAIN_PATH)
img_paths = []
errors = set()

LOG = False
SHOW_RESULT = True

def show_progress(n, i, type):
	count = int(i / n * 100)
	sys.stdout.write('\r')
	sys.stdout.write("[%s][%-20s] %d%%" % (str(type), '='*int(count/5), 1*count))
	sys.stdout.flush()

def getThetas():
	global img_paths 
	global TRAIN_N
	global errors

	rotation_thetas_r2 = {}
	rotation_thetas_r1 = {}

	img_paths = peek.getAllImgPaths(TRAIN_PATH)
	if len(img_paths) < TRAIN_N:
		TRAIN_N = len(img_paths)

	n = TRAIN_N 
	for i in range(n):
		show_progress(n, i, "Rotation")
		img_path = img_paths[i]
		try:
			Hl, Hr = peek.readmat(img_path, i)
		except:
			errors.add(int(img_path[path_len:-5]))
			continue
		## derive rotation angle from homography
		theta = - math.atan2(Hl[0,1], Hl[0,0]) * 180 / math.pi
		
		theta_abs_r2 = round(abs(theta),2)
		theta_abs_r1 = round(abs(theta),1)

		rotation_thetas_r2[i] = (img_path[path_len:-5], theta_abs_r2)
		rotation_thetas_r1[i] = (img_path[path_len:-5], theta_abs_r1)

		if LOG: 
			print("[Rotation][" + \
				str(i) + ":" + img_path + "] " + \
				str(theta_abs_r2) + " degree(s)")

	write_file_r2 = 'json/rotation_thetas_r2_' + str(TRAIN_N) + '.json'
	with open(write_file_r2, 'w') as outfile:
		json.dump(rotation_thetas_r2, outfile)

	write_file_r1 = 'json/rotation_thetas_r1_' + str(TRAIN_N) + '.json'
	with open(write_file_r1, 'w') as outfile:
		json.dump(rotation_thetas_r1, outfile)
	
	return rotation_thetas_r2

def getProjComponents():
	global errors		
	proj_components_r2 = {}
	proj_components_r1 = {}
	
	n = TRAIN_N 
	for i in range(n):
		show_progress(n, i , "Projective")
		img_path = img_paths[i]
		try:
			Hl, Hr = peek.readmat(img_path, i)
		except:
			errors.add(int(img_path[path_len:-5]))
			continue
		## derive rotation angle from homography
		p1_abs = abs(Hl[0,2])
		p2_abs = abs(Hl[1,2])
		p3_abs = abs(Hl[2,2])
		# close = abs((p1_abs - 0) + (p2_abs - 0) + (p3_abs - 1))
		s = 1 / p3_abs
		close = abs(s*(p1_abs - 0) + s*(p2_abs - 0))

		close_log_r2 = round(-math.log10(close),2)
		close_log_r1 = round(-math.log10(close), 1)

		proj_components_r2[i] = (img_path[path_len:-5], close_log_r2)
		proj_components_r1[i] = (img_path[path_len:-5], close_log_r1)

		if LOG: 
			print("[Projective][" + \
				str(i) + ":" + img_path + "]" + \
				str(close_log_r2))

	write_file_r2 = 'json/proj_components_r2_' + str(TRAIN_N) + '.json'
	with open(write_file_r2, 'w') as outfile:
		json.dump(proj_components_r2, outfile)

	write_file_r1 = 'json/proj_components_r1_' + str(TRAIN_N) + '.json'
	with open(write_file_r1, 'w') as outfile:
		json.dump(proj_components_r1, outfile)
	
	return proj_components_r2

def ml_rotation():
	rotation_thetas = getThetas()
	good = 0
	bad = 0
	goods = []
	bads = []
	for i in rotation_thetas.keys():
		(img, theta) = rotation_thetas[i]
		if theta < ROTATION_BORDER:
			good += 1
			goods.append(int(img))
		else:
			bad += 1
			bads.append(int(img))

	if LOG:
		print("[Rotation] good=" + str(good) + \
			" bad=" + str(bad) + ",\n" + \
			"goods=" + str(goods) + "\n" + \
			"bads=" + str(bads) + "\n" + \
			"goods/all =" + str(good/(good+bad)))
	return goods, bads


def ml_projective():
	proj_components = getProjComponents()
	good = 0
	bad = 0
	border = 0
	border_good = 0
	border_bad = 0
	goods = []
	bads = []
	borders = []
	border_goods = []
	border_bads = []
	for i in proj_components.keys():
		(img, close_log) = proj_components[i]
		#  >= PROJECTIVE_BORDER_UP -> good
		#  < PROJECTIVE_BORDER_DOWN -> bad
		#  o/w -> borders
		# 		- >= PROJECTIVE_BORDER -> border_good
		# 		- <	PROJECTIVE_BORDER -> border_bad
		if close_log >= PROJECTIVE_BORDER_UP:
			good += 1
			goods.append(int(img))
		elif close_log < PROJECTIVE_BORDER_DOWN:
			bad += 1
			bads.append(int(img))
		else:
			border += 1
			borders.append(int(img))
			if close_log >= PROJECTIVE_BORDER:
				border_good += 1
				border_goods.append(int(img))
			else:
				border_bad += 1
				border_bads.append(int(img))


	if LOG: 
		print("[Projective] good=" + str(good) + \
			" bad=" + str(bad) + \
			" border=" + str(border)+ \
			" (border_good=" + str(border_good)+ \
			" border_bad=" + str(border_bad)+ ")" +",\n" + \
			"goods=" + str(goods) + "\n" + \
			"bads=" + str(bads) + "\n" + \
			"borders=" + str(borders) + "\n" + \
			"(border_goods=" + str(border_goods) + "\n" + \
			"border_bads=" + str(border_bads) + ")" +"\n" + \
			"goods/all =" + str(good/(good+bad+border)))
	return goods,bads,borders,border_goods,border_bads

def intersect(rotation_goods, proj_goods):
	intersection_set = rotation_goods.intersection(proj_goods)
	return intersection_set

def union(rotation_bads, proj_bads):
	union_set = rotation_bads.union(proj_bads)
	return union_set

def ml():
	rotationGB = ml_rotation()
	projectiveGB = ml_projective()

	rotation_goods = set(rotationGB[0])
	proj_goods = set(projectiveGB[0])
	total_goods = intersect(rotation_goods, proj_goods)

	rotation_bads = set(rotationGB[1])
	proj_bads = set(projectiveGB[1])
	total_bads = union(rotation_bads, proj_bads)

	projective_borders = set(projectiveGB[2])
	total_borders = intersect(rotation_goods, projective_borders)

	projective_border_goods = set(projectiveGB[3])
	total_border_goods = intersect(rotation_goods, projective_border_goods)

	projective_border_bads = set(projectiveGB[4])
	total_border_bads = intersect(rotation_goods, projective_border_bads)

	if SHOW_RESULT: 
		sys.stdout.write('\r')
		print(TRAIN_PATH)
		print("[Rot+Proj] result goods=" + str(sorted(list(total_goods))))
		# print("[Rot+Proj] result bads=" + str(sorted(list(total_bads))))
		print("[Rot+Proj] result borders=" + str(sorted(list(total_borders))))
		print("[Rot+Proj] result border_goods=" + str(sorted(list(total_border_goods))))
		# print("[Rot+Proj] result border_bads=" + str(sorted(list(total_border_bads))))
		print("[Rot+Proj] Results:\n" + \
			" result good=" + str(len(total_goods)) + "\n" + \
			" result bad=" + str(len(total_bads)) + "\n" + \
			" result border=" + str(len(total_borders)) + "\n" + \
			" result border_good=" + str(len(total_border_goods)) + "\n" + \
			" result border_bad=" + str(len(total_border_bads)) + "\n" + \
			"goods/all =" + str(len(total_goods)/(len(total_goods)+len(total_bads)+len(total_borders))))
		print("[EXTRA] errors = " + str(sorted(list(errors))))

		with open("complete-results.txt", 'w') as f:
			f.write("[Rot+Proj] result goods=" + str(sorted(list(total_goods))))
			f.write("[Rot+Proj] result bads=" + str(sorted(list(total_bads))))
			f.write("[Rot+Proj] result borders=" + str(sorted(list(total_borders))))
			f.write("[Rot+Proj] result border_goods=" + str(sorted(list(total_border_goods))))
			f.write("[Rot+Proj] result border_bads=" + str(sorted(list(total_border_bads))))
			f.write("[Rot+Proj] Results:\n" + \
					" result good=" + str(len(total_goods)) + "\n" + \
					" result bad=" + str(len(total_bads)) + "\n" + \
					" result border=" + str(len(total_borders)) + "\n" + \
					" result border_good=" + str(len(total_border_goods)) + "\n" + \
					" result border_bad=" + str(len(total_border_bads)) + "\n" + \
					"goods/all =" + str(len(total_goods)/(len(total_goods)+len(total_bads)+len(total_borders))))
			f.write("[EXTRA] errors = " + str(sorted(list(errors))))


if __name__ == '__main__':
	ml()