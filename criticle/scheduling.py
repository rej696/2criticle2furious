import time
import atexit
import random
import sqlite3
import os
import click

from flask import Flask, g
from flask.cli import with_appcontext
from apscheduler.schedulers.background import BackgroundScheduler
from criticle.db import get_db


BOT_NAME = 'scheduled_poster'
BOT_PASSWORD = '12345'


def run_post_bot(app):
    app.cli.add_command(generate_post)
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=post_bot, trigger="interval", seconds=3)
    scheduler.start()


def post_bot():
    os.system("flask generate-post")


@click.command('generate-post')
@with_appcontext
def generate_post():
    db = get_db()

    bot_id = get_or_create_user_id(db, BOT_NAME, BOT_PASSWORD)

    # category_id = select_random_category_id(db)
    # category_name = get_category_name_from_id(db, category_id)
    # media_id = select_random_media_id(db, category_name)

    verbs = ['liked', 'didn\'t like', 'hated', 'loved']
    separators = ['especially', 'except']
    nouns = ['truck', 'apple', 'jigsaw piece', 't-rex', 'fridge', 'elephant', 'charmander']
    second_verbs = ['fell into', 'exploded', 'ran off with']

    review_body = f'''I {random.choice(verbs)} this movie {random.choice(separators)}
        when the {random.choice(nouns)} {random.choice(second_verbs)} the
        {random.choice(nouns)}
        '''
    
    score = random.randint(0, 30)

    db.execute(f'insert into reviews (category_id, media_id, user_id, body, rating) values (?, ?, ?, ?, ?)',
        (1, 1, bot_id, review_body, score))
    db.commit()


def get_or_create_user_id(db, username, password):
    user_id = db.execute('select id from users where username is ?', (username,)).fetchone()
    if user_id is None:
        create_user(db, username, password)
        return get_or_create_user_id(db, username, password)
    return user_id[0]


def create_user(db, username, password):
    db.execute('insert into users(username, password) values(?, ?)', (username, password))


def select_random_category_id(db):
    return random.choice(db.execute('select id from categories').fetchall())


def get_category_name_from_id(db, category_id):
    return db.execute('select media_type from categories where id is ?', (category_id,)).fetchone()[0]


def select_random_media_id(db, category_name):
    media_ids = db.execute(f'select id from {category_name}').fetchall()
    return random.choice(media_ids)
