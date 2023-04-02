from flask import Response, request, jsonify
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
    data = request.json()
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
    data = request.json()
    chat_id = data.get('chat_id')
    content = data.get('content')

    msg_obj = ChatMessage(user_id=current_user_id, chat_id=chat_id, is_user=True, content=content)
    db.session.add(msg_obj)
    db.session.commit()

    # Respond
    return Response(openai_chat())

    # return jsonify({'code': 0})
