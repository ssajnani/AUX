from flask import Blueprint, render_template, request

playlist_api = Blueprint('playlist_api', __name__, template_folder="templates")


@playlist_api.route('/addsong')
def songAdd(song=None):
	return render_template('songsearch.html')

@playlist_api.route('/songsearch')
def newSong(name=None):
	return render_template('songsearch.html', name = name)

@playlist_api.route('/songsearched', methods = ["POST"])
def songSearched():
	songname = request.form['name']

	if songname == "" or songname == None:
		return render_template('unsucces.html')

	songs = userCatalogue[code].search(songname)

	return render_template('songs.html', songs = songs)



@playlist_api.route('/songadd')
def addSong(song=None):
	return render_template('songs.html', song = song)

@playlist_api.route('/songadded')
def addedSong(song=None):
	song = request.form['song']

	userCatalogue[code].addSong(song)

	songs = userCatalogue[code].getList()
	size = userCatalogue[code].getSize()

	return render_template('playlist.html', username = user, songs = songs, size = size)





