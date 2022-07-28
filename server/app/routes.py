from app import app, request, db
from loguru import logger
from app.models import User, Chat, Message, Subscribe


# User routes
# Add user to database
@app.route('/api/user-signup', methods=['GET', 'POST'])
def _api_signup():
    try:
        if request.method == 'POST':
            data = request.get_json()
            login = data['username']
            password_hash = data['password-hash']
            if not User.query.filter_by(username=login).first():
                logger.info(f'New user! {login}')
                logger.info(User.query.filter_by(username=login).first())
                user = User(username=login, password_hash=password_hash)
                db.session.add(user)
                db.session.commit()
                return {'success': True, 'is_registered': True}
            return {'success': True, 'is_registered': False} 
    except Exception as e:
        logger.error(f'Error in user signup block: {e}')
        return {'success': False, 'is_registered': None}


# Check user login
@app.route('/api/user-login', methods=('GET', 'POST'))
def _api_login():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password-hash']
            if User.query.filter_by(username=username, password_hash=password).first():
                return {'success': True, 'logged': True}
            return {'success': True, 'logged': False}
    except Exception as e:
        logger.error(f'Error in user login block: {e}')
        return {'success': False, 'logged': None}


# Check is user nickname free
@app.route('/api/check-login/<string:login>')
def _api_check_login(login):
    try:
        if User.query.filter_by(username=login).first():
            return {'success': True, 'is_free': False}
        return {'success': True, 'is_free': True}
    except Exception as e:
        logger.error(f'Error in check username block: {e}')
        return {'success': False, 'is_free': None}


# Check client local session
@app.route('/api/check-session', methods=['GET', 'POST'])
def check_user_session():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user = User.query.filter_by(id=data['id'], username=data['username'], password_hash=data['password_hash']).first()
            if user:
                return {'success': True, 'logged': True}
        return {'success': True, 'logged': False}
    except Exception as e:
        logger.error(f'Error in check client local session block: {e}')
        return {'success': False, 'logged': False}


# Get username by id
@app.route('/api/get-user-id/by-username', methods=['GET', 'POST'])
def get_user_id():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user = User.query.filter_by(username=data['username'], password_hash=data['password-hash']).first()
            if user:
                return {'success': True, 'user_id': user.id}
            return {'success': True, 'user_id': None}
    except Exception as e:
        logger.error(f'Error in get user id block: {e}')
        return {'success': False, 'user_id': None}


# Delete user
@app.route('/api/delete-user', methods=['GET', 'POST'])
def _api_delete_user():
    try:
        if request.method == 'POST':
            data = request.get_json()
            username = data['username']
            password = data['password-hash']
            user_to_delete = User.query.filter_by(username=username, password_hash=password).first()
            if user_to_delete:
                db.session.delete(user_to_delete)
                db.session.commit()
                return {'success': True, 'deleted': True}
            return {'success': True, 'deleted': False}
    except Exception as e:
        logger.error(f'Error in delete user block: {e}')
        return {'success': False, 'deleted': None}


# Chat routes
# Create chat
@app.route('/api/create-chat/', methods=['GET', 'POST'])
def _api_create_chat():
    try:
        if request.method == 'POST':
            data = request.get_json()
            logger.info(data)
            if User.query.filter_by(id=data['chat_creator_id'], password_hash=data['password-hash']).first():
                new_chat = Chat(chat_name=data['chat_name'], chat_creator=data['chat_creator_id'])
                db.session.add(new_chat)
                db.session.commit()
                return {'success': True, 'chat': {'id': new_chat.id, 'chat_name': new_chat.chat_name, 'chat_creator_id': new_chat.chat_creator}}
        return {'success': True, 'chat': None}
    except Exception as e:
        logger.error(f'Error in create chat block: {e}')
        return {'success': False, 'chat': None}


# Remove chat by id
@app.route('/api/remove-chat/by-name', methods=['GET', 'POST'])
def _api_delete_chat_by_name():
    try:
        if request.method == 'POST':
            data = request.get_json()
            chat_to_delete = Chat.query.filter_by(chat_name=data['chat_name']).first()
            chat_messages = Message.query.filter_by(from_chat=chat_to_delete.id).all()
            if User.query.filter_by(id=data['chat_creator_id'], password_hash=data['password-hash']):
                if chat_to_delete and chat_to_delete.chat_creator == data['chat_creator_id']:
                    if chat_messages is not None:
                        for message in chat_messages:
                            db.session.delete(message) 
                    db.session.delete(chat_to_delete)
                    db.session.commit()
                    return {'success': True, 'deleted': True}
            return {'success': True, 'deleted': False}
    except Exception as e:
        logger.error(f'Error in delete chat by name block: {e}')
        return {'success': False, 'deleted': None}

# Remove chat by id
@app.route('/api/remove-chat/by-id', methods=['GET', 'POST'])
def _api_delete_chat_by_id():
    try:
        if request.method == 'POST':
            data = request.get_json()
            chat_to_delete = Chat.query.filter_by(id=data['id']).first()
            chat_messages = Message.query.filter_by(from_chat=chat_to_delete.id).all()
            if User.query.filter_by(id=data['chat_creator_id'], password_hash=data['password-hash']).first():
                if chat_to_delete and chat_to_delete.chat_creator == data['chat_creator_id']:
                    if chat_messages is not None:
                        for message in chat_messages:
                            db.session.delete(message)
                    db.session.delete(chat_to_delete)
                    db.session.commit()
                    return {'success': True, 'deleted': True}
        return {'success': True, 'deleted': False}
    except Exception as e:
        logger.error(f'Error in delete chat by id block: {e}')
        return {'success': False, 'deleted': None}

# Get chat name by id
@app.route('/api/get-chat-info/by-id/<int:chat_id>')
def _api_get_chat_info_id(chat_id):
    try:
        chat = Chat.query.filter_by(id=chat_id).first()
        if chat:
            return {'success': True, 'chat': {'id': chat.id, 'chat_name':chat.chat_name, 'chat_creator_id': chat.chat_creator}}
        return {'success': True, 'chat': None}
    except Exception as e:
        logger.error(f'Error in get-chat-info by id block: {e}')
        return {'success': False, 'chat': None}

# Get chat info by chat name
@app.route('/api/get-chat-info/by-name/<string:chat_name>')
def _api_get_chat_info_name(chat_name):
    try:
        chat = Chat.query.filter_by(chat_name=chat_name).first()
        print(chat is None)
        if not (chat is None):
            return {'success': True, 'chat': {'id': chat.id, 'chat_name': chat.chat_name, 'chat_creator_id': chat.chat_creator}}
        return {'success': True, 'chat': None}
    except Exception as e:
        logger.error(f'Error in get-chat-info by name block: {e}')
        return {'success': False, 'chat': None}

# Get chats from user id
@app.route('/api/get-users-chat/<int:user_id>')
def _api_get_users_chat(user_id):
    try:
        chats = Chat.query.filter_by(chat_creator=user_id).all()
        output_chats = []
        if chats:
            for chat in chats:
                output_chats.append({'id': chat.id, 'chat_name': chat.chat_name, 'creator_id': chat.chat_creator})
            return {'success': True, 'chats': output_chats}
        return {'success': True, 'chats': None}
    except Exception as e:
        logger.error(f'Error in get_users_chat block: {e}')
        return {'success': False, 'chats': None}


# Message routes
# Create message
@app.route('/api/message/create', methods=['GET', 'POST'])
def _api_create_message():
    try:  
        if request.method == 'POST':
            data = request.get_json()
            if User.query.filter_by(id=data['from_user'], password_hash=data['password-hash']).first():
                new_message = Message(body=data['body'], from_user=data['from_user'], from_chat=data['from_chat'])
                db.session.add(new_message)
                db.session.commit()
                return {'success': True, 'message': {'id': new_message.id, 'from_user': new_message.from_user, 'from_chat': new_message.from_chat, 'body': new_message.body, 'time_stamp': new_message.time_stamp}}
        return {'success': True, 'message': None}
    except Exception as e:
        logger.error(f'Error in create message block: {e}')
        return {'success': False, 'message': None}

# Get message info by id
@app.route('/api/message/info', methods=['GET', 'POST'])
def _api_get_message_info_id():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if User.query.filter_by(id=data['user_id'], password_hash=data['password-hash']).first():
                message = Message.query.filter_by(id=data['message_id']).first()
                if message:
                    return {'success': True, 'message': {'id': message.id, 'from_user': message.from_user, 'from_chat': message.from_chat, 'body': message.body, 'time_stamp': message.time_stamp}}
        return {'success': True, 'message': None}
    except Exception as e:
        logger.error(f'Error in get message info by id block: {e}')
        return {'success': False, 'message': None}

# Delete message
@app.route('/api/message/delete', methods=['GET', 'POST'])
def _api_delete_message():
    try:
        if request.method == 'POST':
            data = request.get_json()
            if User.query.filter_by(id=data['user_id'], password_hash=data['password-hash']):
                message_to_delete = Message.query.filter_by(id=data['message_id']).first()
                if message_to_delete:
                    db.session.delete(message_to_delete)
                    db.session.commit()
                    return {'success': True, 'deleted': True}
        return {'success': True, 'deleted': False}
    except Exception as e:
        logger.error(f'Error in delete message block: {e}')
        return {'success': False, 'deleted': None}


# Get messages by chat id
@app.route('/api/messages/all/chat-id/<int:chat_id>')
def _api_get_chat_messages(chat_id):
    try:
        output_messages = []
        messages = Message.query.filter_by(from_chat=chat_id).all()
        if messages is not None:
            for message in messages:
                output_messages.append({'id': message.id, 'from_user': message.from_user, 'from_chat': message.from_chat, 'body': message.body, 'time_stamp': message.time_stamp})
            return {'success': True, 'messages': output_messages}
        return {'success': True, 'messages': None}
    except Exception as e:
        logger.error(f'Error in get chat messages block: {e}')
        return {'success': False, 'messages': None}


# User subscriptions routes
# Add user subscriptions
@app.route('/api/user-subscriptions/add', methods=['GET', 'POST'])
def add_user_subscriptions():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user = User.query.filter_by(id=data['user_id'], password_hash=data['password_hash']).first()
            if user:
                if not Subscribe.query.filter_by(chat_id=data['chat_id'], user_id=user.id).first():
                    subscription = Subscribe(chat_id=data['chat_id'], user_id=user.id)
                    db.session.add(subscription)
                    db.session.commit()
                    return {'success': True, 'added': True}
        return {'success': True, 'added': False}
    except Exception as e:
        logger.error(f'Error in add user subscription block: {e}')
        return {'success': False, 'added': False}

# Get user subscriptions
@app.route('/api/user-subscriptions/get', methods=['GET', 'POST'])
def get_user_subscriptions():
    try:
        if request.method == 'POST':
            data = request.get_json()
            chats_output = []
            user = User.query.filter_by(id=data['user_id'], password_hash=data['password_hash']).first()
            if user:
                subscriptions = Subscribe.query.filter_by(user_id=user.id).all()
                if subscriptions:
                    for subscription in subscriptions:
                        chat = Chat.query.filter_by(id=subscription.chat_id).first()
                        chats_output.append({'id': chat.id, 'chat_name':chat.chat_name, 'chat_creator_id': chat.chat_creator})
                    return {'success': True, 'chats': chats_output}
                return {'success': True, 'chats': []}
        return {'success': True, 'chats': None}
    except Exception as e:
        logger.error(f'Error in get user subscriptions block: {e}')
        return {'success': False, 'chats': None}

# Delete user subscription
@app.route('/api/user-subscriptions/delete', methods=['GET', 'POST'])
def delete_user_subscription():
    try:
        if request.method == 'POST':
            data = request.get_json()
            user = User.query.filter_by(id=data['user_id'], password_hash=data['password_hash']).first()
            if user:
                subscription = Subscribe.query.filter_by(user_id, data['chat_id']).first()
                if subscription:
                    db.session.delete(subscription)
                    db.session.commit()
                    return {'success': True, 'deleted': True}
        return {'success': True, 'deleted': False}
    except Exception as e:
        logger.error(f'Error in delete user subscription block: {e}')
        return {'success': False, 'deleted': False}
    
