import re
import requests
import sys
from bs4 import BeautifulSoup as bs
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

#Set up youtubeData API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youTubeApiKey = ""
youtube = build('youtube','v3',developerKey=youTubeApiKey)

class youtubeItem:
	def __init__(self, name, type, id, image):
		self.name = name
		self.type = type
		self.id = id
		self.image = image

	def __init__(self, url):
		idRegex = re.compile(r'www.youtube.com/(\w*)/(\w*)')

		self.type = idRegex.search(url).group(1)
		self.id = idRegex.search(url).group(2)

		channelContent=youtube.channels().list(part='snippet',id=self.id).execute()
		self.name = channelContent['items'][0]['snippet']['title']
		self.image = channelContent['items'][0]['snippet']['thumbnails']['default']['url']

	def getName(self):
		return self.name

	def getId(self):
		return self.id

	def getImage(self):
		return self.image

	def __str__(self):
		return(" ".join((self.name, self.type, self.id, self.image)))

	def __gt__(self,other):
		if self.name.lower() > other.name.lower():
			return True

		return False

	def __lt__(self,other):
		if self.name.lower() < other.name.lower():
			return True

		return False

	def __eq__(self,other):
		if self.name == other.name:
			return True

		return False
