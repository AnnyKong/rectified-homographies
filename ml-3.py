# ml-3.py
# write all json files to json/
import peek
import cv2
import math
import json

TRAIN_N = 60 # <= 100
VALID_N = 40
TEST_N = 100

ROTATION_BORDER = 5 # < border is good
PROJECTIVE_BORDER = 3.5 # >= border is good

TRAIN_PATH = "complete/"
path_len = len(TRAIN_PATH)
TYPE = "border" # type = bad-17/good-73/border-10
USE_TYPE = False

LOG = True
SHOW_RESULT = True

def getImgPath(img_paths, img):
	return [img_paths[j] for j in range(len(img_paths)) if \
				img.find(img_paths[j][9:-5]) != -1][0]

def getThetas():
	rotation_thetas_r2 = {}
	rotation_thetas_r1 = {}
	img_paths = peek.getAllImgPaths(TRAIN_PATH)
	imgs = peek.getAllImgs(TYPE)

	if not USE_TYPE and len(img_paths) < TRAIN_N:
		print("img_paths != TRAIN_N")
		exit(0)

	n = len(imgs) if USE_TYPE else TRAIN_N 
	for i in range(n):
		img_path = getImgPath(img_paths, imgs[i]) if USE_TYPE else img_paths[i]

		Hl, Hr = peek.readmat(img_path, i)
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

	write_file_r2 = 'json/rotation_thetas_r2_' + TYPE + '.json' \
		if USE_TYPE else 'json/rotation_thetas_r2_' + TRAIN_N + '.json'
	with open(write_file_r2, 'w') as outfile:
		json.dump(rotation_thetas_r2, outfile)

	write_file_r1 = 'json/rotation_thetas_r1_' + TYPE + '.json' \
		if USE_TYPE else 'json/rotation_thetas_r1_' + TRAIN_N + '.json'
	with open(write_file_r1, 'w') as outfile:
		json.dump(rotation_thetas_r1, outfile)
	
	return rotation_thetas_r2

def getProjComponents():		
	proj_components_r2 = {}
	proj_components_r1 = {}
	img_paths = peek.getAllImgPaths(TRAIN_PATH)
	imgs = peek.getAllImgs(TYPE)

	if not USE_TYPE and len(img_paths) < TRAIN_N:
		print("img_paths != TRAIN_N")
		exit(0)
	
	n = len(imgs) if USE_TYPE else TRAIN_N 
	for i in range(n):
		img_path = getImgPath(img_paths, imgs[i]) if USE_TYPE else img_paths[i]
		Hl, Hr = peek.readmat(img_path, i)
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

	write_file_r2 = 'json/proj_components_r2_' + TYPE + '.json' \
		if USE_TYPE else 'json/proj_components_r2_' + TRAIN_N + '.json'
	with open(write_file_r2, 'w') as outfile:
		json.dump(proj_components_r2, outfile)

	write_file_r1 = 'json/proj_components_r1_' + TYPE + '.json' \
		if USE_TYPE else 'json/proj_components_r1_' + TRAIN_N + '.json'
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

	if SHOW_RESULT:
		print("[Rotation] good=" + str(good) + \
			" bad=" + str(bad) + ",\ngoods=" + str(goods) +\
			"\nbads=" + str(bads) + "\ngoods/all =" + \
			str(good/(good+bad)))
	return goods, bads


def ml_projective():
	proj_components = getProjComponents()
	good = 0
	bad = 0
	goods = []
	bads = []
	for i in proj_components.keys():
		(img, close_log) = proj_components[i]
		if close_log >= PROJECTIVE_BORDER:
			good += 1
			goods.append(int(img))
		else:
			bad += 1
			bads.append(int(img))

	if SHOW_RESULT: 
		print("[Projective] good=" + str(good) + \
			" bad=" + str(bad) + ",\ngoods=" + str(goods) +\
			" \nbads=" + str(bads) + "\ngoods/all =" + \
			str(good/(good+bad)))
	return goods,bads

def in_sequenceGoods(rotation_goods, proj_goods):
	intersection_set = rotation_goods.intersection(proj_goods)

	if SHOW_RESULT: 
		print("[Rot+Proj] result goods=" + str(sorted(list(intersection_set))))
	return intersection_set

def in_sequenceBads(rotation_bads, proj_bads):
	union_set = rotation_bads.union(proj_bads)

	if SHOW_RESULT: 
		print("[Rot+Proj] result bads=" + str(sorted(list(union_set))))
	return union_set

def ml():
	rotationGB = ml_rotation()
	projectiveGB = ml_projective()

	rotation_goods = set(rotationGB[0])
	proj_goods = set(projectiveGB[0])
	total_goods = in_sequenceGoods(rotation_goods, proj_goods)

	rotation_bads = set(rotationGB[1])
	proj_bads = set(projectiveGB[1])
	total_bads = in_sequenceBads(rotation_bads, proj_bads)

	if SHOW_RESULT: 
		print("[Rot+Proj] result good=" + str(len(total_goods)) + \
			" result bad=" + str(len(total_bads)) + "\ngoods/all =" + \
			str(len(total_goods)/(len(total_goods)+len(total_bads))))



if __name__ == '__main__':
	ml()