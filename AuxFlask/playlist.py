from flask import Blueprint, render_template, request
playlist_api = Blueprint('playlist_api', __name__, template_folder="templates")


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



@playlist_api.route('/listattend')
def listAllAttendancess():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT Attend.Customer_idCustomer as `Customer ID`, Attend.Showing_idShowing as `Showing ID`, Attend.Rating as `Rating`, "
			"Customer.FirstName as `First Name`, Customer.LastName as `Last Name`, Movie.MovieName as `Movie Name`, Movie.idMovie as `Movie ID` "
			"from Attend left join Customer on Attend.Customer_idCustomer = Customer.idCustomer "
			"left join Showing on Attend.Showing_idShowing = Showing.idShowing "
			"left join Movie on Showing.Movie_idMovie = Movie.idMovie order by Attend.Rating" )
	cursor.execute(query)
	atts=cursor.fetchall()
	cnx.close()
	return render_template('listofatts.html', atts = atts)

