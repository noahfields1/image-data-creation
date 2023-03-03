import os
import Model_class
import util
util.create_directories()
models_dir = "./3D_points"
centerlines_dir = "./centerlines"
for model in os.listdir(models_dir):
	if model == ".DS_Store":
		continue
	m = Model_class.Model(model,".")
	branch_dir = models_dir + "/" + model
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
			i.connectPoints()
			i.generateYAML()
			i.getBifurcationID() #Need to learn how to filter based on this!
			i.createImg("X")
			i.createImg("Y")
			i.createImg("Yc")
