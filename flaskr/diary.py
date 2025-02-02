from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask.auth import login_required
from flask.db import get_db

bp = Blueprint('diary', __name__)


@bp.route('/')
def index():
    db = get_db()
    transactions = db.execture(
        'SELECT * FROM transaction t JOIN user u ON t.user_id = u.id ORDER BY created DESC'
    ).fetchall()
    return render_template('diary/index.html', transations=transactions)
