from typing import Text
from flask import (Blueprint, render_template)

from criticle.db import get_db
from criticle.utilities import get_reviews, filter_profile_query


# create blueprint
bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('<string:category>/<string:title>/', methods=('GET',))
def view_media_profile(category: str, title: str) -> Text:
    """Return the profile view for media given a media category and title"""
    db = get_db()
    
    category_id = db.execute(
        'select id from categories where media_type is ?',
        (category.lower(),)).fetchone()[0]

    profile_query = db.execute(
        f'select * from {category.lower()} where title is ?',
        (title.lower(),)).fetchall()[0]

    reviews_query = db.execute(
        'select * from reviews where media_id is ? and category_id is ?',
        (profile_query['id'], category_id)).fetchall()
    reviews = get_reviews(db, reviews_query)

    profile_attrs = filter_profile_query(profile_query)

    try:
        summary = profile_attrs.pop('summary')
    except KeyError:
        summary = ''

    image_id = 1

    input = {
        'profile_attrs': profile_attrs,
        'reviews': reviews,
        'heading': title.title(),
        'summary': summary,
        'image': f'images/{image_id}.jpg',
        'page': 'media'}


    return render_template('profile/profile.j2', input=input)


@bp.route('<string:username>/', methods=('GET',))
def view_user_profile(username: str) -> Text:
    """Return the profile view for a user given a username"""
    db = get_db()

    user_id = db.execute(
        'select id from users where username is ?',
        (username, )).fetchone()[0]
    
    # Get reviews from database
    reviews_query = db.execute(
        'select * from reviews where user_id is ?',
        (user_id,)).fetchall()
    reviews = get_reviews(db, reviews_query)

    # Get profile information from database
    profile_query = db.execute(
        'select * from users where id is ?',
        (user_id,)).fetchall()[0]
    profile_attrs = filter_profile_query(profile_query)

    try:
        summary = profile_attrs.pop('summary')
    except KeyError:
        summary = ''

    image_id = 1

    input = {
        'profile_attrs': profile_attrs,
        'reviews': reviews,
        'heading': username,
        'summary': summary,
        'image': f'images/{image_id}.jpg',
        'page': 'user'}

    return render_template('profile/profile.j2', input=input)
