import functools

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, g)

from werkzeug.security import check_password_hash, generate_password_hash

from criticle.db import get_db


# create blueprint
bp = Blueprint('auth', __name__, url_prefix='/auth')

# @bp.route('/hal')
# def hal():
#     return 'hal'

# @bp.route('/add_user/<string:name>')
# def add_user(name):
#     database = get_db()
#     database.execute('insert into users(username, firstname, lastname, age, image_id) values(?, ?, ?, ?, ?)', (name, name, 'Jackson', 38, 1335))
#     database.commit()

#     # Check user has been added by printing current users
#     results = database.execute('select * from users').fetchall()

#     string = ''
#     for column in results:
#         string += '<p>'
#         for row in column:
#             string += f'{row}, '
#         string += '</p>'
#     print(results[0])
#     print('break')
#     print(results[1])

#     return string


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # TODO need to add image id and profile pic upload
        image_id = None
        
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        age = request.form['age']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        elif not password:
            error = 'Password is required'
        elif db.execute(
            'select id from users where username = ?', (username,)
        ).fetchone() is not None:
            error = f'User {username} is already registered'
        
        if error is None:
            db.execute(
                'insert into users (username, password, firstname, lastname, age, image_id) values (?, ?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), firstname, lastname, age, image_id)
            )
            db.commit()
            
            return redirect(url_for('auth.login'))
        
        flash(error)
            
    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        
        user = db.execute(
            'select * from users where username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect Username'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect Password'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('profile.view_user_reviews', username=username))
        
        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'select * from users where id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
