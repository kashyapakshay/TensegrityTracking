import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import utilities
import csvwriter

# Time Unit to increment by
# NOTE: This in terms of frames. Set as 1/FPS to have time as seconds.
timeUnit = 1

# Color Ranges
LOWER = 0
UPPER = 1

# --- DICTIONARY OF COLORS TO TRACK ---
colorsToTrack = {
			"green": [np.array([40,100,100]), np.array([80,255,255])],
			"yellow": [np.array([23, 200, 80]), np.array([38, 255, 255])]
		}

# --- COLOR OF FIXED REFERENCE POINT ---
# Here, it's Blue.
referencePoint = [np.array([95, 200, 50]), np.array([120, 255, 255])]

def track(img, imgHSV, colorRange):
	""" Tracks the biggest blob of the given color and returns its
	bounding-box coordinates and dimensions.

	Args:
		img: The image to track blob in.
		imgHSV: The image converted to HSV color space.
		colorRange: List of lower and upper ranges of color to track.

	Yields:
		List: A list of coordinates and dimensions of the blob's bounding-box in
		pixels, in the format [x-coord, y-coord, width, height]
	"""

	# Object for Utilities class that has smoothening functions
	utils = utilities.Utilities()

	# Color Ranges
	lower = colorRange[LOWER]
	upper = colorRange[UPPER]
	
	# Create a Mask
	mask = cv2.inRange(imgHSV, lower, upper)
	resMasked = cv2.bitwise_and(img, img, mask=mask)

	# Convert to Grayscale
	resGray = cv2.cvtColor(resMasked, cv2.COLOR_BGR2GRAY)
	# and threshold
	ret, thresh = cv2.threshold(resGray, 0, 255, cv2.THRESH_BINARY)

	boundingPoints = []
	contours, hierarchy = cv2.findContours(thresh, 1, 2)
	if(len(contours) > 0):
		largestContour = utils.getLargestContour(contours)
				
		x, y, w, h = cv2.boundingRect(largestContour)
		boundingPoints = [x, y, w, h]

	return boundingPoints

def recordData(filename):
	""" Read video and track markers of colors specified in the list
	colorsToTrack above. Record coordinates of all markers, including
	reference point to a CSV file.
	"""

	csvFileName = filename + '.csv'
	csvHeaders = ('Time', 'X', 'Y', 'Marker')
	csv = csvwriter.CSVWriter(csvFileName, csvHeaders)

	timeCount = 0
	
	# --- Start Video Capture ---
	cap = cv2.VideoCapture(sys.argv[1])
	ret, frame = cap.read()

	while frame is not None:

		# Make Copy of frame, operate on the copy
		frameCopy = frame[:]
		# Blur the frame
		frameCopy = cv2.medianBlur(frameCopy, 5)
		# Convert color space from RGB to HSV
		hsv = cv2.cvtColor(frameCopy, cv2.COLOR_BGR2HSV)

		# ----- REFERENCE POINT -----
		[x, y, w, h] = track(frameCopy, hsv, referencePoint)
		refPoint = (x, y)
		
		# Draw bounding box.
		cv2.rectangle(frameCopy, (x, y), (x + w, y + h), (0, 255, 0), 2)

		# Write to CSV File
		csv.write((str(timeCount), x, y, "reference"))

		# ----- OTHER POINTS/VERTICES -----
		for colorName in colorsToTrack:
			[x, y, w, h] = track(frameCopy, hsv, colorsToTrack[colorName])

			# Draw Bounding Box and Line
			cv2.rectangle(frameCopy, (x, y), (x + w, y + h), (255, 0, 0), 2)
			cv2.line(frameCopy,(x, y),(refPoint[0],refPoint[1]),(0,0,255),1)

			# Write to CSV File
			csv.write((str(timeCount), x, y, colorName))

		timeCount += timeUnit # Increment Time by one unit.

		cv2.imshow('frame', frameCopy)
		
		ret, frame = cap.read()
		
		# Press 'q' to quit
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	cap.release()
	cv2.destroyAllWindows()

	csv.close()

def main():
	""" Main function to binding everything together.
	"""

	if(len(sys.argv) < 2):
		print "Usage: python track.py filename"
		return -1
	
	filename = (sys.argv[1].split('/')[-1]).split('.')[0]
	recordData(filename)
	
	return 0

main()