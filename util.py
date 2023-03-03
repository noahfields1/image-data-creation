from matplotlib import pyplot as plt
import numpy as np
import os
def isNeighbor(p1,p2):
	x_true = True
	y_true = True
	if abs(p1[0]-p2[0]) > 1:
		x_true = False
	if abs(p1[1]-p2[1]) > 1:
		y_true = False
	return x_true and y_true
def euclideanDistance(p1,p2):
	dist = (p2[0]-p1[0]) **2 + (p2[1]-p1[1]) **2
	return dist ** 0.5
def findRadius():
	pass
def previewImage(pts):
	arr = np.zeros((240,240))
	for i in pts:
		arr[i[0],i[1]] = 1
	plt.imshow(arr)
	plt.show()
def create_directories():
	base_dir = "./3D_points"
	files_dir = "./files"
	for model in os.listdir(base_dir):
		if model == ".DS_Store":
			continue
		base_model_dir = base_dir + "/" + model
		files_model_dir = files_dir + "/" + model

		if not os.path.exists(files_model_dir):
			os.mkdir(files_model_dir)
		for branch in os.listdir(base_model_dir):
			if branch == ".DS_Store":
				continue
			files_branch_dir = files_model_dir + "/" + branch
			if not os.path.exists(files_branch_dir):
				os.mkdir(files_branch_dir)

create_directories()
