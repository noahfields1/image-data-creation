def isNeighbor(p1,p2):
	x_true = True
	y_true = True
	if abs(p1[0]-p2[0]) > 1:
		x_true = False
	if abs(p1[1]-p2[1]) > 1:
		y_true = False
	return x_true and y_true
def euclideanDistance(p1,p2):
	dist = (p2[0]-p1[0]) **2 + (p2[1]-p1[1]) **2 + (p2[2]-p1[2]) **2
	return dist ** 0.5
def findRadius():
	pass
def findMidpoint():
	for i in arr:
		x += arr[0]
		y += arr[1]
	x = x / len(arr)
	y = y / len(arr)
	return x,y