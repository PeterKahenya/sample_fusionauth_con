from flask import Flask, jsonify, request
import os
import requests
import uuid
from os import environ as env



client_id: str = env.get("SF_CLIENT_ID")
client_secret: str = env.get("SF_CLIENT_SECRET")

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})


def sf_auth(username: str, password: str) -> dict:
    url = f"https://humentum-dev-ed.develop.my.salesforce.com/services/oauth2/token?grant_type=password&client_id={client_id}&client_secret={client_secret}&username={username}&password={password}&format=json"
    payload = {}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.json()

def sf_get_user_info(access_token: str) -> dict:
    url = "https://humentum-dev-ed.develop.my.salesforce.com/services/oauth2/userinfo"
    payload = {}
    headers = {
    'Authorization': f'Bearer {access_token}'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    return response.json()

@app.route('/authcon',methods=['POST'])
def auth_conn():
    print("Authenticating connection")
    print(request.json)
    username = request.json["loginId"]
    password = request.json["password"]
    auth_response = sf_auth(username, password)
    print(auth_response)
    sf_user_info = sf_get_user_info(auth_response["access_token"])
    fusionauth_user_info = {
            "user": {
                    "id": str(uuid.uuid4()),
                    "email": sf_user_info["email"],
                    "firstName": sf_user_info["first_name"],
                    "lastName": sf_user_info["last_name"],
                    "username": sf_user_info["preferred_username"]
                }
    }
    return jsonify(fusionauth_user_info)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))