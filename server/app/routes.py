from app import app, request, db
from loguru import logger
from app.models import User


# User routes
# Add user to database
@app.route('/api/user-signup', methods=['GET', 'POST'])
def _api_signup():
    if request.method == 'POST':
        data = request.get_json()
        login = data['login']
        password_hash = data['password-hash']
        user = User(username=login, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return {'is_registered': True}
    return {'is_registered': False}


# Check user login
@app.route('/api/user-login', methods=('GET', 'POST'))
def _api_login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['login']
        password = data['password-hash']
        if User.query.filter_by(username=username, password_hash=password).first():
            return {'logged': True}
        return {'logged': False}


# Check is user nickname free
@app.route('/api/check-login/<string:login>')
def _api_check_login(login):
    try:
        if User.query.filter_by(username=login).first():
            return {'is_free': False}
        return {'is_free': True}
    except Exception as e:
        logger.error(f'Error: {e}')


# Delete user
@app.route('/api/delete-user', methods=['GET', 'POST'])
def _api_delete_user():
    if request.method == 'POST':
        data = request.get_json()
        user_to_delete = User.query.filter_by(username=data['username']).first()
        print(1)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return {'success': True}
        print(2)
        return {'success': False}
