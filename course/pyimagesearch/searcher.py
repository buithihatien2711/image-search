# import the necessary packages
import numpy as np
import csv
class Searcher:
	def __init__(self, indexPath):
		# store our index path
		self.indexPath = indexPath
	def search(self, queryFeatures, limit = 10):
		# initialize our dictionary of results
		results = {}
		# open the index file for reading
		with open(self.indexPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)
			# loop over the rows in the index
			for row in reader:
				if not row:
					continue # Move to the next row if the current one is empty
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[1:]]
				d = self.chi2_distance(features, queryFeatures)
				# now that we have the distance between the two feature
				# vectors, we can udpate the results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				results[row[0]] = d
				# image_id = row[0]
				# if image_id not in results or d < results[image_id]:
				# 	results[image_id] = d
			# close the reader
			f.close()
		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		results = sorted([(v, k) for (k, v) in results.items()])
		# return our (limited) results
		return results[:limit]
		# Extract unique image paths up to the specified limit
		# unique_paths = []
		# seen_paths = set()
		
		# for _, path in results:
		# 	if path not in seen_paths:
		# 		unique_paths.append(path)
		# 		seen_paths.add(path)
		# 	if len(unique_paths) >= limit:
		# 		break

		# # Return only the unique image paths
		# return unique_paths
	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		# return the chi-squared distance
		return d