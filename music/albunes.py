from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort
from music import artista


from music.db import get_db

bp = Blueprint('albums', __name__, url_prefix="/albums")
bpapi = Blueprint('albums', __name__, url_prefix="/api/albums")


@bp.route('/')
def index():
    db = get_db()
    albums = db.execute(
        """SELECT  a.albumId as id, a.title as titulo, ar.name as nombre FROM albums a JOIN artists ar on  ar.ArtistId = a.ArtistId JOIN tracks t on t.AlbumId = a.AlbumId
    GROUP BY a.AlbumId"""
    ).fetchall()
    return render_template('albums/index.html', albums=albums)

@bp.route('/<int:id>/detalle', methods=('GET', 'POST'))
def detalle(id):
    db = get_db()
    album = db.execute(
        """SELECT  a.AlbumId,COUNT(t.name) as canciones ,a.title as titulo,
        ar.name as nombre FROM albums a JOIN artists ar on 
        ar.ArtistId = a.ArtistId JOIN tracks t on t.AlbumId = a.AlbumId
        WHERE a.AlbumId = ?""", 
        (id,)
    ).fetchone()
   
    canciones = db.execute(
        """SELECT TrackId, name as nombre from tracks
        where AlbumId = ?""",(id,)
    ).fetchall()

    return render_template('albums/detalle.html', album=album, canciones=canciones)

#----------------------------------jsnon----------------------------------
@bpapi.route('/')
def index():
    db = get_db()
    albums = db.execute(
        """SELECT  COUNT(t.name) as canciones ,a.title as titulo, ar.name as nombre FROM albums a JOIN artists ar on  ar.ArtistId = a.ArtistId JOIN tracks t on t.AlbumId = a.AlbumId
GROUP BY a.AlbumId"""
    ).fetchall()
    return jsonify(albums=albums)

@bpapi.route('/<int:id>/detalle', methods=('GET', 'POST'))
def detalle(id):
    db = get_db(id)
    artista = db.execute(
        """SELECT ar.ArtistId, al.Title as titulo,ar.name as nombre from albums al 
        join artists ar on al.ArtistId = ar.ArtistId"""
    ).fetchall()
   
    albums = db.execute(
        """SELECT  a.AlbumId,COUNT(t.name) as canciones ,a.title as titulo,
        ar.name as nombre FROM albums a JOIN artists ar on 
        ar.ArtistId = a.ArtistId JOIN tracks t on t.AlbumId = a.AlbumId
        GROUP BY a.AlbumId"""
    ).fetchone()

    return jsonify(albums=albums, artista=artista)
