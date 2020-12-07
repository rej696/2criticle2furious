import time
import atexit
import random
import sqlite3
import os
import click
import requests
import nltk

from textblob import TextBlob
from flask import Flask, g
from flask.cli import with_appcontext
from apscheduler.schedulers.background import BackgroundScheduler
from imdb import IMDb
from criticle.db import get_db


OMDB_API = 'http://www.omdbapi.com/?t=%s&apikey=%s'
BOT_NAME = 'scheduled_poster'
BOT_PASSWORD = '12345'


def run_post_bot(app):
    app.cli.add_command(generate_post)
    # nltk.download('punkt')
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=post_bot, trigger="interval", seconds=10)
    scheduler.start()


def post_bot():
    os.system("flask generate-post")


@click.command('generate-post')
@with_appcontext
def generate_post():
    db = get_db()

    # add_movie(db)

    bot_id = get_or_create_user_id(db, BOT_NAME, BOT_PASSWORD)

    category_id = select_random_category_id(db)
    category_name = get_category_name_from_id(db, category_id)
    media = select_random_media(db, category_name)
    media_id = media['id']

    verbs = ['liked', 'didn\'t like', 'hated', 'loved']
    separators = ['especially', 'except']
    # nouns = ['truck', 'apple', 'jigsaw piece', 't-rex', 'fridge', 'elephant', 'charmander']
    second_verbs = ['fell into', 'exploded', 'ran off with']
    nouns = []
    for noun_phrase in TextBlob(media['summary']).noun_phrases:
        nouns.append(noun_phrase)

    review_body = f'''I {random.choice(verbs)} this {category_name[:-1]} {random.choice(separators)}
        when the {random.choice(nouns)} {random.choice(second_verbs)} the
        {random.choice(nouns)}.
        '''
    
    score = random.randint(0, 30)

    db.execute(f'insert into reviews (category_id, media_id, user_id, body, rating) values (?, ?, ?, ?, ?)',
        (category_id, media_id, bot_id, review_body, score))

    db.commit()


def add_movie(db):
    imdb_api = IMDb()
    top_250 = imdb_api.get_top250_movies()
    omdb_key = os.environ['OMDB_KEY']

    top_250_shuffled = []
    for movie in top_250:
        top_250_shuffled.append(movie)
    
    random.shuffle(top_250_shuffled)

    for imdb_movie in top_250_shuffled:
        movie_title = imdb_movie['title']
        if not is_title_in_db(db, 'movies', movie_title.lower()):
            omdb_response = make_omdb_request(movie_title, omdb_key)
            if omdb_response is not None:
                cleaned_movie = {
                    'title': omdb_response['Title'],
                    'director': omdb_response['Director'],
                    'genre': omdb_response['Genre'],
                    'summary': omdb_response['Plot']
                }

                add_title_to_db(db, cleaned_movie)
                break


def make_omdb_request(movie_title, key):
    response = requests.get(OMDB_API % (movie_title.replace(' ', '+'), key))
    if response.status_code == 200:
        return response.json()
    return None


def is_title_in_db(db, category_name, title):
    results = db.execute(f'select * from {category_name} where title is ?', (title,)).fetchone()
    return results is not None


def add_title_to_db(db, movie_dict):
    db.execute('insert into movies (title, director, genre, summary) values (?, ?, ?, ?)',
        (movie_dict['title'].lower(), movie_dict['director'].lower(), movie_dict['genre'].lower(), movie_dict['summary']))


def get_or_create_user_id(db, username, password):
    user_id = db.execute('select id from users where username is ?', (username,)).fetchone()
    if user_id is None:
        create_user(db, username, password)
        return get_or_create_user_id(db, username, password)
    return user_id[0]


def create_user(db, username, password):
    db.execute('insert into users(username, password) values(?, ?)', (username, password))


def select_random_category_id(db):
    return random.choice(db.execute('select id from categories').fetchall())[0]


def get_category_name_from_id(db, category_id):
    return db.execute('select media_type from categories where id is ?', (category_id,)).fetchone()[0]


def select_random_media(db, category_name):
    medias = db.execute(f'select * from {category_name}').fetchall()
    return random.choice(medias)
