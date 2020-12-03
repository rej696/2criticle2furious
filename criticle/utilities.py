from dateutil.parser import parse, ParserError
from sqlite3 import Connection
from typing import Dict, List


# Database fields that are should not be displayed on a profile
BANNED_KEYS = (
    'password',
    'id',
    'image_id'
)


def is_valid_date(date_string: str) -> bool:
    """Check if an input string can be parsed correctly as a date"""
    try:
        parse(date_string)  # .strptime('%Y-%m-%d %H:%M:%S')
    except ParserError:
        return False
    return True


def filter_profile_query(profile_query: Dict) -> Dict:
    """Return a dictionary of filtered profile information valid for display"""
    profile_attrs = {}
    for key in profile_query.keys():
        if key not in BANNED_KEYS:
            if 'date' in key:
                # Database strformat 2020-12-03 15:32:11
                date_str = parse(profile_query[key])  # .strptime('%Y-%m-%d %H:%M:%S')
                profile_attrs[key] = date_str.strftime('%H:%M %d-%m-%Y')
            else:
                profile_attrs[key] = profile_query[key]
    return profile_attrs
    # return {key: profile_query[key] for key in profile_query.keys() if key not in BANNED_KEYS}


def get_review(db: Connection, review_query: Dict) -> Dict:
    """Return a dictionary of review information to be displayed from a 
    database query for a single review entry
    """
    category = db.execute(
        'select media_type from categories where id is ?',
        (review_query['category_id'],)).fetchone()[0]

    title = db.execute(
        f'select title from {category.lower()} where id is ?',
        (review_query['media_id'],)).fetchone()[0]

    username = db.execute(
        'select username from users where id is ?',
        (review_query['user_id'],)).fetchone()[0]
    
    # Database strformat 2020-12-03 15:32:11
    date_str = parse(review_query['upload_date'])  # .strptime('%Y-%m-%d %H:%M:%S')
    upload_date = date_str.strftime('%H:%M %d-%m-%Y')

    rating = review_query['rating']
    rating_percentage = str(int((int(rating)/30) * 100)) + '%'

    return {'category': category.title(),
            'rating': review_query['rating'],
            'rating_percentage': rating_percentage,
            'body': review_query['body'],
            'title': title.title(),
            'username': username,
            'upload_date': upload_date}


def get_reviews(db: Connection, reviews_query: List[Dict]):
    """Return a list dictionaries of each review data in from a review query"""
    return [get_review(db, review_query) for review_query in reviews_query]