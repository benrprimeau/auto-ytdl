from youtubeItem import *
import pickle

class collection:
	def __init__(self):
		self.collection = []

	def getItem(self, index):
		return self.collection[index]

	def getLength(self):
		return len(self.collection)

	def addYoutubeItem(self, url):
		self.collection.append(youtubeItem(url))

	def removeDuplicates(self):
		self.collection.sort()
		
		##DOESN'T WORK		
		i=0

		while i<len(self.collection)-1:
			if self.collection[i+1]==self.collection[i]:
				self.collection.pop(i+1)

				print(self.collection)

			else:
				i+=1


	def read(file):
		with open(file, 'rb') as f:
			return pickle.load(f)

	def write(self, file):
		with open(file,'wb') as f:
			pickle.dump(self, f)