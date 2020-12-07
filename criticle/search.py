from typing import Dict, List
from sqlite3 import Connection
from flask import (Blueprint, render_template, request, flash)

from criticle.db import get_db
from criticle.utilities import get_reviews


# create blueprint
bp = Blueprint('search', __name__, url_prefix='/search')


def get_profiles(profiles_query, search_for):
    if search_for == 'users':
        return [{'username': profile['username']} for profile in profiles_query]
    else:
        return [{'title': profile['title'].title()} for profile in profiles_query]


def get_input(db: Connection, display_type: str, search_for: str, search_input:str, profiles_query, reviews_query) -> Dict:
    return {
        'display_type': display_type,
        'search_for': search_for,
        'profiles': get_profiles(profiles_query, search_for),
        'reviews': get_reviews(db, reviews_query),
        'search_input': search_input}


def get_default_user_profiles_query(db: Connection) -> List:
    """Get all users from database ordered alphabetically"""
    return db.execute('select username from users order by username asc').fetchall()


def get_default_movie_profiles_query(db: Connection) -> List:
    """Get all movies from database ordered alphabetically"""
    return db.execute('select title from movies order by title asc').fetchall()


def get_default_book_profiles_query(db: Connection) -> List:
    """Get all books from database ordered alphabetically"""
    return db.execute('select title from books order by title asc').fetchall()


def get_default_profiles_query(db: Connection, search_for: str = None) -> List:
    """Get all profiles from database ordered alphabetically according to search_for"""
    if search_for == 'users':
        return get_default_user_profiles_query(db)
    elif search_for == 'books':
        return get_default_book_profiles_query(db)
    else:
        return get_default_movie_profiles_query(db)


def get_default_reviews_query(db: Connection) -> List:
    """Get all reviews from database orderd by upload_date"""
    return db.execute('select * from reviews order by upload_date desc').fetchall()


# def search_users(db: Connection, search: str) -> List:
#     """Search user database for search input and return user_profiles and user_reviews"""
#     pass


# """select * from reviews where category_id is 
#         (select id from categories where media_type is 'movies')
#         and (media_id is (select id from movies
#         where title like '%rowan saunders%' or director like '%rowan%'
#         or genre like '%rowan%')
#         or user_id is (select id from users
#         where username like '%rowan%' or firstname like '%rowan saunders%'
#         or lastname like '%rowan saunders%' 
#         or firstname || ' ' || lastname like '%rowan saunders%'))""",


# -------------------------------------------------------------------------
# search queries
# -------------------------------------------------------------------------

def search_user_profiles(db: Connection, search: str) -> List:
    """Search users database for search input and return user_profiles"""

    return db.execute(
        """select username from users where username like ?
        or firstname like ? or lastname like ?
        or firstname || ' ' || lastname like ?""",
        (search, search, search, search,)
    ).fetchall()


def search_movie_profiles(db: Connection, search: str) -> List:
    """Search movies database for search input and return movie_profiles"""

    return db.execute(
        """select title from movies
        where title like ? or director like ? or genre like ?
        order by title asc""",
        (search, search, search,)
    ).fetchall()


def search_book_profiles(db: Connection, search: str) -> List:
    """Search books database for search input and return book_profiles"""

    return db.execute(
        """select title from books
        where title like ? or author like ? or genre like ?
        order by title asc""",
        (search, search, search,)
    ).fetchall()


def search_user_reviews(db: Connection, search: str) -> List:
    """Search users database for search input and return user_reviews"""

    return db.execute(
        """select * from reviews where 
        user_id is (select id from users where username like ?
        or firstname like ? or lastname like ?
        or firstname || ' ' || lastname like ?)
        order by upload_date desc""",
        (search, search, search, search,)
    ).fetchall()


def search_movie_reviews(db: Connection, search: str) -> List:
    """Search movies database for search input and return movie_reviews"""

    return db.execute(
        """select * from reviews where category_id is 
        (select id from categories where media_type is 'movies')
        and media_id is (select id from movies
        where title like ? or director like ? or genre like ?)
        order by upload_date desc""",
        (search, search, search,)
    ).fetchall()


def search_book_reviews(db: Connection, search: str) -> List:
    """Search books database for search input and return book_reviews"""

    return db.execute(
        """select * from reviews where category_id is 
        (select id from categories where media_type is 'books')
        and media_id is (select id from books
        where title like ? or author like ? or genre like ?)
        order by upload_date desc""",
        (search, search, search,)
    ).fetchall()


@bp.route("/", methods=('GET', 'POST'))
def view():

    db = get_db()

    if request.method == 'POST':
        display_type = request.form['display_type'].lower()
        search_for = request.form['search_for'].lower()
        search_input = request.form['search']
        search = f"%{search_input.lower()}%"

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
            profiles_query = search_user_profiles(db, search)

        if not reviews_query and display_type == 'reviews':
            # write error message and set query to default depending on search_for
            flash(f'"{search_input}" returns no results. Displaying all reviews.')
            reviews_query = get_default_reviews_query(db=db)
            profiles_query = get_default_profiles_query(db=db, search_for=search_for)
        
        
        if not profiles_query and display_type == 'profiles':
            # write error message and set query to default depending on search_for
            flash(f'"{search_input}" returns no results. Displaying all {search_for} profiles')
            reviews_query = get_default_reviews_query(db=db)
            profiles_query = get_default_profiles_query(db=db, search_for=search_for)

    else:
        display_type='reviews'
        search_for='movies'
        profiles_query = get_default_profiles_query(db=db)
        reviews_query = get_default_reviews_query(db=db)
        search_input = "Search"

    return render_template(
        'search/search.j2',
        input=get_input(
            db,
            profiles_query=profiles_query,
            reviews_query=reviews_query,
            display_type=display_type,
            search_for=search_for,
            search_input=search_input))
