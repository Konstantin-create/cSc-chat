from app import app, request, db
from loguru import logger
from app.models import User, Chat, Message


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
    try:
        if request.method == 'POST':
            data = request.get_json()
            user_to_delete = User.query.filter_by(username=data['username']).first()
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return {'success': True}
            return {'success': False}
    except Exception as e:
        logger.error(f'Error: {e}')
        return {'success': False}


# Chat routes
# Create chat
@app.route('/api/create-chat/', methods=['GET', 'POST'])
def _api_create_chat():
    try:
        if request.method == 'POST':
            data = request.get_json()
            new_chat = Chat(chat_name=data['chat_name'], chat_creator=data['chat_creator'])
            db.session.add(new_chat)
            db.session.commit()
            return {'success': True, 'chat_id': new_chat.id}
    except Exception as e:
        logger.error(f'Error: {e}')
        return {'success': False, 'chat_id': None}


# Remove chat
@app.route('/api/remove-chat', methods=['GET', 'POST'])
def _api_delete_chat():
    try:
        if request.method == 'POST':
            data = request.get_json()
            chat_to_delete = Chat.query.filter_by(chat_name=data['chat_name']).first()
            if chat_to_delete and chat_to_delete.chat_creator == data['chat_creator']:
                db.session.delete(chat_to_delete)
                db.session.commit()
                return {'success': True}
        return {'success': False}
    except Exception as e:
        logger.error(f'Error: {e}')
        return {'success': False}

