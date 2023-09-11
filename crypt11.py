import json
from functools import wraps
from datetime import datetime, timedelta
import os
import pytz
from flask import Flask, abort, jsonify, redirect, url_for, render_template, request, session
from flask_socketio import SocketIO
import requests
import jwt  # You need to have PyJWT library installed
import string
import random
from encryption.encrypt import *

from decryption.decrypt import *




from argon2 import PasswordHasher
import argon2.exceptions

from functions import appendUsernameToJSONFile, createJSONFile, format_date_time, generate_random_string
app = Flask(__name__)

def sendStats(sid, profile, interests):
    
    
    # API endpoint URL
    url = "http://localhost/api/sendStats.php"

    # JWT payload
    payload = {
        "sid": encrypt(sid.encode()),
        "profile": profile,
        "interests": interests
        
    }

    # Your secret key
    secret_key = 'kousic'

    # Create JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm='HS256')
    print("============Water===============")
    print(jwt_token)
    



    # Custom headers including the JWT
    headers = {
        "Authorization": f"Bearer {jwt_token}"
    }
   
    # Send the POST request with custom headers and JWT token
    response = requests.post(url, headers=headers)

    # Print response content
    # print("Response Content:", response.content)
    if response.status_code  == 200 :
        setLocalStats(sid, profile, interests)

        
        return True

    # return response.status_code 

def setLocalStats(sid, profile, interests):
   
    

    data = {
        "profile": f"{interests}",
        "interests": f"{profile}"    
        
    }
   
    
    with open(f"./user-json/{sid}.json", 'r') as json_file:
        existing_data = json.load(json_file)
    existing_data['stats'] = data
    with open(f'./user-json/{sid}.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


sid = "UuHjYqu91YKKjf3OJ5M4ox4AmiEx4g"
profile = 0
interests = 1
snedStats(sid, profile, interests)

       



