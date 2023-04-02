from flask import Response, request, jsonify, current_app, stream_with_context
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.apis import bp
from app.extensions import db
from app.models import User, Token, Chat, ChatMessage
from app.aigc import openai_chat


@bp.route('/user/token/new', methods=['POST'])
@jwt_required()
def new_token():
    current_user_id = get_jwt_identity()
    # Data validation
    data = request.get_json()
    platform = data.get('platform')
    token = data.get('token')

    token_obj = Token(user_id=current_user_id, platform=platform, token=token)
    db.session.add(token_obj)
    db.session.commit()

    return jsonify({'code': 0})


@bp.route('/user/token/edit', methods=['POST'])
@jwt_required()
def edit_token():
    current_user_id = get_jwt_identity()
    pass


@bp.route('/user/token/remove', methods=['POST'])
@jwt_required()
def remove_token():
    current_user_id = get_jwt_identity()
    pass


@bp.route('/chat/new', methods=['POST'])
@jwt_required()
def new_chat():
    current_user_id = get_jwt_identity()

    chat_obj = Chat(user_id=current_user_id)
    db.session.add(chat_obj)
    db.session.commit()

    return jsonify({'code': 0, 'data': {'chat_id': chat_obj.id}})


@bp.route('/chat/message', methods=['POST'])
@jwt_required()
def new_chat_message():
    current_user_id = get_jwt_identity()
    # Data validation
    data = request.get_json()
    chat_id = data.get('chat_id')
    content = str(data.get('content'))

    chat_obj = Chat.query.get(chat_id)
    if chat_obj is None or not content:
        return jsonify({'message': 'Invalid data'})
    if chat_obj.user.id != current_user_id:
        return jsonify({'message': 'Not authorized'})

    msg_obj = ChatMessage(chat_id=chat_id, is_user=True, content=content)
    db.session.add(msg_obj)
    db.session.commit()
    history = chat_obj.to_history()

    @stream_with_context
    def wrapper(iterable):
        try:
            response_content = ''
            for item in iterable:
                response_content += item
                yield item
        finally:
            msg_obj = ChatMessage(chat_id=chat_id, is_user=False, content=response_content)
            db.session.add(msg_obj)
            db.session.commit()

    # Respond
    return wrapper(openai_chat(history=history))
