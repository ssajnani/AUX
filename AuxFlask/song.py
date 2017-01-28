import spotipy

# Song class to represent Spotify track info in a prettier format.
class Song():

	def __init__(self, spotifyObject, spotifyID):

		self.voteCount = 0
		self.spotifyID = ''
		self.sp = spotifyObject
		self.title = ''
		self.artist = ''
		self.album = ''
		self.songLength = 0
		self.songInfo = []
		self.id = spotifyID
		self.getInfo()
		
	def findInfo(self):

		song = self.sp.track(spotifyID)

		self.title = song['artists'][0]['name']
		self.artist = song['name']
		self.songLength = int(song['duration_ms'])
		self.album = song['album']['name']
		self.songInfo = [self.title, self.artist, self.songLength, self.album]

	def getInfo(self):
		return self.songInfo

	def upvote(self):
		self.voteCount = self.voteCount + 1

	def downvote(self):
		self.voteCount = self.voteCount - 1

	def getVoteCount(self):
		return self.voteCount