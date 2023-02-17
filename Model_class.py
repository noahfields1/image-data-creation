import util
import tools #from the github repository

class Model():
	def __init__(self,model_name, pathway):
		self.model_name = model_name
		self.pathway = pathway
	def filter_3Dpoints():
		pass


class Branch(Model):
	def __init__(self, Model, branch_name):
		self.model_name = Model.model_name
		self.pathway = Model.pathway
		self.branch_name = branch_name

class Images(Branch):
	def __init__(self, Branch, image_name):
		self.model_name = Branch.model_name
		self.pathway = Branch.pathway
		self.branch_name = Branch.branch_name
		self.image_name = image_name
		self.path_id = None
		self.yaml_file = None
		self.points3D_file = None
		self.points3D = []
		self.points2D = []
		self.points2D_filtered = []
		self.image_corners3D = []
		self.radius = None
		self.BifurcationID = None
		self.spacing = None
		self.dimensions = 160
		self.extent = 240
		self.vtp_file = None
		self.vti_file = None
		self.X_np_file = None
		self.X_pnd_file = None
		self.Y_png_file = None
		self.Yc_np_file = None
		self.Yc_png_file = None
	def generateFileNames():
		self.points3D_file = None
		self.vtp_file = None
		self.vti_file = None
		self.yaml = None
		self.X_np_file = None
		self.X_pnd_file = None
		self.Y_png_file = None
		self.Yc_np_file = None
		self.Yc_png_file = None
	def generatePNG(image_type,arr):
		reader = vtk.vtkXMLImageDataReader()
    	reader.SetFileName(vtiFilePath)
    	reader.Update()
    	vtiimage = reader.GetOutput()
    	extent = vtiimage.GetExtent()
    	width = extent[1] - extent[0] + 1
    	height = extent[3] - extent[2] + 1
    	image_data = np.reshape(v2n(vtiimage.GetPointData().GetArray(0)), (width, height))
    	np.save(X_np_path,image_data) #saving npy image
    	matplotlib.image.imsave(output_path + "image" + vtpfile[5:-4] + '.png', image_data,cmap='gray')
    	img = Image.open(output_path + "image" + vtpfile[5:-4] + '.png').convert('L')
    	img.save(output_path + "image" + vtpfile[5:-4] + '.png') #saving png image
	def generateYAML():
		pass
	def getPoints():
		for line in filename.readlines():
			coord = line.split()
			x = (float(coord[0]))
			y = (float(coord[1]))
			z = (float(coord[2]))
			self.points3D.append(np.array([x,y,z]))
		new_origin = self.points3D[0]
		self.image_corners = self.points3D[0:4]
		vec1 = self.image_corners[1] - self.image_corners[0]
		vec2 = self.image_corners[2] - self.image_corners[0]
		vec3 = self.image_corners[3] - self.image_corners[0]
		new_pts = []
		for i in pts:
			a = (np.dot(i,vec1)/np.dot(vec1,vec1)) * 240
			b = (np.dot(i,vec3)/np.dot(vec3,vec3)) * 240
			new_pts.append((a,b))
		self.points2D = new_pts[4:]
	def connectPoints():
		#Reading in the points from 'path_2D'
		f = open(path_2D,'r')
		points = []
		points_set = set()
		for i in f.readlines():
			point = i.rstrip().split()
			points.append((int(float(point[0])),int(float(point[1]))))
			points_set.add((int(float(point[0])),int(float(point[1]))))
		points = list(points_set)
		f.close()
		#If there are no points (or just the origin), we get rid of the point
		#This is the case when a pathway point is created without a segmentation
		if len(points) <= 1:
			return
		#The origin is the first point (also known as the centerpoint of the pathway)
		origin = (121,121)
		min = 10000
		min_index = None

		#Find the closest point to the centerpoint of the pathway (origin)
		for i in range(0,len(points)):
			dist_from_origin = ((origin[0] - points[i][0])**2 + (origin[1] - points[i][1])**2)**0.5
			if dist_from_origin < min:
				min = dist_from_origin
				min_index = i
		first_point = points.pop(min_index)

		#Finding all the points in the vessels
		#points is the array of all the points, and we are selectively adding points to vessel array
		old_point = first_point
		next_point = None
		next_point_index = None
		old_tangent = None
		new_tangent = None
		min = 10000
		vessel = []
		while next_point != first_point and len(points) != 0:
			min = 10000
			next_point_index = None
			for i in range(0,len(points)):
				dist_from_old_point = ((old_point[0] - points[i][0])**2 + (old_point[1] - points[i][1])**2)**0.5
				if dist_from_old_point < min:
					min = dist_from_old_point
					next_point_index = i
			next_point = points[next_point_index]
			old_point = points.pop(next_point_index)
			vessel.append(old_point)
			if len(vessel) == 10:
				points.append(first_point)

		#add the first point back again, so we have a complete circle
		vessel.append(vessel[0])
		
		#Recursively go through all of the points and add the midpoints to the vessels
		#until all of the points are connected
		finished = False
		i = 0
		while not finished:
			if not neighbors(vessel[i],vessel[i+1]):
				x_mid = round((vessel[i][0] + vessel[i+1][0])/2)
				y_mid = round((vessel[i][1] + vessel[i+1][1])/2)
				midpoint = (x_mid,y_mid)
				vessel.insert(i+1,midpoint)
				i = i - 1
			i += 1
			if i == len(vessel)-1:
				finished = True

		start = [(121,121)]
		used = set(vessel)

		while len(start) != 0:
			next = start.pop(0)
			if next in used:
				continue
			if next[1] == 239 or next[1] == 0 or next[0] == 0 or next[0] == 239:
				used.add(next)
				return
			used.add(next)
			if (next[0]+1,next[1]) not in used:
				start.append((next[0]+1,next[1]))
			if (next[0],next[1]+1) not in used:
				start.append((next[0],next[1]+1))
			if (next[0]-1,next[1]) not in used:
				start.append((next[0]-1,next[1]))
			if (next[0],next[1]-1) not in used:
				start.append((next[0],next[1]-1))
		used.add((121,121))
		
		if len(used) > 40000:
			return
		vessel = used
		f = open(path_2D_clean,'w')
		for i in vessel:
			f.write(str(i[0]) + '\t' + str(i[1]) + '\n')
		f.close()

	def fillInVessel():
		pass
	def scoreDistance(scorefxn):
		pass
	def getBifurcationID():
		vtp = tools.read_geo(self.vtp_file)
		point_data, _, points = tools.get_all_arrays(vtp.GetOutput())
		bifurcationId = point_data['BifurcationId']
		self.BifurcationID = BifurcatoinID
	def getRadius():
		pass



m1 = Model("model2","/here/it/is")
b1 = Branch(m1, "branch34")
#b1.pathway = "hi"
print(b1.branch_name, b1.pathway, b1. model_name)