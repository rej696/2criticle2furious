#!/usr/bin/env python3
import os
from flask import Flask, render_template


def create_app(test_config=None):
    """Create and configure the app"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "criticle.db")
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def home():
        from .db import get_db
        database = get_db()
        users = []
        for row in database.execute('select username from users').fetchall():
            users.append(row['username'])

        return render_template('home.j2', users=users)

    @app.route("/hello")
    def hello():
        return "Hello, World!"
    
    from . import db
    db.init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp)
    
    # from . import user_profile # user_profile.py
    # app.register_blueprint(user_profile)

    # #user_profile.py

    # @app.route("/profiles/<string:username>")
    # def profile(username):
    #     return "this is a profile"
    

    return app