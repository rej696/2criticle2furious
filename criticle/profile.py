from criticle.auth import login_required
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, g)

from werkzeug.security import check_password_hash, generate_password_hash

from criticle.db import get_db
from criticle.auth import login_required
from criticle.review import Review


# create blueprint
bp = Blueprint('profile', __name__, url_prefix='/profile')

BANNED_KEYS = (
    'password',
    'id',
    'image_id'
)

def filter_profile_query(profile_query):
    profile_attrs = {}
    for key in profile_query.keys():
        if key not in BANNED_KEYS:
            profile_attrs[key] = profile_query[key]
    return profile_attrs


@bp.route('<string:category>/<string:title>/view_reviews', methods=('GET',))
def view_media_reviews(category, title):
    database = get_db()
    
    category_id = database.execute('select id from categories where media_type is ?', (category,)).fetchone()[0]

    profile_query = database.execute(f'select * from {category} where title is ?', (title,)).fetchall()[0]

    raw_reviews = database.execute('select * from reviews where media_id is ? and category_id is ?', (profile_query['id'], category_id)).fetchall()

    reviews = list(Review(database, review_raw) for review_raw in raw_reviews)

    profile_attrs = filter_profile_query(profile_query)

    summary = profile_attrs.pop('summary')

    return render_template('profile/media.j2', title=title.title(), reviews=reviews, profile_attrs=profile_attrs, summary=summary, page="media")


@bp.route('<string:username>/view_reviews', methods=('GET',))
def view_user_reviews(username):
    database = get_db()

    user_id = database.execute('select id from users where username is ?', (username, )).fetchone()[0]
    
    # Get database entries
    raw_reviews = database.execute('select * from reviews where user_id is ?', (user_id,)).fetchall()

    profile_attrs = filter_profile_query(database.execute('select * from users where id is ?', (user_id,)).fetchall()[0])

    summary = profile_attrs.pop('summary')

    reviews = list(Review(database, review_raw) for review_raw in raw_reviews)

    return render_template('profile/media.j2', title=username, reviews=reviews, profile_attrs=profile_attrs, summary=summary, page="user")


@login_required
@bp.route('<string:username>/add_review', methods=('GET', 'POST'))
def add_user_reviews(username):
    if get_db().execute(
        'select id from users where username is ?', (username,)
    ).fetchone()[0] != g.user['id']:
        flash(f"You do not have permission to add reviews as {username}")
        return redirect(url_for('home'))



    if request.method == 'POST':
        media_type = request.form['category'].lower()
        media_title = request.form['media_title'].lower()
        body = request.form['body']
        rating = int(request.form['rating'])
        
        db = get_db()
        error = None

        if db.execute(
            'select id from categories where media_type is ?',
            (media_type,)
        ).fetchone() is None:
            error = 'Category does not exist'
        elif db.execute(
            f'select id from {media_type} where title is ?',
            (media_title,)
        ).fetchone() is None:
            error = 'Title does not exist'
        elif rating > 30 or rating < 0:
            error = 'Rating must be a number between 0 - 30'
        
        if error is None:
            db.execute(
                f'''insert into reviews (category_id, media_id, user_id, body, rating) values (
                (select id from categories where media_type is ?),
                (select id from {media_type} where title is ?),
                (select id from users where username is ?),
                ?, ?)''',
                (media_type, media_title, username, body, rating,)
            )
            db.commit()

            return redirect(url_for('profile.view_user_reviews', username=username))
        
        flash(error)
    
    return render_template('profile/add_review.j2')
