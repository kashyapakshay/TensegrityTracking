import cv2

class Utilities:
	'A Collection of Miscellaneous Utilities.'

	def __init__(self):
		pass

	def getLargestContour(self, contoursList):
		contoursListCopy = contoursList[:]

		largestContour = contoursListCopy[0]
		for contour in contoursListCopy:
			if(cv2.contourArea(contour) > cv2.contourArea(largestContour)):
				largestContour = contour

		return largestContour

	def mergeSortContours(self, contoursList):
		contoursListCopy = contoursList[:]

		if len(contoursListCopy) > 0:
			mid = len(contoursListCopy)//2
			leftHalf = contoursListCopy[:mid]
			rightHalf = contoursListCopy[mid:]

			leftHalf = mergeSort(leftHalf)
			rightHalf = mergeSort(rightHalf)

			i = j = k = 0
			while i < len(leftHalf) and j < len(rightHalf):
				if cv2.contourArea(leftHalf[i])<cv2.contourArea(rightHalf[j]):
					contoursListCopy[k] = leftHalf[i]
					i = i + 1
				else:
					contoursListCopy[k] = rightHalf[j]
					j = j + 1

				k = k + 1

			while i < len(leftHalf):
				contoursListCopy[k] = leftHalf[i]
				i = i + 1
				k = k + 1

			while j < len(rightHalf):
				contoursListCopy[k] = rightHalf[j]
				j = j + 1
				k = k + 1

		return contoursListCopy

	def rectangularSmooth(self, input):
		output = []
		output.append(input[0])

		for i in range(1, len(input) - 1):
			output.append(
				(input[i - 1] + input[i] + input[i + 1])/3)

		output.append(input[-1])

		return output

	def triangularSmooth(self, input):
		output = []
		output.append(input[0])
		output.append(input[1])
		
		avg = 0

		for i in range(2, len(input) - 2):
			avg = (input[i - 1] + 2*input[i - 1] 
				+ 3*input[i] 
				+ 2*input[i + 1] + input[i + 2])/9

			output.append(avg)

		output.append(input[-2])
		output.append(input[-1])

		return output

	def compute_dft(self, input):
		n = len(input)
		output = [complex(0)] * n

		for k in range(n):  # For each output element
			s = complex(0)
			
			for t in range(n):  # For each input element
				s += input[t] * cmath.exp(-2j * cmath.pi * t * k / n)
			output[k] = s

		return output
