from flask import  Blueprint, render_template, request
from spotify import Spotify_API
import sys
import spotipy
import spotipy.util as util
import os
import song
import settings



authorization_api = Blueprint('authorization_api', __name__, template_folder="templates")




@authorization_api.route('/host')
def listOpts():
	return render_template('host.html')

@authorization_api.route('/username')
def newUsername(info=None):
	return render_template('formusername.html', info = info)

userCatalogue = {}
userCode = {}

spot = []

code = None

user = None

@authorization_api.route('/usersubmit', methods = ["POST"])
def submitUsername():
		
	username = request.form['username']
	if (request.form['username'] == "" or request.form['username'] == None):
		return render_template('unsuccess.html')
	if (request.form['auxcode'] == "" or request.form['auxcode'] == None):
		return render_template('unsuccess.html')	
	if (request.form['name'] == "" or request.form['name'] == None):
		spot.append(Spotify_API(request.form['username'], request.form['auxcode']))
		spot[-1].authorizeUser(request.form['username'])
		
	else:
		spot.append(Spotify_API(request.form['username'], request.form['auxcode'], request.form['name']))
		spot[-1].authorizeUser(request.form['username'])

	

	if spot[-1].isAuthorized():
		code = request.form['auxcode']
		user = username
		userCatalogue[request.form['auxcode']] = spot
		userCode[request.form['username']] = request.form['auxcode']
		songs = spot[-1].getList()
		size = spot[-1].getSize()
		return render_template('playlist.html', code = code, username = username, songs = songs, size = size)


