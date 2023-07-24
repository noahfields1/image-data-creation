from matplotlib import pyplot as plt
import numpy as np
import os
import glob
import Model_class

"""
This function is designed to be used after 'create_directories'.
This function rotates through all models,branches, and images
found in ./3D_points and creates 2D images and generates corresponding yaml files.
"""
def create_images():
	points3D_dir = "./3D_points"
	for model in os.listdir(points3D_dir):
		if model == ".DS_Store":
			continue


		m = Model_class.Model(model,".")
		branch_dir = points3D_dir + "/" + model
		for branch in os.listdir(branch_dir):
			if branch == ".DS_Store":
				continue

			b = Model_class.Branch(m,branch)
			image_dir = branch_dir + "/" + branch

			for image in os.listdir(image_dir):
				if image == ".DS_Store":
					continue

				im = image[0:-4].split('_')[2]
				i = Model_class.Image(b,im)
				i.generateFileNames()
				i.getPoints()
				i.getBifurcationID()
				if i.BifurcationID != -1:
					continue
				i.connectPoints()
				if len(i.points2D_filtered) < 4 or len(i.points2D_filtered) > 40000:
					continue
				i.generateYAML()
				i.createImg("X")
				i.createImg("Y")
				i.createImg("Yc")
"""
This function is used to make directories needed to run Dave's code.
If a directory already exist, then the directory is not added.
Input: The pathway to all of the models
Output: None
Function: Runs Dave's code on all models and all pathways available
using the directory holding all of the VMR models.
"""
def create_directories(models_dir):
	if not os.path.exists("./3D_points"):
		os.mkdir("./3D_points")
	if not os.path.exists("./files"):
		os.mkdir("./files")
	if not os.path.exists("./results"):
		os.mkdir("./results")
	models = set(os.listdir(models_dir))

	for m in models:
		if m == ".DS_Store":
			continue
		paths = os.listdir(models_dir + "/" + m + "/Paths/")
		if not os.path.exists("./3D_points/" + m): #if the pathway already exists, ignore it
			os.mkdir("./3D_points/" + m)
		else:
			continue
		if not os.path.exists("./files/" + m):
			os.mkdir("./files/" + m)
		else:
			continue
		if not os.path.exists("./results/" + m):
			os.mkdir("./results/" + m)
		for p in paths:
			if p == ".DS_Store":
				continue
			p = p[0:-4]
			if not os.path.exists("./3D_points/" + m + '/' + p):
				os.mkdir("./3D_points/" + m + '/' + p)
			if not os.path.exists("./files/" + m + '/' + p):
				os.mkdir("./files/" + m + '/' + p)
			if not os.path.exists("./results/" + m + '/' + p):
				os.mkdir("./results/" + m + '/' + p)
			create_slices(m,p)

#This function runs Dave's code to create image slices from a 3D volume.
def create_slices(model,path):
	images_path = "models/" + model + "/Images/OSMSC" + model.split('_')[0] + "-cm.vti"
	models_file = "models/" + model + "/Meshes/" + model + ".vtp"
	results_dir = "results/" + model + "/" + path
	path_dir = "models/" + model + "/Paths/" + path + ".pth"
	slice_increment = "1" #usually 10
	slice_width = "5"
	extract_slices = "True"
	os.system("python3 extract-2d-images.py --image-file " + images_path + " --path-file " + path_dir + " --model-file " + models_file + " --slice-increment " + slice_increment + " --path-sample-method number --slice-width " + slice_width + " --extract-slices " + extract_slices + " --results-directory " + results_dir)

#This function outputs the number of yaml files found, and outputs a file with the names of all the yaml files
def summary():
	yaml_count = count_yaml_files("./files")
	print("There are " + str(yaml_count) + " new training images!")
	write_files_txt("./files")

#this function takes in a pathways and returns the number of yaml files recursively found
def count_yaml_files(path):
    count = 0
    for file in glob.glob(path + "/**/*.yaml", recursive=True):
        if os.path.isfile(file):
            count += 1
    return count

#This function takes in a pathway and recursively finds all the '.yaml' returns all the pathways in an array
def get_yaml_files(path):
    yaml_files = []
    for file in glob.glob(path + "/**/*.yaml", recursive=True):
        if os.path.isfile(file):
            yaml_files.append("./files/" + os.path.relpath(file, path))
    return yaml_files

#This function writes all the yaml files into 'files.txt'
def write_files_txt(path):
    yaml_files = get_yaml_files(path)
    with open('files.txt', 'w') as file:
        file.write('\n'.join(yaml_files))

#Given two 2-dimensional points, returns true if the two points are touching (including diagnolly), and false otherwise
def isNeighbor(p1,p2):
	x_true = True
	y_true = True
	if abs(p1[0]-p2[0]) > 1:
		x_true = False
	if abs(p1[1]-p2[1]) > 1:
		y_true = False
	return x_true and y_true

#This function takes in two 2-dimensional points and returns the euclidean distance between them
def euclideanDistance(p1,p2):
	dist = (p2[0]-p1[0]) **2 + (p2[1]-p1[1]) **2
	return dist ** 0.5

#This is an undefined function.
def findRadius():
	pass

#This is a function used to preview numpy arrays in matplotlib.pyplot.
def previewImage(pts):
	arr = np.zeros((240,240))
	for i in pts:
		arr[i[0],i[1]] = 1
	plt.imshow(arr)
	plt.show()


