from flask import  Blueprint, render_template, request

song_api = Blueprint('song_api', __name__, template_folder="templates")

@song_api.route('/movieoptions')
def listOpts():
	return render_template('movieMainPage.html')

@song_api.route('/addmovie')
def newMovie(movie=None):
	return render_template('formmovie.html', movie=movie)

@song_api.route('/moviesubmit', methods = ["POST"])
def submitSong():


		
@song_api.route('/modifymovie')
def changeMovie(movie=None):
        return render_template('formmoviemodify.html',movie=movie)

@song_api.route('/moviemodified', methods = ["POST"])
def modifyMovie():

	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	modify_stmt = (
			"UPDATE Movie SET MovieName=%s, MovieYear=%s"
			"WHERE idMovie= %s"
			)
	data = (request.form['name'], request.form['year'], request.form['id'])
	if (request.form['id'] == None or request.form['id'] == ""):
		return render_template('addMid.html') 
	if (request.form['name'] == None or request.form['name'] == ""):
		return render_template('addMovieName.html')
	cursor.execute(modify_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('indexmodify.html', name=request.form['name'], year=request.form['year'], id = request.form['id']) 


@song_api.route('/deletemovie')
def oldMovie(movie=None):
	return render_template('formmoviedelete.html', movie=movie)

@song_api.route('/moviedelete', methods = ["POST"])
def deleteMovie():
	cnx = mysql.connector.connect(user='root', database = 'MovieTheatre')
	cursor = cnx.cursor()
	del_stmt = (
		"DELETE FROM Movie "
		"where idMovie = %s "
		)
	data = (request.form['id'],)

	cursor.execute(del_stmt, data)
	cnx.commit()
	cnx.close()
	return render_template('index2.html',  id=request.form['id'])

@song_api.route('/listallmovies') 
def listAll():
	cnx = mysql.connector.connect(user='root', database='MovieTheatre')
	cursor = cnx.cursor()
	query = ("SELECT * from Movie GROUP BY MovieName")
	cursor.execute(query)
	movies=cursor.fetchall()
	cnx.close()
	return render_template('listofmovies.html', movies=movies)

