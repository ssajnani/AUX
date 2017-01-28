from flask import Blueprint, render_template, request
import mysql.connector
room_api = Blueprint('room_api', __name__, template_folder="templates")

@room_api.route('/roomoptions')
def roomOpts():
	return render_template('roomMainPage.html')

@room_api.route('/addroom')
def newRoom(room=None):
	return render_template('formroomadd.html', room=room)

@room_api.route('/roomadded', methods = ["POST"])
def submitRoom():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	insert_stmt = (
		"INSERT INTO TheatreRoom (RoomNumber, Capacity)  "
		"VALUES (%s, %s)"
		)
	data = (request.form['num'], request.form['capacity'])
	data2 = (request.form['num'],)

	if (request.form['num'] == "" or request.form['num'] == None):
		return render_template('addNum.html')

	if (request.form['capacity'] == "" or request.form['capacity'] == None):
		return render_template('addCap.html')

	sel_stmt = (
		"SELECT * from TheatreRoom "
		"where RoomNumber= %s"
		)

	cursor.execute(sel_stmt, data2)

	if cursor.fetchone():
		return render_template('roomAlreadyExists.html')
	cursor.execute(insert_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('addedRoom.html', num=request.form['num'], capacity=request.form['capacity'])
		
@room_api.route('/deleteroom')
def oldRoom(room=None):
        return render_template('formroomdelete.html', room=room)

@room_api.route('/roomdelete', methods = ["POST"])
def deleteRooom():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre', buffered=True)
	cursor = cnx.cursor()
	del_stmt = (
		"DELETE FROM TheatreRoom "
		"where RoomNumber = %s"
		)
	data = (request.form['num'],)
	
	if (request.form['num'] == "" or request.form['num'] == None):
		cnx.close()
		return render_template('addNum.html')
	
	sel_stmt = (
		"SELECT * from TheatreRoom "
		"where RoomNumber = %s"
		)

	cursor.execute(sel_stmt, data)
	
	if not cursor.fetchone():
		cnx.close()
		return render_template('noSuchRoom.html')

	sel_stmt2 = (
		"SELECT * from Showing where TheatreRoom_RoomNumber = %s")
	
	cursor.execute(sel_stmt2, data)

	if cursor.fetchone():
		cnx.close()
		return render_template('roomInUse.html')

	cursor.execute(del_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('successfulRoomDelete.html', num = request.form['num'])

@room_api.route('/modifyroom')
def changeRoom(room=None):
        return render_template('formroomchange.html',room=room)

@room_api.route('/roommodified', methods = ["POST"])
def modifyRoom():

        cnx = mysql.connector.connect(user='root', database='MovieTheatre')
        cursor = cnx.cursor()
        modify_stmt = (
                        "UPDATE TheatreRoom SET Capacity=%s"
                        "WHERE RoomNumber= %s"
                        )
        data = (request.form['capacity'], request.form['num'])
        if (request.form['num'] == None or request.form['num'] == ""):
                return render_template('addNum.html')
        cursor.execute(modify_stmt, data)
        cnx.commit()
        cnx.close()
        return render_template('successfulRoomModified.html', num=request.form['num'], cap=request.form['capacity'])



@room_api.route('/listrooms')
def listAllRooms():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from TheatreRoom")
	cursor.execute(query)
	rooms=cursor.fetchall()
	cnx.close()
	return render_template('listofrooms.html', rooms=rooms)

