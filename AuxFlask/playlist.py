
class playlist(object):
	def __init__(self, auxCode):
		self.code = auxCode
		self.songList = []
		self.top = len(songList) - 1

	def addSong(self, song):
		self.append(song)
		self.top += 1

	def removeSong(self):
		self.songList.pop(self.top)
		self.top -= 1

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

	def getTopSong():
		return self.songList[self.top]