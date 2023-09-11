import json
from functools import wraps
import datetime
import os
import pytz
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    url_for,
    render_template,
    request,
    session,
)
from flask_socketio import SocketIO
import requests
import jwt  # You need to have PyJWT library installed
import string
import random
from encryption.encrypt import *
import re
from decryption.decrypt import *
from argon2 import PasswordHasher
import argon2.exceptions


JWT_EXPIRATION_MINUTES = 1440

skc = "kousic"


# Function to create a new JWT token
def create_jwt_token(username, sid, client_ip, skc):
    payload = {
        "username": username,
        "ip": client_ip,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        "user_agent": request.headers.get("User-Agent"),
        "sid": sid, 
    }

    token = jwt.encode(payload, skc, algorithm="HS256")

    return token


def hash_password(password):
    # Generate a salt
    ph = PasswordHasher()

    hash = ph.hash(password)

    return hash


def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def validate_password(password):
    pattern = r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return bool(re.match(pattern, password))


with open("./server-json/user.json") as f1:
    usernames_data1 = json.load(f1)
    taken_usernames1 = usernames_data1["usernames"]


def check_username_server_side(username):
    username = username.lower()
    print(username)
    if username in taken_usernames1:
        print("F")
        return False

    else:
        print("T")

        return True


def InputValidation(u, p1, p2):
    u = u.lower()
    if check_username_server_side(u) == True:
        rp1 = r"^(?:.*[a-zA-Z]){4,}"
        # atleast four alphabets
        if re.match(rp1, u):
            username = u
            if p1 == p2:
                if validate_password(p1) == 1:
                    p1 = hash_password(p1)
                    InpData = [username, p1]
                    return InpData
                else:
                    error = "Password must contain atleast 8 characters.<br>Atleast one Letter And Atleast one Digit. <br>Atleast one character from @, $, !, %, ?, &."
                    return error

            else:
                error = "Both Passwords should match!"
                return error

        else:
            error = "Username should have atleast 4 Alphabets"
            return error
    else:
        error = "Username is not available.."


# ================================================================================================================================#


# Function to format current date and time in IST timezone
def format_date_time():
    # Get the current datetime in IST timezone
    ist = pytz.timezone("Asia/Kolkata")
    current_datetime = datetime.datetime.now(ist)

    # Format the datetime as "Mon DD YYYY hh:mmAM/PM"
    formatted_datetime = current_datetime.strftime("%b %d %Y %I:%M%p")
    return formatted_datetime


# Function to generate a random string of specified length
def generate_random_string(length=random.randint(30, 40)):
    characters = string.ascii_letters + string.digits
    random_string = "".join(random.choice(characters) for _ in range(length))
    return random_string


#######=================Create json file for users===============###########


def createJSONFile(sid):
    # Sample data in a dictionary
    data = {"sid": f"{sid}"}

    # Specify the file path where you want to create the JSON file
    file_path = f"./user-json/{sid}.json"

    # Open the file in write mode and use json.dump() to write the data
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON file created successfully!")
    session["sid"] = sid


def appendUsernameToJSONFile(username):
    file_path = "./server-json/user.json"

    # Check if the file already exists
    if os.path.exists(file_path):
        # Read the existing data from the file
        with open(file_path, "r") as json_file:
            existing_data = json.load(json_file)

        # Check if the file is empty or doesn't have a 'usernames' array
        if "usernames" in existing_data:
            existing_data["usernames"].append(username)
        else:
            existing_data["usernames"] = [username]
    else:
        # Create a new data dictionary with the provided username
        existing_data = {"usernames": [username]}

    # Write the updated data back to the file
    with open(file_path, "w") as json_file:
        json.dump(existing_data, json_file, indent=4)

    print("Username appended to JSON file successfully!")


#######=================Create json file for users===============###########


def sendStats(sid, profile, interests):
    # API endpoint URL
    url = "http://localhost/api/sendStats.php"

    # JWT payload
    payload = {"sid": encrypt(sid.encode()), "profile": profile, "interests": interests}

    # Your secret key
    secret_key = "kousic"

    # Create JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("============Water===============")
    print(jwt_token)

    # Custom headers including the JWT
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Send the POST request with custom headers and JWT token
    response = requests.post(url, headers=headers)

    # Print response content
    # print("Response Content:", response.content)
    if response.status_code == 200:
        setLocalStats(sid, profile, interests)

        return True

    # return response.status_code


def setLocalStats(sid, profile, interests):
    data = {"profile": f"{interests}", "interests": f"{profile}"}

    with open(f"./user-json/{sid}.json", "r") as json_file:
        existing_data = json.load(json_file)
    existing_data["stats"] = data
    with open(f"./user-json/{sid}.json", "w") as json_file:
        json.dump(existing_data, json_file, indent=4)


def send_sign_up_data_to_db(username, password):
    # API endpoint URL
    url = "http://localhost/api/postUserData.php"
    sid = generate_random_string()
    # JWT payload
    payload = {
        "username": encrypt(username.encode()),
        "password": encrypt(password.encode()),
        "datetime": encrypt(format_date_time().encode()),
        "sid": encrypt(sid.encode()),
    }

    # Your secret key
    secret_key = "kousic"

    # Create JWT token
    jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")
    print("============Water===============")
    print(jwt_token)

    # Custom headers including the JWT
    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Send the POST request with custom headers and JWT token
    response = requests.post(url, headers=headers)

    # Print response content
    # print("Response Content:", response.content)
    if response.status_code == 200:
        createJSONFile(sid)
        appendUsernameToJSONFile(username.lower())
        sendStats(sid, 0, 0)

    return response.status_code


# ==============for password verification==============#


def verify_password(entered_password, stored_hashed_password):
    ph = PasswordHasher()

    try:
        passwords_match = ph.verify(stored_hashed_password, entered_password)
    except argon2.exceptions.VerifyMismatchError:
        # Password verification failed
        return False

    return passwords_match


# ==============for password verification==============#


# S==============Shit is about to get real==============#
def isPasswordOkay(username, password):
    # API endpoint URL
    url = "http://localhost/api/isPasswordOkay.php"
    print(f"Username = {username}")

    # bytes.fromhex(username)

    encrypted_u = encrypt(username.encode())
    print(f"Username_e = {encrypted_u}")

    # Custom headers including the username and password
    headers = {"u": f"{encrypted_u}", "p": "kousic111"}

    # Send the GET request with custom headers
    responsetoget = requests.get(url, headers=headers)
    print("========================")
    print(f"response = {responsetoget}")
    print("========================")
    print(f"response_code = {responsetoget.status_code}")
    print("========================")

    if responsetoget.status_code == 200:
        try:
            response_json = responsetoget.json()
            enc_payload = response_json["message"]
            # print("========================")
            print("========================")

            print(f"This is enc_str : {enc_payload}")
            print("========================")
            print("========================")

        except (json.JSONDecodeError, KeyError):
            print("Failed to get enc_str")
            return False

        # Decode the JWT token
        try:
            # enc_payload = bytes.fromhex(enc_payload)
            # decoded_payload = bytes.fromhex(enc_payload[0][2:])
            print("Decrypting")

            decoded_payload = decrypt(enc_payload).split(", ")
            print(decoded_payload)

            print("Decrypted")

            # return decoded_payload
            # print(decoded_payload)

            password_hash = decoded_payload[5]
            if verify_password(password, password_hash):
                client_ip = request.remote_addr

                jwt_token1 = create_jwt_token(
                    decoded_payload[1], decoded_payload[2], client_ip, skc
                )

                # API endpoint URL
                url = "http://localhost/api/uploadToken.php"

                # JWT payload
                payload1 = {
                    "id": decoded_payload[0],
                    "username": decoded_payload[1],
                    "token": jwt_token1,
                    "aid": decoded_payload[3],
                    "valid": True,
                }

                # Create JWT token#####Works because skc and secret_key are same####
                jwt_token11 = jwt.encode(payload1, skc, algorithm="HS256")
                # print("New JWT Token:", jwt_token11)
                # Custom headers including the JWT
                headers = {"token": f"Bearer {jwt_token11}"}
                print("==========HEADERS==============")

                print(headers)
                print("==========HEADERS==============")

                # Send the POST request with custom headers and JWT token
                response1 = requests.post(url, headers=headers)

                # Print response content
                print("Response Content:", response1.content)
                return [response1.status_code, jwt_token1]
            else:
                return False
        except jwt.ExpiredSignatureError:
            print("Token expired")
            return False
        except jwt.InvalidTokenError:
            print("Invalid token")
            return False

    else:
        return False


##Sitepoint


####=======================================####


# E==============Shit is about to get real==============#


# Function to send sign-up data to the API
def get_user_data_from_db(username):
    # API endpoint URL
    url = "http://localhost/api/getUserData.php"

    # Custom headers including the JWT
    headers = {
        "u": f"{username}",
        "p": "kousic111",  # Here is where you need to change the key||
    }

    # Send the POST request with custom headers and JWT token
    response = requests.get(url, headers=headers)
    try:
        response_json = json.loads(response.content)
        enc_string = response_json["message"]
        print(enc_string)
        # enc_string = enc_string.strip("[]")  # Remove the square brackets from the string
        # enc_string = enc_string.replace("'", "")  # Remove single quotes
        # enc_string = ast.literal_eval(enc_string)
        print("-========================================")

        print(enc_string)
        enc_string = decrypt(enc_string).split(", ")
        print(enc_string)
        return enc_string

    except (json.JSONDecodeError, KeyError):
        print("Failed to extract JWT token from response")
        return


# username = "kousic"
# get_user_data_from_db(username)


def require_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = session.get("authenticated")

        if not token:
            return redirect(url_for("LogIn"))

        try:
            payload = jwt.decode(token, skc, algorithms=["HS256"])

            # Verify client IP against the IP in the token payload
            client_ip = request.remote_addr
            token_ip = payload.get("ip")

            if token_ip and token_ip != client_ip:
                return redirect(url_for("LogIn"))

            # Verify user-agent header against the user-agent in the token payload
            client_user_agent = request.headers.get("User-Agent")
            token_user_agent = payload.get("user_agent")

            if token_user_agent and token_user_agent != client_user_agent:
                return redirect(url_for("LogIn"))

            return f(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("LogIn"))
        except jwt.InvalidTokenError:
            return redirect(url_for("LogIn"))

    return decorated_function


def getArt():
    art1 = read_file("./arts/1.html")
    art2 = read_file("./arts/2.html")

    random_number = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
    if random_number == 1:
        pile = art1
        a = "Yoav Kadosh"
        c = [pile, a]
        return c
    elif random_number == 2:
        pile = art2
        a = "Carlos Córdova"
        c = [pile, a]
        return c
    elif random_number == 3:
        pile = "<img src='https://images.pexels.com/photos/3113541/pexels-photo-3113541.png?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pexels.com/@jovydas/"
        c = [pile, a]
        return c

    elif random_number == 4:
        pile = "<img src='https://images.pexels.com/photos/167964/pexels-photo-167964.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pexels.com/@lanophotography/"
        c = [pile, a]
        return c

    elif random_number == 5:
        pile = "<img src='https://images.pexels.com/photos/1270184/pexels-photo-1270184.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pexels.com/@ahmedadly/"
        c = [pile, a]
        return c
    elif random_number == 6:
        pile = "<img src='https://images.pexels.com/photos/1540684/pexels-photo-1540684.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pexels.com/@ahmedadly/"
        c = [pile, a]
        return c
    elif random_number == 7:
        pile = "<img src='https://images.pexels.com/photos/991422/pexels-photo-991422.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pexels.com/@luis-ruiz/"
        c = [pile, a]
        return c
    elif random_number == 8:
        pile = "<img src='https://cdn.pixabay.com/photo/2023/08/11/05/57/ai-generated-8182861_1280.jpg' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pixabay.com/users/geralt-9301/"
        c = [pile, a]
        return c
    elif random_number == 9:
        pile = "<img src='https://cdn.pixabay.com/photo/2023/08/08/17/46/building-8177885_1280.jpg' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pixabay.com/users/geralt-9301/"
        c = [pile, a]
        return c
    elif random_number == 10:
        pile = "<img src='https://cdn.pixabay.com/photo/2016/07/22/16/29/fog-1535201_1280.jpg' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pixabay.com/users/lum3n-1066559/"
        c = [pile, a]
        return c
    elif random_number == 11:
        pile = "<img src='https://cdn.pixabay.com/photo/2023/08/12/18/41/ai-generated-8186233_1280.jpg' id='ima'> <style>#ima{width:49vw;height:400px;min-width:700px;}</style>"
        a = "pixabay.com/users/artspark-13342248/"
        c = [pile, a]
        return c
