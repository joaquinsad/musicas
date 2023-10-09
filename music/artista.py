from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('artista', __name__, url_prefix="/artista")

@bp.route('/')
def index():
    db = get_db()
    artista = db.execute(
        """SELECT ar.name as artista, COUNT(ar.name) as albums 
        from albums a join artists ar on a.ArtistId = ar.ArtistId
        group by ar.ArtistId"""
    ).fetchall()
    return render_template('artista/index.html', artista=artista)