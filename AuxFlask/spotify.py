
import sys
import spotipy
import spotipy.util as util
import os
import song
from settings import setKeys

class Spotify_API:

	def __init__(self, username, auxCode, playlistName = 'AuxPlaylist'):

		self.user = username
		self.sp = None
		self.authorizeUser(self.user)

		self.code = auxCode
		self.songList = []
		self.top = len(self.songList) - 1
		self.sp.user_playlist_create(username, playlistName, public = True)
		self.spPlaylist = self.sp.user_playlists(username, limit = 1, offset = 0)
		self.playListId = self.spPlaylist['items'][0]['uri']

	# Spotify functions.
	def search(self, query):

		searchResults = []
		results = self.sp.search(q = query, limit = 5, type = 'track')
		for track in results:
			song = Song(track['id'])
			searchResults.append(song)

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
		self.append(song)
		self.top += 1

	def removeSong(self):
		if top != 0:
			topSong = self.songList.pop(self.top)
			self.top -= 1
		self.sp.user_playlist_add_tracks(self.username, self.playListId, tracks = topSong.id, position = 0)

	def rearrangeUpvote(self, index):
		if self.songList[index].getVoteCount() > self.songList[index+1].getVoteCount() and index != self.top:
			self.temp = self.songList[index]
			self.songList[index] = self.songList[index+1]
			self.songList[index+1] = self.temp 
	
	def rearrangeDownvote(self, index):
		if self.songList[index].getVoteCount() < self.songList[index-1].getVoteCount() and index != 0:
			self.temp = self.songList[index]
			self.songList[index] = self.songList[index-1]
			self.songList[self.i-1] = self.temp 

	def getTopSong(self):
		return self.songList[self.top]

	def getList(self):
		return self.songList

	def getSize(self):
		return self.top


