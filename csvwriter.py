import csv

class CSVWriter:
	'Write Data to CSV Files.'

	def __init__(self, filename=None, headers=None):
		self._filename = filename
		self._headers = headers
		self._csvFile = open(self._filename, "wt")
		self._csvWriter = csv.writer(self._csvFile)
		self._init()

	def _init(self):
		self._csvWriter.writerow(self._headers)

	def write(self, toWrite):
		self._csvWriter.writerow(toWrite)

	def close(self):
		self._csvFile.close()
