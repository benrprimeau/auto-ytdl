import json
import ast
import time
import re
from os import listdir
from os.path import isfile, join
import os
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from youtube_dl import YoutubeDL


Collection = {}
Quit = False

ToDownload= []

with open('reversedPlaylists.txt','r') as file:
	reversedPlaylists = ast.literal_eval(file.read())

#Set up youtubeData API
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
youTubeApiKey = #APIKEY
youtube=build('youtube','v3',developerKey=youTubeApiKey)

multipageMaxResults = 50

open('urls.txt', 'w').close()

while Quit == False:
	#Read Collection from Text Document, stored as dict
	with open('Collection.txt', 'r') as file:
		Collection = ast.literal_eval(file.read())

	print('You have %d current subscriptions' %len(Collection))
	for item in Collection:
		print(item + ': ' + Collection[item])

	inp = input('1: Edit subscriptions, 2: Update library, 3: Quit\n')
	
	if inp=='1':

		inp2 = input('1: Add subscriptions, 2: Pause/Unpause Subscription, 3: Upgrade Subscription\n')

		if inp2 == '1':
			val = str(input('Please input the id:\n'))

			if ('youtube.com' not in val):
				if val.startswith('PL'):
					playlistContent=youtube.playlists().list(part='snippet',id=val).execute()

					name = playlistContent['items'][0]['snippet']['title']

				elif val.startswith('U'):
					channelContent=youtube.channels().list(part='snippet',id=val).execute()

					name = channelContent['items'][0]['snippet']['title']

				Collection.update({name:val})
				CollectionKeys = list(Collection.keys())
				CollectionKeys.sort()
				Collection = {k: Collection[k] for k in CollectionKeys}

				p = input('Id ' + val + ' matches with ' + name + '. Would you like to proceed in downloading and adding to library? (y/n)\n')
				d = input('Start after specific date? (YYYYMMDD or n)')

				if val.startswith('PL'):
					r = input('Newest videos on top? (y/n)')

				else:
					r = 'y'

				if r == 'n':
					with open('reverse.txt', 'w') as file:
						file.write(' ')

				elif r == 'y':
					with open('reverse.txt', 'w') as file:
						file.write('--playlist-reverse')

					if val.startswith('PL'):
						if val not in reversedPlaylists:
							reversedPlaylists.append(val)

							with open('reversedPlaylists.txt','w') as file:
								file.write(str(reversedPlaylists))

				if d == 'n':
					with open('dateAfter.txt', 'w') as file:
						file.write('00010101')

				if d != 'n':
					with open('dateAfter.txt', 'w') as file:
						file.write(str(d))

				if p == 'y' or p == 'Y':
					with open('Collection.txt', 'w') as file:
						file.write(str(Collection))

					with open('autonumberStart.txt', 'w') as file:
						file.write('1')

					with open('folder.txt', 'w') as file:
						file.write(name)

					with open('urls.txt', 'w') as file:
						if val.startswith('PL'):
							file.write('youtube.com/playlist?list=' + val)
						elif val.startswith('U'): 
							file.write('youtube.com/channel/' + val)

					os.system('downloaderNEW.bat')

				if p == 'n' or p == 'N':
					break

		if inp2 == '2':
		#To Be Implemented
			break

		if inp2 == '3':
		#To Be Implemented
			break


	if inp=='2':
		#Get last video id in dir matching key, get id's of youtube list, see if there is an id newer than the one saved
		
		#Parsing Function
		for key in list(Collection):
			dirList = [f for f in listdir('D:/Movies/Youtube Series/'+key)]
			lastEp = str(sorted(dirList)[len(dirList)-1])

			l = 2
			while '.mkv' not in lastEp:
				lastEp = str(sorted(dirList)[len(dirList)-l])
				l = l + 1

			id = str(re.search('(\\[)(...........)(\\]\\.mkv)$', lastEp).group(2))
			#print('Latest Episode in Archives: ' + lastEp + '    id: ' + id)

			if Collection[key].startswith('U'):
				channelId=Collection[key]

				channelContent=youtube.channels().list(part='contentDetails',id=channelId).execute()
				uploadsId = channelContent['items'][0]['contentDetails']['relatedPlaylists']['uploads']


				uploads = youtube.playlistItems().list(playlistId=uploadsId, part='snippet',maxResults=50).execute()

				matched=False;
				upToDate=False;
				i=0
				while not matched:
					matchVal = str(uploads['items'][i]['snippet']['resourceId']['videoId'])
					if matchVal == id:
						matched=True
						if i == 0:
							print(key + ' up to date')
							upToDate=True;
							del Collection[key]
						else:
							print(key + ' ' + str(i) + ' episodes behind')
							uploads = uploads['items'][0:i]
					else:
						i=i+1

				if upToDate==False:
					uploads = uploads[::-1]
					urls = []

					for item in uploads:
						ToDownload.append('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']))

			elif Collection[key].startswith('P'):

				playlistId=Collection[key]

				playlistContent=youtube.playlistItems().list(playlistId=playlistId, part='snippet',maxResults=50).execute()

				#PLAYLISTS WITH NEWEST VIDEOS AT THE TOP
				if Collection[key] in reversedPlaylists:

					videos = playlistContent['items']

					videos = [x for x in videos if 'Private video' not in x['snippet']['title']]

					matched=False;
					upToDate=False;
					i=0
					while not matched:
						matchVal = str(videos[i]['snippet']['resourceId']['videoId'])
						if matchVal == id:
							matched=True
							if i == 0:
								print(key + ' up to date')
								upToDate=True;
								del Collection[key]
							else:
								print(key + ' ' + str(i) + ' episodes behind')
								videos = videos[0:i]
						else:
							i=i+1

					if upToDate==False:
						videos = videos[::-1]
						urls = []

						for item in videos:
							ToDownload.append('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']))

				#PLAYLISTS WITH NEWEST VIDEOS ON THE BOTTOM
				else:
					next=''
					error=False

					while error==False:
						try:
							next = playlistContent['nextPageToken']
							playlistContent=youtube.playlistItems().list(playlistId=playlistId, part='snippet',maxResults=multipageMaxResults, pageToken=next).execute()
						except:
							error==True
							break

					videos = playlistContent['items'][::-1]

					videos = [x for x in videos if 'Private video' not in x['snippet']['title']]

					matched=False;
					upToDate=False;
					i=0
					while not matched:
						matchVal = str(videos[i]['snippet']['resourceId']['videoId'])
						if matchVal == id:
							matched=True
							if i == 0:
								print(key + ' up to date')
								upToDate=True;
								del Collection[key]
							else:
								print(key + ' ' + str(i) + ' episodes behind')
								videos = videos[0:i]
						else:
							i=i+1

					if upToDate==False:
						videos = videos[::-1]
						urls = []

						for item in videos:
							ToDownload.append('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']))

		totalSize = 0

		ydl_opts = {
			'format': 'bestvideo+bestaudio',
			'quiet': True,
			'no_warnings': True
		}

		ytdl = YoutubeDL(ydl_opts)

		for url in ToDownload:
			info = ytdl.extract_info(url, download=False)

			filesize = info['requested_formats'][0]['filesize']+info['requested_formats'][1]['filesize']

			sizeForm=filesize/1024/1024

			totalSize += sizeForm

		print("\n##########################################")
		print('# Total Size to Download: ' + str(int(round(totalSize, 0)))+'MiB')
		print('# Number of items to Download: ' + str(len(ToDownload)))
		print('##########################################')

		time.sleep(3)


		#Downloading Function
		for key in Collection:
			dirList = [f for f in listdir('D:/Movies/Youtube Series/'+key)]
			lastEp = str(sorted(dirList)[len(dirList)-1])

			l = 2
			while '.mkv' not in lastEp:
				lastEp = str(sorted(dirList)[len(dirList)-l])
				l = l + 1

			id = str(re.search('(\\[)(...........)(\\]\\.mkv)$', lastEp).group(2))

			if Collection[key].startswith('U'):
				channelId=Collection[key]

				channelContent=youtube.channels().list(part='contentDetails',id=channelId).execute()
				uploadsId = channelContent['items'][0]['contentDetails']['relatedPlaylists']['uploads']


				uploads = youtube.playlistItems().list(playlistId=uploadsId, part='snippet',maxResults=50).execute()

				matched=False;
				upToDate=False;
				i=0
				while not matched:
					matchVal = str(uploads['items'][i]['snippet']['resourceId']['videoId'])
					if matchVal == id:
						matched=True
						uploads = uploads['items'][0:i]
					else:
						i=i+1

				uploads = uploads[::-1]
				urls = []
				with open('urls.txt', 'w') as file:
					for item in uploads:
						file.write('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']) + '\n')

				with open('autonumberStart.txt', 'w') as file:
					file.write(str(int(re.search('(S01E)(\d\d\d)', lastEp).group(2))+1))

				with open('folder.txt', 'w') as file:
					file.write(key)

				os.system("downloader.bat")

			elif Collection[key].startswith('P'):
				playlistId=Collection[key]

				playlistContent=youtube.playlistItems().list(playlistId=playlistId, part='snippet',maxResults=50).execute()

				if Collection[key] in reversedPlaylists:

					videos = playlistContent['items']

					for item in videos:
						if item['snippet']['title'] == 'Private video':
							videos.remove(item)

					matched=False;
					upToDate=False;
					i=0
					while not matched:
						matchVal = str(videos[i]['snippet']['resourceId']['videoId'])
						if matchVal == id:
							matched=True
							videos = videos[0:i]
						else:
							i=i+1

					videos = videos[::-1]
					urls = []
					with open('urls.txt', 'w') as file:
						for item in videos:
							file.write('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']) + '\n')

					with open('autonumberStart.txt', 'w') as file:
						file.write(str(int(re.search('(S01E)(\d\d\d)', lastEp).group(2))+1))

					with open('folder.txt', 'w') as file:
						file.write(key)

					os.system("downloader.bat")

				else:
					next=''
					error=False

					while error==False:
						try:
							next = playlistContent['nextPageToken']
							playlistContent=youtube.playlistItems().list(playlistId=playlistId, part='snippet',maxResults=multipageMaxResults, pageToken=next).execute()
						except:
							error==True
							break

					videos = playlistContent['items'][::-1]

					for item in videos:
						if item['snippet']['title'] == 'Private video':
							videos.remove(item)

					matched=False;
					upToDate=False;
					i=0
					while not matched:
						matchVal = str(videos[i]['snippet']['resourceId']['videoId'])
						if matchVal == id:
							matched=True
							videos = videos[0:i]
						else:
							i=i+1

					videos = videos[::-1]
					urls = []
					with open('urls.txt', 'w') as file:
						for item in videos:
							file.write('youtube.com/watch?v=' + str(item['snippet']['resourceId']['videoId']) + '\n')

					with open('autonumberStart.txt', 'w') as file:
						file.write(str(int(re.search('(S01E)(\d\d\d)', lastEp).group(2))+1))

					with open('folder.txt', 'w') as file:
						file.write(key)

					os.system("downloader.bat")


		print("\n\n All series up to date\n\n")

	if inp=='3':
		Quit==True
		break