# coding: utf-8

from flask import request
from sqlalchemy import desc
from sqlalchemy.orm import aliased
import random
import uuid

from web import app
from db import Track, Folder

@app.route('/rest/getRandomSongs.view', methods = [ 'GET', 'POST' ])
def rand_songs():
	size = request.args.get('size', '10')
	genre, fromYear, toYear, musicFolderId = map(request.args.get, [ 'genre', 'fromYear', 'toYear', 'musicFolderId' ])

	try:
		size = int(size) if size else 10
		fromYear = int(fromYear) if fromYear else None
		toYear = int(toYear) if toYear else None
		fid = uuid.UUID(musicFolderId) if musicFolderId else None
	except:
		return request.error_formatter(0, 'Invalid parameter format')

	query = Track.query
	if fromYear:
		query = query.filter(Track.year >= fromYear)
	if toYear:
		query = query.filter(Track.year <= toYear)
	if genre:
		query = query.filter(Track.genre == genre)
	if fid:
		query = query.filter(Track.root_folder_id == fid)
	tracks = query.all()

	if not tracks:
		return request.formatter({ 'randomSongs': {} })

	return request.formatter({
		'randomSongs': {
			'song': [ random.choice(tracks).as_subsonic_child() for x in xrange(size) ]
		}
	})

@app.route('/rest/getAlbumList.view', methods = [ 'GET', 'POST' ])
def album_list():
	ltype, size, offset = map(request.args.get, [ 'type', 'size', 'offset' ])
	try:
		size = int(size) if size else 10
		offset = int(offset) if offset else 0
	except:
		return request.error_formatter(0, 'Invalid parameter format')

	query = Folder.query.filter(Folder.tracks.any())
	if ltype == 'random':
		albums = query.all()
		return request.formatter({
			'albumList': {
				'album': [ random.choice(albums).as_subsonic_child() for x in xrange(size) ]
			}
		})
	elif ltype == 'newest':
		query = query.order_by(desc(Folder.created))
	elif ltype == 'highest':
		return request.error_formatter(0, 'Not implemented')
	elif ltype == 'frequent':
		return request.error_formatter(0, 'Not implemented')
	elif ltype == 'recent':
		return request.error_formatter(0, 'Not implemented')
	elif ltype == 'starred':
		return request.error_formatter(0, 'Not implemented')
	elif ltype == 'alphabeticalByName':
		query = query.order_by(Folder.name)
	elif ltype == 'alphabeticalByArtist':
		parent = aliased(Folder)
		query = query.join(parent, Folder.parent).order_by(parent.name).order_by(Folder.name)
	else:
		return request.error_formatter(0, 'Unknown search type')

	return request.formatter({
		'albumList': {
			'album': [ f.as_subsonic_child() for f in query.limit(size).offset(offset) ]
		}
	})

