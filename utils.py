from datetime import datetime

from settings import JWT_SECRET_KEY
from flask_mysqldb import MySQLdb
from hashlib import pbkdf2_hmac

from Database_connector import db

import os
import jwt


def db_read(query, params=None):
    # cursor = db.connection.cursor()
    cursor = db.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)

    entries = cursor.fetchall()
    cursor.close()

    content = []

    for entry in entries:
        content.append(entry)

    return content


def db_write(query, params):
    # cursor = db.connection.cursor()
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        # db.connection.commit()
        db.commit()
        cursor.close()

        return True

    except MySQLdb._exceptions.IntegrityError:
        cursor.close()
        return False


def generate_salt():
    salt = os.urandom(16)
    return salt.hex()


def generate_hash(plain_password, password_salt):
    password_hash = pbkdf2_hmac(
        "sha256",
        b"%b" % bytes(plain_password, "utf-8"),
        b"%b" % bytes(password_salt, "utf-8"),
        10000,
    )
    return password_hash.hex()


def generate_jwt_token(content):
    encoded_content = jwt.encode(content, JWT_SECRET_KEY, algorithm="HS256")
    token = str(encoded_content).split("'")[1]
    return token


def validate_user_input(input_type, **kwargs):
    if input_type == "authentication":
        if len(kwargs["email"]) <= 255 and len(kwargs["password"]) <= 255:
            return True
        else:
            return False


def validate_user(email, password):
    current_user = db_read("""SELECT * FROM users WHERE email = %s""", (email,))

    if len(current_user) == 1:
        saved_password_hash = current_user[0]["password_hash"]
        saved_password_salt = current_user[0]["password_salt"]
        password_hash = generate_hash(password, saved_password_salt)

        if password_hash == saved_password_hash:
            user_id = current_user[0]["user_id"]
            first_name = current_user[0]["first_name"]
            last_name = current_user[0]["last_name"]
            user_email = current_user[0]["email"]
            jwt_token = generate_jwt_token(
                {"user_id": user_id,
                 "first_name": first_name,
                 "last_name": last_name,
                 "email": user_email
                 })
            return jwt_token
        else:
            return False, "password"

    else:
        return False, "email"


def write_message(id, user_id, message, is_bot):
    # cur = db.cursor()
    # db.commit()
    # if db_write("""INSERT into medical_chatbot_messages (id, user_id, message, isBot) VALUES (%s, %s, %s, %s)""",
    # (id, user_id, message, is_bot)
    # ):
    cur = db.cursor()
    cur.execute("insert into medical_chatbot_messages (id, user_id, message, isBot) values ('%s', %s, '%s', %s)" % (id, user_id, message, is_bot))
    db.commit()
    print("Successfully written to db")
    return True

    # else:
    #     return False


def get_user_messages(user_id):
    messages = db_read("""SELECT * FROM medical_chatbot_messages WHERE user_id = %s""", (user_id,))
    for message in messages:
        if message["isBot"] == 0:
            message["isBot"] = False
        elif message["isBot"] == 1:
            message["isBot"] = True
    messages_dict = {}
    messages_dict["messages"] = messages
    return messages_dict
