from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('blog', __name__)

@bp.route('/')
def index():
    db = get_db()
    canciones = db.execute(
        'SELECT t.name as cancion,g.name as genero, a.Title as titulo, a.title as disco, ar.name as nombre  FROM tracks t join genres  g on g.GenreId = t.GenreId
        'join albums a on t.AlbumId = a.AlbumId  join artists ar on ar.ArtistId = a.ArtistId'
    ).fetchall()
    return render_template('blog/index.html', canciones=canciones)
