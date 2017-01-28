from flask import Blueprint, render_template, request
import datetime
import mysql.connector
from werkzeug.utils import secure_filename
select_api = Blueprint('genre_api', __name__, template_folder="templates")


@select_api.route('/selectshowing')
def listAll():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Genre GROUP BY Genre")
	cursor.execute(query)
	genres=cursor.fetchall()
	query = ("SELECT CAST(ShowingDateTime as DATE) from Showing order by ShowingDateTime")
	cursor.execute(query)
	showings = cursor.fetchall()
	cnx.close()
	return render_template('select.html', genres=genres, showings=showings)


def newSearch(showings=None):
        return render_template('select.html', showings=showings)


@select_api.route('/searchedshowing', methods = ["POST"])
def getShowings():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()

	name = request.form['name']
	genre = request.form['genre']
	end = request.form['end']
	start = request.form['start']
	seating = request.form['seating']
	
	if name == "" or name == None:
		if seating == "0":
			sel_stmt = (
				"select Showing.idShowing, Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity, count(Customer.idCustomer) from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s group by Showing.idShowing"
			)
			data = (start, end, genre)    
		else:
			sel_stmt = (
				"select * from (select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity as capacity, count(Customer.idCustomer) as number from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s) as showings where showings.number < showings.capacity"
			)
			data = (start, end, genre)
	else:
		if seating == "0": 
			sel_stmt = (
				"select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity, count(Customer.idCustomer) from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s and Movie.MovieName = %s group by Showing.idShowing"
			)
			data = (start, end, genre, name)
		else:
			sel_stmt = (
				"select * from (select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity as capacity, count(Customer.idCustomer) as number from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s and Movie.MovieName = %s) as showings where showings.number < showings.capacity"
			
			)
			data = (start, end, genre, name)

	cursor.execute(sel_stmt, data)
	showings = cursor.fetchall()

	if len(showings) == 0:
		error = "No showings found."
		cnx.close()
		return render_template('unsuccess.html', error = error)
	else:
		cnx.commit()
		cnx.close()
		return render_template('showings.html', showings=showings)

@select_api.route('/sqlinjection')
def listAll():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Genre GROUP BY Genre")
	cursor.execute(query)
	genres=cursor.fetchall()
	query = ("SELECT CAST(ShowingDateTime as DATE) from Showing order by ShowingDateTime")
	cursor.execute(query)
	showings = cursor.fetchall()
	cnx.close()
	return render_template('select.html', genres=genres, showings=showings)


def newSearch(showings=None):
        return render_template('select.html', showings=showings)


@select_api.route('/injecting', methods = ["POST"])
def getShowings():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()

	name = request.form['name']
	genre = request.form['genre']
	end = request.form['end']
	start = request.form['start']
	seating = request.form['seating']
	
	if name == "" or name == None:
		if seating == "0":
			sel_stmt = (
				"select Showing.idShowing, Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity, count(Customer.idCustomer) from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s group by Showing.idShowing"
			)
			data = (start, end, genre)    
		else:
			sel_stmt = (
				"select * from (select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity as capacity, count(Customer.idCustomer) as number from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s) as showings where showings.number < showings.capacity"
								
					)
			data = (start, end, genre)
	else:
		if seating == "0": 
			sel_stmt = (
				"select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity, count(Customer.idCustomer) from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and Movie.MovieName = '" + name + "' and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s group by Showing.idShowing"
			)
			data = (start, end, genre,)
		else:
			sel_stmt = (
				"select * from (select Showing.idShowing,  Movie.MovieName, Showing.ShowingDateTime, TheatreRoom.Capacity as capacity, count(Customer.idCustomer) as number from Movie, Customer, Genre, Showing, Attend, TheatreRoom where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie = Movie.idMovie and Attend.Showing_idShowing = Showing.idShowing and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber and Customer.idCustomer = Attend.Customer_idCustomer and Movie.MovieName = '" + name + "' and CAST(Showing.ShowingDateTime as DATE) >= %s and CAST(Showing.ShowingDateTime as DATE) <= %s and Genre.Genre = %s) as showings where showings.number < showings.capacity"
			
			)
			data = (start, end, genre,)

	cursor.execute(sel_stmt, data)
	showings = cursor.fetchall()

	if len(showings) == 0:
		error = "No showings found."
		cnx.close()
		return render_template('unsuccess.html', error = error)
	else:
		cnx.commit()
		cnx.close()
		return render_template('showings.html', showings=showings)