from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort


from music.db import get_db

bp = Blueprint('albums', __name__, url_prefix="/albums")

@bp.route('/')
def index():
    db = get_db()
    albunes = db.execute(
        """SELECT  COUNT(t.name) as canciones ,a.title as titulo, ar.name as nombre FROM albums a JOIN artists ar on  ar.ArtistId = a.ArtistId JOIN tracks t on t.AlbumId = a.AlbumId
GROUP BY a.AlbumId"""
    ).fetchall()
    return render_template('albums/index.html', albunes=albunes)
