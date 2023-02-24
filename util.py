from matplotlib import pyplot as plt
import numpy as np
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

