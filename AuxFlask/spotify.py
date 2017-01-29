
import sys
import spotipy
import spotipy.util as util
import os
from song import Song
from settings import setKeys

class Spotify_API:

	def __init__(self, username, auxCode, playlistName = 'AuxPlaylist'):

		self.user = username
		self.sp = None
		self.authorizeUser(self.user)

		self.code = auxCode
		self.songList = []
		self.sp.user_playlist_create(username, playlistName, public = True)
		self.spPlaylist = self.sp.user_playlists(username, limit = 1, offset = 0)
		self.playListId = self.spPlaylist['items'][0]['uri']

	# Spotify functions.
	def search(self, query):

		searchResults = []
		results = self.sp.search(q = query, limit = 5, type = 'track')
		for track in results['tracks']['items']:
			print(track['name'])
			new = Song(track)
			searchResults.append(new)

		return searchResults

	def authorizeUser(self, username):

		# Spotify scope of application.
		scope = 'playlist-modify-public'
		setKeys()

		# Create Spotipy object.
		token = util.prompt_for_user_token(username, scope)
		if token:
			self.sp = spotipy.Spotify(auth = token)

	def isAuthorized(self):
		if self.sp:
			return True
		else:
			return False

	## Playlist related functions.
	def addSong(self, song):
		if len(self.songList) != 0:
			self.count = len(self.songList) - 1
			while 0 < self.songList[self.count].getVoteCount() and self.count != 0:
				self.songList[self.count + 1] = self.songList[self.count]
				self.songList[self.count + 1].setIndex(self.count + 1)
				self.count -= 1
			song.setIndex(self.count)
			self.songList.insert(self.count, song)
		elif len(self.songList) == 0:
			song.setIndex(0)
			self.songList.append(song)
		else:
			song.setIndex(self.count + 1)
			self.songList.append(song)


	def removeSong(self, songName):
		if len(self.songList) > 0:
			self.count = len(self.songList) - 1
			while songName != self.songList[self.count].getName() and self.count != 0:
				self.count -= 1
			if songName == self.songList[self.count].getName():
				self.songList.pop(self.count)
				while len(self.songList) - 1 > self.count:
					self.songList[self.count].setIndex(self.count)
					self.count += 1


	def getCode(self):
		return self.code

	def rearrangeUpvote(self, index):
		if self.songList[index].getVoteCount() > self.songList[index+1].getVoteCount() and index != self.top:
			self.temp = self.songList[index]
			self.songList[index] = self.songList[index+1]
			self.songList[index].setIndex(index)
			self.songList[index+1] = self.temp 
			self.songList[index + 1].setIndex(index + 1)
	
	def rearrangeDownvote(self, index):
		if self.songList[index].getVoteCount() < self.songList[index-1].getVoteCount() and index != 0:
			self.temp = self.songList[index]
			self.songList[index] = self.songList[index-1]
			self.songList[index].setIndex(index)
			self.songList[index-1] = self.temp
			self.songList[index-1].setIndex(index-1) 

	def getTopSong(self):
		return self.songList[len(self.songList) - 1]

	def getList(self):
		return self.songList

	def getSize(self):
		return len(self.songList) - 1


