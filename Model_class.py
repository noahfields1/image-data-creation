import util
import tools #from the github repository
import numpy as np
import PIL 
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

class Image(Branch):
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
		self.X_png_file = None
		self.Y_png_file = None
		self.Yc_np_file = None
		self.Yc_png_file = None
	def generateFileNames(self):
		self.points3D_file = "./3D_points/" + self.model_name + "/" + self.branch_name + "/3D_points_" + self.image_name + ".txt"
		self.vtp_file = "./centerlines/" + self.model_name + ".vtp"
		self.vti_file = "./results/" + self.model_name + "/Mesh/" + self.branch_name + "/image_slice_" + self.image_name + ".vti"
		self.yaml_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".yaml"
		self.X_np_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".X.npy"
		self.X_png_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".X.png"
		self.Y_png_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".Y.png"
		self.Yc_np_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".Yc.npy"
		self.Yc_png_file = "./files/" + self.model_name + "/" + self.branch_name + "/" + self.image_name + ".Yc.png"
	def generateXPNG(image_type,arr):
		pass
		#reader = vtk.vtkXMLImageDataReader()
    	#reader.SetFileName(vtiFilePath)
    	#reader.Update()
    	#vtiimage = reader.GetOutput()
    	#extent = vtiimage.GetExtent()
    	#width = extent[1] - extent[0] + 1
    	#height = extent[3] - extent[2] + 1
    	#image_data = np.reshape(v2n(vtiimage.GetPointData().GetArray(0)), (width, height))
    	#np.save(self.X_np_file,image_data) #saving npy image
    	#matplotlib.image.imsave(output_path + "image" + vtpfile[5:-4] + '.png', image_data,cmap='gray')
    	#img = Image.open(output_path + "image" + vtpfile[5:-4] + '.png').convert('L')
    	#img.save(self.X_png_file) #saving png image
	def generateYAML():
		yaml_dict = [{'X':self.X_np_file},{'Y':self.Y_np_file},{'Yc':self.Yc_np_file},{'dimensions':self.dimensions},{'extent':self.extent},{'image':image_path},{'path_id':''},{'path_name':self.branch_name},{'point':self.image_name},{'radius':''},{'spacing':''}]
		with open(yaml_file, 'w') as file:
			documents = yaml.dump(yaml_dict,file)
	def getPoints(self):
		pts = []
		f = open(self.points3D_file,'r')
		for line in f.readlines():
			coord = line.split()
			x = (float(coord[0]))
			y = (float(coord[1]))
			z = (float(coord[2]))
			pts.append(np.array([x,y,z]))
		new_origin = pts[0]

		for i in range(len(pts)):
			self.points3D.append(pts[i] - new_origin)
		self.image_corners = self.points3D[0:4]
		vec1 = self.image_corners[1] - self.image_corners[0]
		vec2 = self.image_corners[2] - self.image_corners[0]
		vec3 = self.image_corners[3] - self.image_corners[0]
		new_pts = []
		for i in self.points3D[4:]:
			a = int((np.dot(i,vec1)/np.dot(vec1,vec1)) * 240)
			b = int((np.dot(i,vec3)/np.dot(vec3,vec3)) * 240)
			if a < 0 or a > 239 or b < 0 or b > 239:
				continue
			new_pts.append((a,b))
		self.points2D = new_pts
	def connectPoints(self):
		#Reading in the points from 'path_2D'

		points = list(self.points2D)

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
				dist_from_old_point = self.scoreDistance(util.euclideanDistance,old_point,points[i])
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
			if not util.isNeighbor(vessel[i],vessel[i+1]):
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
		self.points2D_filtered = used

		

	def scoreDistance(self,scorefxn,p1,p2):
		return scorefxn(p1,p2)
	def getBifurcationID(self):
		vtp = tools.read_geo(self.vtp_file)
		point_data, _, points = tools.get_all_arrays(vtp.GetOutput())
		bifurcationId = point_data['BifurcationId']
		self.BifurcationID = bifurcationId
	def getRadius():
		pass
	def createImg(self):
		arr = np.zeros((240,240))
		for i in self.points2D_filtered:
			arr[i[0],i[1]] = 1

		arr = arr * 255
		arr = arr.astype(np.uint8)
		im = PIL.Image.fromarray(arr)
		im.save(self.Yc_png_file)
		np.save(self.Yc_np_file,arr)



m1 = Model("0083_2002",".")
b1 = Branch(m1, "LPA")
i1 = Image(b1,"10")
i1.generateFileNames()
print(i1.points3D_file)
#print(i1.points3D_file)
i1.getPoints()
#print(len(i1.points3D))
#rint(i1.points2D)
print(i1.Yc_png_file)
i1.connectPoints()
#print(i1.points2D_filtered)
#util.previewImage(i1.points2D_filtered)
i1.createImg()
#print(b1.branch_name, b1.pathway, b1. model_name)