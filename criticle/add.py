from sqlite3 import Connection
from typing import Dict
from datetime import datetime
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, g)

from criticle.db import get_db
from criticle.auth import login_required
from criticle.utilities import is_valid_date


# create blueprint
bp = Blueprint('add', __name__, url_prefix='/add')


@login_required
@bp.route('/review/<string:username>', methods=('GET', 'POST'))
def review(username):
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

            return redirect(url_for('profile.view_user_profile', username=username))
        
        flash(error)
    
    return render_template('add/add_review.j2')


def add_movie_to_database(db: Connection, request_form: Dict):
    '''Inserts book data into the movies database'''

    title = request_form['media_title'].lower()
    director = request_form['director'].lower()
    genre = request_form['genre'].lower()
    summary = request_form['summary']
    release_date = request_form['release_date']

    db.execute(f'''insert into movies(title, director, 
        genre, summary, release_date) values (?, ?, ?, ?, ?)''',
    (title, director, genre, summary, release_date))


def add_book_to_database(db: Connection, request_form: Dict):
    '''Inserts book data into the books database'''

    title = request_form['media_title'].lower()
    author = request_form['author'].lower()
    genre = request_form['genre'].lower()
    summary = request_form['summary']
    release_date = request_form['release_date']

    db.execute(f'''insert into books(title, author, 
        genre, summary, release_date) values (?, ?, ?, ?, ?)''',
    (title, author, genre, summary, release_date))


def add_media_to_database(db: Connection, request_form: Dict):
    '''Determines the category of an input media and inserts 
    the data into the correct database
    '''
    category = request_form['category']
    if category == 'movies':
        add_movie_to_database(db, request_form)
    elif category == 'books':
        add_book_to_database(db, request_form)


@login_required
@bp.route('media', methods=('GET', 'POST'))
def media():
    '''Form for adding new reviewable media for existing categories'''

    if request.method == 'POST':
        media_type = request.form['category'].lower()
        media_title = request.form['media_title'].lower()
        release_date = request.form['release_date']

        db = get_db()
        error = None

        if db.execute(
            'select id from categories where media_type is ?',
            (media_type,)
        ).fetchone() is None:
            error = f'Category {media_type} does not exist'
        elif not is_valid_date(release_date):
            error = f'{release_date} is not a valid date format. Try dd-mm-YYYY (e.g {datetime.now().strftime("%d-%m-%Y")}).'
        
        if error is None:
            add_media_to_database(db, request.form)
            db.commit()

            return redirect(url_for('profile.view_media_profile', category=media_type, title=media_title))
        
        flash(error)
    
    return render_template('add/add_media.j2')
