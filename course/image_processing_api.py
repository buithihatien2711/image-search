from flask import Flask, request, jsonify
import cv2
import os
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.searcher import Searcher
from csv import writer
import numpy as np

app = Flask(__name__)

# Folder to save uploaded images temporarily
UPLOAD_FOLDER = "uploads"
# Path to where the computed index will be stored (Location of feature vector is saved)
# index_path = "../index/index.csv" # use relative when not open code by workspace
index_path = "C:/temp/Image-Search-Engine/index/index.csv" # use absolute path when open code by folder
# index_path = "C:/temp/Image-Search-Engine/index/index2.csv"
# Path to the result (path of all image)
result_directory = "../images"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/search', methods=['POST'])
def search_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400

    # Save the uploaded file
    image_file = request.files['image']
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    # Load the image using cv2.imread
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({"error": "Failed to read the image"}), 500

    # Search image
    #extract feature
    cd = ColorDescriptor((8, 12, 3))
    features = cd.describe(image)

    # perform the search
    searcher = Searcher(index_path)
    limit = 10 # limit number of returned image
    results = searcher.search(features, limit)

    # display the query
    cv2.imshow("Query", image)
    # loop over the results and display result
    result_ids = []
    for (score, resultID) in results:
        # load the result image and display it
        result_ids.append(resultID)
        result_path = result_directory + "/" + resultID
        print(result_path)
        # result = cv2.imread(result_path)
        # cv2.imshow("Result", result)
        # cv2.waitKey(0)

    # Optionally, delete the file after processing
    os.remove(image_path)

    return jsonify(result_ids=result_ids), 200

@app.route('/processimage', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file uploaded"}), 400
    
    image_id = request.form.get('imageId')  # Use request.json if sent as JSON

    # If imageId is not provided, return an error
    if not image_id:
        return jsonify({"error": "No imageId provided"}), 400
    
    # Save the uploaded file
    image_file = request.files['image']
    
    image_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(image_path)

    # Load the image using cv2.imread
    image = cv2.imread(image_path)

    if image is None:
        return jsonify({"error": "Failed to read the image"}), 500

    # Search image
    #extract feature
    cd = ColorDescriptor((8, 12, 3))
    features = cd.describe(image)

    add_feature_row(features, image_id)

    # Optionally, delete the file after processing
    os.remove(image_path)

    return jsonify({"success": True}), 200

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

if __name__ == "__main__":
    app.run(debug=True)
