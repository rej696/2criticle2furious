from flask import (
    Blueprint, render_template)

from criticle.db import get_db
from criticle.utilities import get_reviews


# create blueprint
bp = Blueprint('home', __name__, url_prefix='/')


@bp.route("/")
@bp.route("/home")
def view():
    db = get_db()
    users = []
    for row in db.execute('select username from users').fetchall():
        users.append(row['username'])
    
    # Get reviews from database
    reviews_query = db.execute('select * from reviews order by upload_date desc').fetchall()
    reviews = get_reviews(db, reviews_query)

    input = {'users': users, 'reviews': reviews}

    return render_template('home/home.j2', input=input)