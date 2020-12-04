from typing import Dict, List

from sqlite3 import Connection
from flask import (Blueprint, render_template, request, flash)

from criticle.db import get_db
from criticle.utilities import get_reviews, filter_profile_query


# create blueprint
bp = Blueprint('search', __name__, url_prefix='/search')


def get_profiles(db: Connection, profiles_query):
    # TODO Get users/movies/ from database
    users = []
    for row in profiles_query:
        users.append(row['username'])
    return users


def get_input(db: Connection, profiles_query, reviews_query) -> Dict:
    return {'profiles': get_profiles(db, profiles_query), 'reviews': get_reviews(db, reviews_query)}


def get_default_profiles_query(db: Connection) -> List:
    """Get all users from database ordered alphabetically"""
    return db.execute('select * from users order by username asc').fetchall()


def get_default_reviews_query(db: Connection) -> List:
    """Get all reviews from database orderd by upload_date"""
    return db.execute('select * from reviews order by upload_date desc').fetchall()


def search_users(db: Connection, search: str) -> List:
    """Search user database for search input and return user_profiles and user_reviews"""
    pass


"""select * from reviews where category_id is 
        (select id from categories where media_type is 'movies')
        and (media_id is (select id from movies
        where title like '%rowan saunders%' or director like '%rowan%'
        or genre like '%rowan%')
        or user_id is (select id from users
        where username like '%rowan%' or firstname like '%rowan saunders%'
        or lastname like '%rowan saunders%' 
        or firstname || ' ' || lastname like '%rowan saunders%'))""",


# -------------------------------------------------------------------------
# search queries
# -------------------------------------------------------------------------

def search_user_profiles(db: Connection, search: str) -> List:
    """Search users database for search input and return user_profiles"""

    return db.execute(
        """select * from users where username like '%?%'
        or firstname like '%?%' or lastname like '%?%'
        or firstname || ' ' || lastname like '%?%')""",
        (search, search, search, search,)
    ).fetchall()


def search_movie_profiles(db: Connection, search: str) -> List:
    """Search movies database for search input and return movie_profiles"""

    return db.execute(
        """select * from movies
        where title like '%?%' or director like '%?%' or genre like '%?%'
        order by title asc)""",
        (search, search, search,)
    ).fetchall()


def search_book_profiles(db: Connection, search: str) -> List:
    """Search books database for search input and return book_profiles"""

    return db.execute(
        """select * from books
        where title like '%?%' or author like '%?%' or genre like '%?%'
        order by title asc""",
        (search, search, search,)
    ).fetchall()


def search_user_reviews(db: Connection, search: str) -> List:
    """Search users database for search input and return user_reviews"""

    return db.execute(
        """select * from reviews where 
        user_id is (select id from users where username like '%?%'
        or firstname like '%?%' or lastname like '%?%'
        or firstname || ' ' || lastname like '%?%')
        order by upload_date desc""",
        (search, search, search, search,)
    ).fetchall()


def search_movie_reviews(db: Connection, search: str) -> List:
    """Search movies database for search input and return movie_reviews"""

    return db.execute(
        """select * from reviews where category_id is 
        (select id from categories where media_type is 'movies')
        and media_id is (select id from movies
        where title like '%?%' or director like '%?%' or genre like '%?%')
        order by upload_date desc""",
        (search, search, search,)
    ).fetchall()


def search_book_reviews(db: Connection, search: str) -> List:
    """Search books database for search input and return book_reviews"""

    return db.execute(
        """select * from reviews where category_id is 
        (select id from categories where media_type is 'books')
        and media_id is (select id from movies
        where title like '%?%' or author like '%?%' or genre like '%?%')
        order by upload_date desc""",
        (search, search, search, search, search, search, search,)
    ).fetchall()


@bp.route("/", methods=('GET', 'POST'))
def view():

    db = get_db()

    if request.method == 'POST':
        display_type = request.form['displaytype'].lower()
        search_for = request.form['searchfor'].lower()
        search = request.form['search'].lower()

        reviews_query = None
        profiles_query = None

        if search_for == 'movies':

            reviews_query = search_movie_reviews(db, search)
            profiles_query = search_movie_profiles(db, search)
        
        if search_for == 'books':

            reviews_query = search_book_reviews(db, search)
            profiles_query = search_book_profiles(db, search)
        
        if search_for == 'users':

            reviews_query = search_user_reviews(db, search)
            profiles_query = search_book_profiles(db, search)

        if reviews_query is None and display_type == 'reviews':
            # write error message and set query to default depending on search_for
            flash()
            pass
        
        if profiles_query is None and display_type == 'profiles':
            # write error message and set query to default depending on search_for
            flash()
            pass

        # # search database for profiles from search field
        # profiles_query = search_profiles(db=db, search=search)
        
        # if profiles_query is None:
        #     error = f'Input "{search}" is not valid. Displaying all existing users.'

        # # search database for reviews from search field
        # reviews_query = search_reviews(db=db, search=search)

        # if reviews_query is None:
        #     error = f'Input "{search} is not valid. Displaying all reviews.'
        
        # if error is not None:
        #     flash(error)
        #     profiles_query = get_default_profiles_query(db=db)
        #     reviews_query = get_default_reviews_query(db=db)

    else:
        profiles_query = get_default_profiles_query(db=db)
        reviews_query = get_default_reviews_query(db=db)

    return render_template(
        'search/search.j2',
        input=get_input(db, profiles_query=profiles_query, reviews_query=reviews_query))
