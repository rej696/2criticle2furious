from flask import Blueprint

from criticle import db


# create blueprint
bp = Blueprint('add_user', __name__, url_prefix='/add_user')

@bp.route('/hal')
def hal():
    return 'hal'

@bp.route('/add/<string:name>')
def add_user(name):
    database = db.get_db()
    database.execute('insert into users(username, firstname, lastname, age, image_id) values(?, ?, ?, ?, ?)', (name, name, 'Jackson', 38, 1335))
    database.commit()

    # Check user has been added by printing current users
    results = database.execute('select * from users').fetchall()

    string = ''
    for column in results:
        string += '<p>'
        for row in column:
            string += f'{row}, '
        string += '</p>'
    print(results[0])
    print('break')
    print(results[1])

    return string
