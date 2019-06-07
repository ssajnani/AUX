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

spot = {}

username = []


@authorization_api.route('/usersubmit', methods = ["POST"])
def submitUsername():
	global spot
	global username

	username.insert(0, request.form['username'])
	if (request.form['username'] == "" or request.form['username'] == None):
		return render_template('unsuccess.html')
	if (request.form['auxcode'] == "" or request.form['auxcode'] == None):
		return render_template('unsuccess.html')	
	if username[0] in spot:
		return render_template('playlist.html', code = spot[username[0]].getCode, username = username[0], songs = spot[username[0]].getList())
	elif (request.form['name'] == "" or request.form['name'] == None):
		spot[username[0]] = Spotify_API(request.form['username'], request.form['auxcode'])
		spot[username[0]].authorizeUser(request.form['username'])
	else:
		spot[username[0]] = Spotify_API(request.form['username'], request.form['auxcode'], request.form['name'])
		spot[username[0]].authorizeUser(request.form['username'])

	
	if spot[username[0]].isAuthorized():
		return render_template('playlist.html', code = spot[username[0]].getCode(), username = username[0], songs = spot[username[0]].getList())


