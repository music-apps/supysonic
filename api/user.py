# coding: utf-8

from flask import request
from web import app
from db import User

@app.route('/rest/getUser.view')
def user_info():
	username = request.args.get('username')
	if username is None:
		return request.formatter({
			'error': {
				'code': 10,
				'message': 'Missing username'
			}
		}, error = True)

	user = User.query.filter(User.name == username).first()
	if user is None:
		return request.formatter({
			'error': {
				'code': 0,
				'message': 'Unkwown user'
			}
		}, error = True)

	return request.formatter({
		'user': {
			'username': user.name,
			'email': user.mail,
			'scrobblingEnabled': False,
			'adminRole': user.admin,
			'settingsRole': False,
			'downloadRole': False,
			'uploadRole': False,
			'playlistRole': False,
			'coverArtRole': False,
			'commentRole': False,
			'podcastRole': False,
			'streamRole': False,
			'jukeboxRole': False,
			'shareRole': False
		}
	})

