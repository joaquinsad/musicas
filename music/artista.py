from flask import (
    Blueprint, flash, g, redirect, jsonify, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('artista', __name__, url_prefix="/artistas")

@bp.route('/')
def index():
    db = get_db()
    artista = db.execute(
        """SELECT artistId as id, name as artista
         from artists ORDER BY artista"""
    ).fetchall()
    return render_template('artista/index.html', artista=artista)

@bp.route('/<int:id>/detalle', methods=('GET', 'POST'))
def detalle(id):
    db = get_db()
    artista = db.execute(
        """SELECT artistId as id, name as nombre_del_artista from artists
        where ArtistId = ?""", 
        (id,)
    ).fetchone()
   
    albums = db.execute(
        """SELECT albumId as id, Title as nombre_del_album from albums
        where ArtistId = ?""",(id,)
    ).fetchall()

    return render_template('artista/detalle.html', artista=artista, albums=albums)
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