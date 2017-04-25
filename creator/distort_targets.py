# classify_images.py
# Author: Arizona Autonomous Vehicles Club
# Task: AUVSI SUAS 2017 Image Classification
# Description: This script applies random distortions to images with JSON labels in a directory

import argparse
import os
import shutil
import json

import numpy as np
import cv2

parser = argparse.ArgumentParser(
					description='Utility program which applies distortions to contents '
								'of a folder. Note that both the image AND the JSON '
								'must be present in the directory!'
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-d', '--dir', 
						help='Directory to scan for images. If no directory provided, '
								'scans current working directory')
parser.add_argument('-n', '--num_copies', default=1,
						help='Number of distorted copies to generate, excluding original')

args = parser.parse_args()

def randomAngle(maxangle=180):
    return (random.random() - 0.5) * 2 * maxangle

	
def distort_image(image, perspective_warp_weight=0.2):
	im = image.copy()
	
	# Randomly the target
	(h, w) = im.shape[:2]
	center = (w / 2, h / 2)
	M = cv2.getRotationMatrix2D(center, randomAngle(180), 1.0)
	im = cv2.warpAffine(im, M, (w, h))
	
	# Randomly distort perspective
	psrc = np.array([[0,0], [w-1,0], [w-1,h-1], [0, h-1]], dtype=np.float32)
	warp_amt = ((h + w) / 2) * perspective_warp_weight
	pdst = np.array([[0-warp_amt*random.random(), 0-PW*random.random()],
					 [w-1+warp_amt*random.random(), 0-PW*random.random()],
					 [w-1+PW*random.random(), h-1+PW*random.random()],
					 [0-PW*random.random(), h-1+PW*random.random()]], dtype=np.float32)
	warp = cv2.getPerspectiveTransform(psrc, pdst)
	im = cv2.warpPerspective(im, warp, (w, h)) # targetWarped
	
	return im
	
def save_to_processed_subdir(root, f, newname=None, copy=False):
	''' Args:
			root: root directory path (str)
			f: the file to move
	'''
	if newname is not None:
		filename = newname
	else
		filename = f
	# Move a file into processed_## subdir
	counter = 0
	processedDir = 'processed_' + str(counter).zfill(2)
	# Increment counter until we find unused processed_##/file location
	while os.path.exists(os.path.join(root, processedDir, f)):
		counter += 1
		processedDir = 'processed_' + str(counter).zfill(2)
	# NOTE: Program will continue to work after counter > 99, but naming
	#	   convention will be violated (e.g. processed_101/foo.jpg)
	# Make subdirectories as necessary
	if not os.path.exists(os.path.join(root, processedDir)):
		os.mkdir(os.path.join(root, processedDir))
	# Move processed file to processed_##/ subdirectory
	if copy:
		shutil.copyFile(os.path.join(root, f), os.path.join(root, processedDir, filename))
	else:
		os.rename(os.path.join(root, f), os.path.join(root, processedDir, filename))

	
def main():
	# Process command line args
	if args.dir is not None:
		 directory = args.dir
	else:
		 directory = os.getcwd()
	ext = '.' + args.format.split('.')[-1].lower()

	# Validate arguments
	assert os.path.exists(directory)

	# Iterate through files in directory (NOTE: 'file' is a __builtin__)
	counter = 0
	processed = 0
	generated = 0
	for f in os.listdir(directory):
		if f.lower().endswith('json'):
			if args.verbose:
				print('Processing %s' % os.path.join(directory, f))
				
			with open(f) as data_file:
				data = json.load(data_file) # TODO
				imagepath = data['image']
				image = cv2.imread(imagepath)
				# TODO: Rewrite image entry of json with corrected path (e.g. path to the JPGs)
				
				# Process image here
				for i in xrange(args.num_copies):
					im_distorted = distort_image(image)
					json_name, json_ext = os.path.splitext(f)
					json_out = json_name + '_%d' % i + json_ext
					move_to_processed_subdir(directory, f, json_out, copy=True)
					generated += 1
				
				# Move processed files into processed_## subdir
				move_to_processed_subdir(directory, f)
				# TODO: Move the processed image as well
				
				processed += 1
			
			counter += 1

	if args.verbose:
		print('Image distortion script complete. Execution summary:')
		print('%d files found' % counter)
		print('%d files successfully processed' % processed)
		print('%d images generated' % generated)

if __name__ == '__main__':
	main()
						
						
