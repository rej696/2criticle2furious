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

    @app.route("/hello")
    def hello():
        return render_template('search/search.j2')
    
    from . import db
    db.init_app(app)

    from . import scheduling
    scheduling.run_post_bot(app)

    from .home import bp as home_bp
    app.register_blueprint(home_bp)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from .add import bp as add_bp
    app.register_blueprint(add_bp)

    # from . import user_profile # user_profile.py
    # app.register_blueprint(user_profile)

    # #user_profile.py

    # @app.route("/profiles/<string:username>")
    # def profile(username):
    #     return "this is a profile"
    
    return app