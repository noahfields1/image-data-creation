import yaml
import os
import math
import matplotlib.pyplot as plt

# Function to recursively search for YAML files
def find_yaml_files(path):
    yaml_files = []

    for model in os.listdir(path):
            if model == ".DS_Store":
                continue
            for branch in os.listdir(path + '/' + model):
                if branch == ".DS_Store":
                    continue
                for file in os.listdir(path + '/' + model + '/' + branch):
                    if file == '.DS_Store':
                        continue
                    if file.endswith('.yaml'):
                        root = path + '/' + model + '/' + branch
                        # print(root + file)
                        # exit()
                        yaml_files.append(os.path.join(root, file))
    print(len(yaml_files))
    return yaml_files

# Function to extract radii from YAML file
def extract_radius(yaml_file):
    with open(yaml_file, 'r') as f:
        data = yaml.safe_load(f)
    if 'ratio (circum^2/area)' in data[10]:
        return data[10]['ratio (circum^2/area)']
    else:
        return None

# Recursively search for YAML files
yaml_files = find_yaml_files('./files')

# Extract radii from YAML files
radii = []
for yaml_file in yaml_files:
    radius = math.log(extract_radius(yaml_file))
    if radius is not None:
        radii.append(radius)

# Plot histogram of radii
plt.hist(radii, bins=100)
plt.xlim(2,4)
plt.xlabel('ln(Ratio)')
plt.ylabel('Frequency')
plt.show()
