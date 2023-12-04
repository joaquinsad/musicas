from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('artistas', __name__, url_prefix="/artistas")

@bp.route('/')
def index():
    db = get_db()
    artistas = db.execute(
        """SELECT ar.name as artistas, COUNT(ar.name) as albums 
        from albums a join artists ar on a.ArtistId = ar.ArtistId
        group by ar.ArtistId WHERE artistId = ?""",(id,)
    ).fetchall()
    return render_template('artista/index.html', artistas=artistas)

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
        """SELECT name as nombre from tracks
        where AlbumId = ?""",(id,)
    ).fetchall()

    return render_template('artista/detalle.html', album=album, canciones=canciones)
#---------------------------jsonify-------------------------------------
bpapi = Blueprint('artista', __name__, url_prefix="api/artista")

@bpapi.route('/')
def index():
    db = get_db()
    artista = db.execute(
        """SELECT ar.name as artista, COUNT(ar.name) as albums 
        from albums a join artists ar on a.ArtistId = ar.ArtistId
        group by ar.ArtistId"""
    ).fetchall()
    return jsonify('artista/index.html', artista=artista)