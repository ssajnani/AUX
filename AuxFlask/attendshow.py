import os
from flask import Blueprint, render_template, request
import datetime
import mysql.connector
attendshow_api = Blueprint('attendshow_api', __name__, template_folder="templates")

@attendshow_api.route('/attendshow')
def listAll():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Customer ORDER BY FirstName")
	cursor.execute(query)
	customers=cursor.fetchall()
	query = ("SELECT Showing.idShowing, Movie.MovieName, Showing.ShowingDateTime from Showing, Movie where Showing.Movie_idMovie = Movie.idMovie order by Showing.ShowingDateTime")
	cursor.execute(query)
	showings = cursor.fetchall()
	cnx.close()
	return render_template('attendshow.html', customers=customers, showings=showings)
 

def newSearch(showings=None):
        return render_template('attendshow.html', showings=showings)


@attendshow_api.route('/attendingshowing', methods = ["POST"])
def getShowings():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	customerID = request.form['customerID']
	showingID = request.form['showingID']

	check_stmt = (
		"Select * from Attend where Attend.Customer_idCustomer = %s and Attend.Showing_idShowing = %s" 
	)
	data = (customerID, showingID)
	cursor.execute(check_stmt, data)
	check = cursor.fetchall()
	if len(check) >= 1:
		error = "You are already going to that showing."
		return render_template("unsuccess.html", error = error)    
	sel_stmt = (
		"select Showing.idShowing, Movie.MovieName, Showing.ShowingDateTime"
		", TheatreRoom.Capacity, count(Customer.idCustomer) "
		"from Movie, Customer, Genre, Showing, Attend, TheatreRoom "
		"where Movie.idMovie = Genre.Movie_idMovie and Showing.Movie_idMovie "
		" = Movie.idMovie and Attend.Showing_idShowing = %s " 
		"and TheatreRoom.RoomNumber = Showing.TheatreRoom_RoomNumber " 
		"and Customer.idCustomer = Attend.Customer_idCustomer "
		"and Showing.idShowing = %s group by Showing.idShowing"
	)
	data = (showingID, showingID)
	cursor.execute(sel_stmt, data)
	select = cursor.fetchall()
	for row in select:
		if row[4] >= row[3]:
			error = "Sorry, the showing is fully booked."
			return render_template("unsuccess.html", error = error)
	
	insert_stmt = (
		"INSERT INTO Attend VALUES (%s, %s, NULL)"
	) 
	data = (customerID, showingID)
	cursor.execute(insert_stmt, data)
	cnx.commit()
	cnx.close()
	statement = "You have successfully bought tickets to the showing."
	return render_template('success.html', statement = statement)

@attendshow_api.route('/rate')
def listName():
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        query = ("SELECT * from Customer ORDER BY FirstName")
        cursor.execute(query)
        customers=cursor.fetchall()
        cnx.close()
        return render_template('rate.html', customers=customers)

def showings(showings=None):
        return render_template('rate.html', showings=showings)


@attendshow_api.route('/rateshowing', methods = ["POST"])
def listShowing():
	cnx =  mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	customerID = request.form['customerID']
	custsel_stmt = (
		"select * from Customer where Customer.idCustomer = %s "
	)
	cursor.execute(custsel_stmt, (customerID,))
	customers = cursor.fetchall()
	
	sel_stmt = (
		"Select Showing.idShowing, Movie.MovieName, Showing.ShowingDateTime "
		"from Showing, Customer, Attend, Movie where Movie.idMovie "
		"= Showing.Movie_idMovie and Customer.idCustomer "
		"= Attend.Customer_idCustomer and Customer.idCustomer = %s"
		" and Showing.idShowing "
		"= Attend.Showing_idShowing"
	)
	data = (customerID,)
	cursor.execute(sel_stmt, data)
	showings = cursor.fetchall()
	if len(showings) == 0:
		error = "You have not been to any showings yet."
		return render_template("unsuccess.html", error = error)
	cnx.close()
	return render_template('rateshowing.html', customers = customers, showings=showings)


@attendshow_api.route('/ratedshowing', methods = ["POST"])
def rateShowings():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	customerID = request.form['customerID']
	showingID = request.form['showingID']
	rating = request.form['rating']
	update_stmt = (
		"update Attend set Rating = %s where Attend.Customer_idCustomer = "
		"%s and Attend.Showing_idShowing = %s"	
        )
	data = (rating, customerID, showingID)
	cursor.execute(update_stmt, data)
	statement = "The rating for this show was updated."
	return render_template("success.html", statement = statement)

@attendshow_api.route('/customerselection')
def nameSel():
        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        query = ("SELECT * from Customer ORDER BY FirstName")
        cursor.execute(query)
        customers=cursor.fetchall()
        cnx.close()
        return render_template('custsel.html', customers=customers)

def cusShowings(showings=None):
        return render_template('custsel.html', showings=showings)


@attendshow_api.route('/movierating', methods = ["POST"])
def showing():
	cnx =  mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	customerID = request.form['customerID']
	sel_stmt = (
		"Select Showing.idShowing, Movie.MovieName, Attend.Rating "
		"from Showing, Customer, Attend, Movie where Movie.idMovie "
		"= Showing.Movie_idMovie and Customer.idCustomer "
		"= Attend.Customer_idCustomer and Customer.idCustomer = %s"
		" and Showing.idShowing = Attend.Showing_idShowing"
	)
	data = (customerID,)
	cursor.execute(sel_stmt, data)
	showings = cursor.fetchall()
	if len(showings) == 0:
		error = "You have not watched any shows yet."
		return render_template("unsuccess.html", error = error)
	cnx.close()
	return render_template('custratings.html', showings=showings)

@attendshow_api.route('/custinfosel')
def selName():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Customer ORDER BY FirstName")
	cursor.execute(query)
	customers=cursor.fetchall()
	cnx.close()
	return render_template('custinfosel.html', customers=customers)

def customers(showings=None):
        return render_template('custinfosel.html', showings=showings)


@attendshow_api.route('/custinfo', methods = ["POST"])
def custinfo():
	cnx =  mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	customerID = request.form['customerID']
	sel_stmt = (
		"Select * from Customer where Customer.idCustomer = %s"
	)
	data = (customerID,)
	cursor.execute(sel_stmt, data)
	customers = cursor.fetchall()
	sel_stmt = (
		"Select * from Attend where Attend.Customer_idCustomer = %s"
	)
	data = (customerID,)
	cursor.execute(sel_stmt, data)
	showings = cursor.fetchall()

	return render_template('custinfo.html', customers=customers, showings=showings)
