from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('music', __name__)

@bp.route('/')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name as cancion,g.name as genero, a.title as disco, ar.name as artista  
        FROM tracks t join genres  g on g.GenreId = t.GenreId
        join albums a on t.AlbumId = a.AlbumId  join artists ar on ar.ArtistId = a.ArtistId"""
    ).fetchall()
    return render_template('music/index.html', canciones=canciones)

bpapi = Blueprint('music', __name__)

@bpapi.route('api/')
def index():
    db = get_db()
    canciones = db.execute(
        """SELECT t.name as cancion,g.name as genero, a.title as disco, ar.name as artista  
        FROM tracks t join genres  g on g.GenreId = t.GenreId
        join albums a on t.AlbumId = a.AlbumId  join artists ar on ar.ArtistId = a.ArtistId"""
    ).fetchall()
    return jsonify(canciones=canciones)