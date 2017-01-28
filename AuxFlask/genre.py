from flask import Blueprint, render_template, request
import mysql.connector
genre_api = Blueprint('genre_api', __name__, template_folder="templates")

@genre_api.route('/genreoptions')
def genreOpts():
	return render_template('genreMainPage.html')

@genre_api.route('/addgenre')
def newGenre(genre=None):
	return render_template('formgenre.html', genre=genre)

@genre_api.route('/genreadded', methods = ["POST"])
def submitGenre():

	
		cnx = mysql.connector.connect(user='root', database='MovieTheatre')
		cursor = cnx.cursor()
		insert_stmt = (
			"INSERT INTO Genre (Genre, Movie_idMovie)  "
			"VALUES (%s, %s)"
			)
		data = (request.form['genre'], request.form['mid'])
		#print(request.form['genre'])
		if (request.form['genre'] == "" or request.form['genre'] == None):
			return render_template('addGenre.html')
		if (request.form['mid'] == "" or request.form['mid'] == None):
			return render_template('addMid.html')
		sel_stm = (
			"SELECT * from Movie where idMovie = %s" 
			)
		data2 = (request.form['mid'],)
		cursor.execute(sel_stm, data2)
		if not cursor.fetchone():
			return render_template('invalidMovieID.html')
		sel_stmt = (
			"SELECT * from Genre where Genre = %s and Movie_idMovie = %s"
			)
		cursor.execute(sel_stmt, data)
		if cursor.fetchone():
			return render_template('movieAndGenreExist.html')
		cursor.execute(insert_stmt, data)
		cnx.commit()
		cnx.close()
		return render_template('addedGenre.html', genre=request.form['genre'], mid=request.form['mid'])
		#return render_template('defaultTemp.html')
		
@genre_api.route('/deletegenre')
def oldGenre(genre=None):
        return render_template('formgenredelete.html', genre=genre)

@genre_api.route('/genredelete', methods = ["POST"])
def deleteGenre():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre', buffered=True)
	cursor = cnx.cursor()
	del_stmt = (
		"DELETE FROM Genre "
		"where Movie_idMovie = %s and Genre = %s"
		)
	data = (request.form['mid'], request.form['genre'])
	
	if (request.form['mid'] == "" or request.form['mid'] == None):
		cnx.close()
		return render_template('addMid.html')

	if (request.form['genre'] == "" or request.form['genre'] == None):
		cnx.close()
		return render_template('addGenre.html')
	
	sel_stmt = (
		"SELECT * from Genre "
		"where Movie_idMovie = %s and Genre = %s"
		)

	cursor.execute(sel_stmt, data)
	
	if cursor.rowcount == 0:
		return render_template('noSuchMovies.html')

	cursor.execute(del_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('successfulGenreDelete.html', mid = request.form['mid'], genre=request.form['genre'])

@genre_api.route('/listallgenres')
def listAllGenres():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT MovieName, Genre from Genre natural join Movie where Movie_idMovie = idMovie ORDER BY Genre")
	cursor.execute(query)
	genres=cursor.fetchall()
	cnx.close()
	return render_template('listofgenres.html', genres=genres)

