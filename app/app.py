import os
import jwt
import random
from functools import wraps
from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from notion_client import Client, APIResponseError
from dotenv import load_dotenv

load_dotenv(".env")

# env variables
user = os.environ.get("USER_AUTH")
userMdp = os.environ.get("USER_MDP")
secret = os.environ.get('FLASK_SECRET_KEY')
notion_quotes_id = os.environ.get('NOTION_QUOTES_DATABASE_ID')
notion_english_id = os.environ.get('NOTION_ENGLISH_DATABASE_ID')
notion_token = os.environ.get('NOTION_TOKEN')
cors_url = os.environ.get('CORS_URL')

app = Flask(__name__)
app.secret_key = secret
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

print(cors_url if cors_url is not None else "*")
# enable CORS
CORS(app, resources={r"/*": {"origins": cors_url if cors_url is not None else "*"}})

# set up database
notion = Client(auth=notion_token)

# middleware for auth
def isAuthenticated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not request.headers.get('Authorization'):
            return {'message': 'No token provided'}, 400
        try:
            token = request.headers.get('Authorization')[7:]
            payload = jwt.decode(token, secret, algorithms=[
                                 "HS256"], options={'verify_exp': False})

            if not payload["mdp"] == userMdp:
                return {'status': 'false', 'message': 'Invalid token provided.'}, 400
        except Exception as error:
            print(error)
            return {'status': 'false', 'message': 'Error with token'}, 400
        return current_app.ensure_sync(func)(*args, **kwargs)
    return wrapper


def generate_cookie():
    encoded_jwt = jwt.encode({"user": user, "mdp": userMdp}, os.environ.get(
        'FLASK_SECRET_KEY'), algorithm="HS256").decode("utf-8")
    print(encoded_jwt)


def queryNotion(database_id):
    try:
        query = notion.databases.query(
            **{
                "database_id": database_id,
            }
        )
        return query.get("results")

    except APIResponseError as error:
        print(error)
        return jsonify(status=False, message=f"Api error response : {error}")
     

@app.route("/quotes", methods=["GET"])
@isAuthenticated
def allQuotes():
    quotes = queryNotion(notion_quotes_id)
    return jsonify(status=True, data=quotes)


@app.route("/quotes/random", methods=["GET"])
@isAuthenticated
def randomQuotes():
    quotes = queryNotion(notion_quotes_id)
    quotes = [quote["properties"]["quotes"]["title"][0]["plain_text"]
              for quote in quotes]

    # generate_cookie()
    return jsonify(status=True, data=random.choice(quotes))


@app.route("/english", methods=["GET"])
@isAuthenticated
def allEnglish():
    quotes = queryNotion(notion_english_id)
    quotes = [quote["properties"] for quote in quotes]

    return jsonify(status=True, data=quotes)


@app.route("/english/random", methods=["GET"])
@isAuthenticated
def randomEnglish():
    quotes = queryNotion(notion_english_id)
    quotes = [quote["properties"] for quote in quotes]
    return jsonify(status=True, data=random.choice(quotes))
