# API Keys and Settings.

import os

# Set variables specific to our application.
def setKeys():
	os.environ['SPOTIPY_CLIENT_ID'] = '2421a4b55e5c457eb279cacbacb9d318'
	os.environ['SPOTIPY_CLIENT_SECRET'] = '97d2682f52c44db6ab68a812d72e59c0'
	os.environ['SPOTIPY_REDIRECT_URI'] = 'http://publish.uwo.ca/~amccan5/'
