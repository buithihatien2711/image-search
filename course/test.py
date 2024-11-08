import cv2
import os
from pyimagesearch.colordescriptor import ColorDescriptor
from csv import writer

index_path = "index.csv" # use absolute path when open code by folder

def add_feature_row(feature, imageId):
    # List that we want to add as a new row
    row = [imageId] + feature
    
    # Open our existing CSV file in append mode
    # Create a file object for this file
    with open(index_path, 'a', newline='') as f_object:
    
        # Pass this file object to csv.writer()
        # and get a writer object
        writer_object = writer(f_object)
    
        # Pass the list as an argument into
        # the writerow()
        writer_object.writerow(row)
    
        # Close the file object
        f_object.close()

# Root directory
root_dir = 'C:\\temp\img_highres'

# Traverse the directory tree
for root, dirs, files in os.walk(root_dir):
    for file in files:
        print(root)
        file_path = os.path.join(root, file)
        print(file_path)
        # Load the image using cv2.imread
        image = cv2.imread(file_path)
        # Search image
        #extract feature
        cd = ColorDescriptor((8, 12, 3))
        features = cd.describe(image)

        add_feature_row(features, file_path)


# import os
# import shutil

# # Root directory
# root_dir = 'C:/temp/img_highres'
# # New directory to move folders
# new_dir = 'C:/temp/img_highres_selected'

# # Ensure the new directory exists
# os.makedirs(new_dir, exist_ok=True)

# # Traverse the directory tree (men/women level)
# for gender_folder in os.listdir(root_dir):
#     gender_path = os.path.join(root_dir, gender_folder)
#     if os.path.isdir(gender_path):  # Check if it's a directory (e.g., men or women)
#         # Traverse subfolders like denim, pants, etc.
#         for category in os.listdir(gender_path):
#             category_path = os.path.join(gender_path, category)
#             if os.path.isdir(category_path):  # Check if it's a directory
#                 # Get the first 3 subfolders (e.g., id_00000001)
#                 subfolders = [f for f in os.listdir(category_path) if os.path.isdir(os.path.join(category_path, f))][:3]
#                 for subfolder in subfolders:
#                     source_path = os.path.join(category_path, subfolder)
#                     destination_path = os.path.join(new_dir, subfolder)
#                     shutil.move(source_path, destination_path)
#                     print(f"Moved: {source_path} -> {destination_path}")