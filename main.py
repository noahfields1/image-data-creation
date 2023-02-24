import os
import Model_class
#if name == "main":
models_dir = "./models"
centerlines_dir = "./centerlines"
for model in os.listdir(models_dir):
	print(model)
	m = Model_class.Model(model,".")
	branch_dir = models_dir + "/" + model + "/Mesh"
	for branch in os.listdir(branch_dir):
		print(branch)
		b = Model_class.Branch(m,branch)
		image_dir = branch_dir + "/" + branch
		for image in os.listdir(image_dir):
			im = image[0:-4].split('_')[2]
			print(im)
			i = Model_class.Image(b,im)
			# i.generateFileNames()
			# i.getPoints()
			# i.connectPoints()
			# i.createImg()
