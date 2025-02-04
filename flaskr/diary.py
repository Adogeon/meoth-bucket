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
        'SELECT * '
        'FROM transaction t JOIN user u ON t.user_id = u.id '
        'ORDER BY created DESC'
    ).fetchall()
    return render_template('diary/index.html', transations=transactions)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        name = request.form['name']
        amount = request.form['amount']
        category = request.form['category']
        error = None

        if not name:
            error = 'Transaction name is required'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO transaction (name, amount, category, user_id)'
                'VALUES (?, ?, ?)',
                (name, amount, category, g.user['id'])
            )
            db.commit()
            return redirect(url_for('diary.index'))

    return render_template('diary/create.html')
