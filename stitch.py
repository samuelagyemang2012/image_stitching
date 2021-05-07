# import the necessary packages
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2

def stitch(image_path, output_path):
	print("[INFO] loading images...")
	imagePaths = sorted(list(paths.list_images(image_path)))
	images = []
	# loop over the image paths, load each one, and add them to our
	# images to stich list
	for imagePath in imagePaths:
		image = cv2.imread(imagePath)
		images.append(image)
	# initialize OpenCV's image sticher object and then perform the image
	# stitching
	print("[INFO] stitching images...")
	stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
	(status, stitched) = stitcher.stitch(images)
	cv2.imwrite(output_path,stitched)
	print('done')
