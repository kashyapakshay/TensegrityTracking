import sys
import matplotlib.pyplot as plt
import csv
import utilities

PLOT_X = False
PLOT_Y = False
PLOT_REL = False

APPLY_SMOOTH = False

# List of colors to graph. Same colors that were tracked.
colorsToGraph = ["green", "yellow"]

def calculateRel(xDict, yDict, xRef, yRef):
	""" Given list of X and Y coordinates for marker of each color and the
	reference point, calculate and return the list of relative distances
	between each marker and reference point, over time.

	Args:
		xDict: Dictionary containing list of X-coordinates over time for marker
		of each color, with color names as keys.
		yDict: Dictionary containing list of Y-coordinates over time for marker
		of each color, with color names as keys.
		xRef: List of X-coordinates over time for reference point.
		yRef: List of Y-coordinates over time for reference point.

	Yields:
		Dictionary: A Dictionary of list of Relative Distances(in pixels)
		between reference point and marker of each color. Colors names are
		keys.
	"""

	relDict = {}
	for colorName in colorsToGraph:
		relDict[colorName] = []

	for colorKey in xDict:
		for i in range(len(xDict[colorKey])):
			xDist = (xDict[colorKey][i] - xRef[i])
			yDist = (yDict[colorKey][i] - yRef[i])
			
			relDict[colorKey].append((xDist**2 + yDist**2)**0.5)

	return relDict

def plot(filename):
	""" Read data from specified CSV file and plot a graph for it based on
	specified flags.

	Args:
		filename: Name of CSV file to read from.
	"""

	try:
		csvFile = open(filename, "rt")
		reader = csv.reader(csvFile)
	except:
		print "*** File Not Found ***"
		return -1

	utils = utilities.Utilities()

	timeList = [-1]
	
	# Dictionary containing list of x and y coordinates for each color.
	xDict = {}
	yDict = {}
	relDict = {}

	# List of x and y coordinates for reference point
	xRef = []
	yRef = []

	# Initialize the Dictionaries
	for colorName in colorsToGraph:
		xDict[colorName] = []
		yDict[colorName] = []
		
	xDict['reference'] = []
	yDict['reference'] = []

	rowNum = 0
	for row in reader:
		if rowNum != 0:
			if timeList[-1] is not int(row[0]):
				timeList.append(int(row[0]))

			xDict[row[3]].append(int(row[1]))
			yDict[row[3]].append(int(row[2]))

		rowNum += 1

	# Remove the "reference" Data
	xRef = xDict.pop("reference", [])
	yRef = yDict.pop("reference", [])

	timeList = timeList[1:]
	
	if PLOT_REL:
		relDict = calculateRel(xDict, yDict, xRef, yRef)

	# PLOT!
	for colorKey in xDict:
		try:
			if PLOT_X:
				if APPLY_SMOOTH:
					xDict[colorKey] = utils.triangularSmooth(xDict[colorKey])

				plt.plot(timeList, xDict[colorKey], (colorKey[0]+'-'))
			if PLOT_Y:
				if APPLY_SMOOTH:
					yDict[colorKey] = utils.triangularSmooth(yDict[colorKey])

				plt.plot(timeList, yDict[colorKey], (colorKey[0]+'+'))
			if PLOT_REL:
				if APPLY_SMOOTH:
					relDict[colorKey]=utils.triangularSmooth(relDict[colorKey])

				plt.plot(timeList, relDict[colorKey], (colorKey[0]+'.'))

		except ValueError:
			print "\n*** COLOR DOES NOT EXIST: " + colorKey + " ***\n"

		except:
			print "\n*** ERROR GRAPHING: " + colorKey + " ***\n"

	plt.xlabel('Time/Frame')
	plt.ylabel('Relative Dist.')
	plt.show()

def main():
	if(len(sys.argv) < 3):
		print "Usage: python graph.py filename flags [-smooth]\nflags=x,y,rel"
		print "Example: python graph.py x,y -smooth"

		return -1

	# Set filename
	filename = sys.argv[1]

	global PLOT_X, PLOT_Y, PLOT_REL, APPLY_SMOOTH
	
	# Check flags
	flagArgs = sys.argv[2].split(',')

	if "x" in flagArgs:
		PLOT_X = True
	if "y" in flagArgs:
		PLOT_Y = True
	if "rel" in flagArgs:
		PLOT_REL = True

	if len(sys.argv) > 3:
		if sys.argv[3] == "-smooth":
			APPLY_SMOOTH = True

	# Plot
	plot(filename + ".csv")

	return 0

main()