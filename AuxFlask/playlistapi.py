from flask import Blueprint, render_template, request
playlist_api = Blueprint('playlist_api', __name__, template_folder="templates")

import playlist


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

