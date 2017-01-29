from flask import Blueprint, render_template, request
from authorization import spot, username
from song import Song



playlist_api = Blueprint('playlist_api', __name__, template_folder="templates")


@playlist_api.route('/addsong')
def songAdd(song=None):
	return render_template('playlist.html', song = song)

saved_songs = []

@playlist_api.route('/songsearched', methods = ['POST'])
def songSearched():
	songname = request.form['name']

	if songname == "" or songname == None:
		return render_template('unsuccess.html')

	global saved_songs
	
	saved_songs = spot[username[0]].search(songname)

	vals = []

	for song in saved_songs:
		vals.append(song.getName())

	return render_template('songs.html', vals = vals)



@playlist_api.route('/songadd')
def addSong(name=None):
	return render_template('songs.html', name = name)

@playlist_api.route('/songadded', methods = ['POST'])
def addedSong(name=None):
	name = request.form['name']
	for val in saved_songs:
		if name == val.getName():
			spot[username[0]].addSong(val)

	return render_template('playlist.html', code = spot[username[0]].getCode(), username = username[0], songs = spot[username[0]].getList())

	

@playlist_api.route('/removesong')
def removeSong(songs=None):
	return render_template('removesong.html', songs = spot[user].getList())

@playlist_api.route('/songdelete', methods = ['POST'])
def songDelete(songs=None):
	song = request.form['song']


	spot[username[0]].removeSong(song)


	return render_template('playlist.html', username = username[0], songs = spot[username[0]].getList())





