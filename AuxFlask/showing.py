from flask import Blueprint, render_template, request
import mysql.connector
showing_api = Blueprint('showing_api', __name__, template_folder="templates")

@showing_api.route('/showingoptions')
def showingOpts():
	return render_template('showingMainPage.html')

@showing_api.route('/addshowing')
def newRoom(showing=None):
	return render_template('formshowingadd.html', showing=showing)

@showing_api.route('/showingadded', methods = ["POST"])
def submitShowing():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insert_stmt = (
		"INSERT INTO Showing (idShowing, ShowingDateTime, Movie_idMovie, TheatreRoom_RoomNumber, TicketPrice)  "
		"VALUES (%s, %s, %s, %s, %s)"
		)
	
	data = (request.form['sid'], request.form['time'],request.form['mid'],request.form['num'],request.form['price'])
	data2 = (request.form['sid'],)

	sel_stmt = (
		"SELECT * from Showing "
		"where idShowing= %s"
		)

	cursor.execute(sel_stmt, data2)

	if cursor.fetchone():
		return render_template('showingAlreadyExists.html')
	
	if (request.form['sid'] == "" or request.form['sid'] == None):
		return render_template('addSid.html')

#	if (request.form['time'] == "" or request.form['time'] == None):
#		return render_template('addTime.html')

	if (request.form['mid'] == "" or request.form['mid'] == None):
		return render_template('addMid.html')

	if (request.form['num'] == "" or request.form['num'] == None):
		return render_template('addNum.html')

	if (request.form['price'] == "" or request.form['price'] == None):
		return render_template('addPrice.html')
	
	cursor.execute(insert_stmt, data)
	
	cnx.commit()
	cnx.close()
	return render_template('addedShowing.html', sid=request.form['sid'])
		
@showing_api.route('/deleteshowing')
def oldShowing(showing=None):
        return render_template('formshowingdelete.html', showing=showing)

@showing_api.route('/showingdelete', methods = ["POST"])
def deleteShowing():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre', buffered=True)
	cursor = cnx.cursor()
	del_stmt = (
		"DELETE FROM Showing "
		"where idShowing = %s"
		)
	data = (request.form['sid'],)
	
	if (request.form['sid'] == "" or request.form['sid'] == None):
		cnx.close()
		return render_template('addSid.html')
	
	sel_stmt = (
		"SELECT * from Showing "
		"where idShowing = %s"
		)

	cursor.execute(sel_stmt, data)
	
	if not cursor.fetchone():
		cnx.close()
		return render_template('noSuchShowing.html')

	sel_stmt2 = (
		"SELECT * from Showing right join Attend on Showing.idShowing = Attend.Showing_idShowing where Showing.idShowing = %s"
		)
	cursor.execute(sel_stmt2, data)

	if cursor.fetchone():
		return render_template('showingBooked.html')
#check if showing will be attended

	cursor.execute(del_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('successfulShowingDelete.html', sid = request.form['sid'])

@showing_api.route('/modifyshowing')
def changeShowing(showing=None):
        return render_template('formshowingchange.html',showing=showing)

@showing_api.route('/showingmodified', methods = ["POST"])
def modifyShowing():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	modify_stmt = (
			"UPDATE Showing SET ShowingDateTime=%s, Movie_idMovie=%s, TheatreRoom_RoomNumber =%s, TicketPrice =%s "
			"WHERE idShowing = %s"
			)
	data = (request.form['time'], request.form['mid'], request.form['num'], request.form['price'], request.form['sid'])

#	if (request.form['time'] == None or request.form['time'] == ""):
#		return render_template('addTime.html')
	if (request.form['mid'] == None or request.form['mid'] == ""):
		return render_template('addMid.html')
	if (request.form['num'] == None or request.form['num'] == ""):
		return render_template('addNum.html')
	if (request.form['price'] == None or request.form['price'] == ""):
		return render_template('addPrice.html')
	if (request.form['sid'] == None or request.form['sid'] == ""):
		return render_template('addSid.html')
	cnx.commit()
	cnx.close()
	return render_template('successfulShowingModified.html', sid=request.form['sid'])


@showing_api.route('/listshowings')
def listAllShowings():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Showing order by ShowingDateTime")
	cursor.execute(query)
	shows=cursor.fetchall()
	cnx.close()
	return render_template('listofshowings.html', shows=shows)

