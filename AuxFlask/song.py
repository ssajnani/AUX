import spotipy

# Song class to represent Spotify track info in a prettier format.
class Song():

	def __init__(self, spotifyObject):

		self.index = 0
		self.title = spotifyObject['name']
		self.artist = spotifyObject['artists']
		self.songLength = int(spotifyObject['duration_ms'])
		self.songInfo = [self.title, self.artist, self.songLength]
		self.voteCount = 0

	def getName(self):
		return self.title

	def setIndex(self, index):
		self.index = index

	def getIndex(self):
		return self.index

	def getInfo(self):
		return self.songInfo

	def upvote(self):
		self.voteCount = self.voteCount + 1

	def downvote(self):
		self.voteCount = self.voteCount - 1

	def getVoteCount(self):
		return self.voteCount