import Main as chatbot

# Flask
from flask import Flask, request, jsonify, json
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import datetime
import json
from settings import MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB

# from auth import authentication
import auth
from utils import get_user_messages, write_message

authentication = auth.authentication

app = Flask(__name__)

CORS(app)

app.register_blueprint(authentication, url_prefix="/api/auth")

# @cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
# GET /, test route
# @app.route('/', methods=["GET"])
# # @cross_origin(supports_credentials=True)
# def testGet():
#     return jsonify({"userId": 1, "isBot": True}), 200


# POST /medical
@app.route('/medical', methods=["POST"])
# @cross_origin(supports_credentials=True)
def chatbotReply():
    # context = chatbot.context
    message = request.get_json()
    print(message)
    id = message['id']
    messageText = message['message']
    userId = message['userId']
    context = message['context']

    # write user message to database
    write_message(id, userId, messageText, False)

    # if not userId in context.keys():
    #     chatbot.context[userId]=""
    # while userId not in context.keys():
    #     pass
    # reply, context = chatbot.response(messageText, userId, context)
    reply = chatbot.response(messageText,userId)
    date_handler = lambda obj: (
        obj.isoformat()
        if isinstance(obj, (datetime.datetime, datetime.date))
        else None
    )
    ident = json.dumps(datetime.datetime.now(), default=date_handler).strip('"')
    write_message(ident, userId, reply, True)
    # return jsonify({"userId": 1, "id": ident, "message": reply, "isBot": True, "context": context}), 200
    return jsonify({"userId": userId, "id": ident, "message": reply, "isBot": True}), 200


# @app.route('/medical/messages/<user_id>', methods=["GET"])
# def getMessages(user_id):
#     print(jsonify(get_user_messages(user_id)))
#     return jsonify(get_user_messages(user_id)), 200

@app.route('/medical/messages/<user_id>', methods=["GET"])
# @cross_origin(supports_credentials=True)
def getMessages(user_id):
    print(jsonify(get_user_messages(user_id)))
    return jsonify(get_user_messages(user_id)), 200


app.run(port=5002, debug=True, use_reloader=False)
