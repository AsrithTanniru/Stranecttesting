from flask import Flask, request, jsonify, make_response, session
import jwt
import datetime
import pytz
import string
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Set the expiration time for JWT
JWT_EXPIRATION_MINUTES = 15  # 15 minutes

@app.after_request
def after_request(response):
    response.headers['Content-Type'] = 'application/json'
    return response

# Function to generate a random string
def generate_random_string(length=30):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

# Function to create a new JWT token
def create_jwt_token(username, client_ip):
    payload = {
        'username': username,
        'ip': client_ip,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES),
        'user_agent': request.headers.get('User-Agent')
    }
    secret_key = app.secret_key
    return jwt.encode(payload, secret_key, algorithm='HS256')

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Validate user credentials and generate JWT
    # In a real application, this would involve checking against a database
    # and verifying the password using secure hashing and salting techniques
    username = request.json['username']
    password = request.json['password']

    # Simulating successful authentication
    if username == 'valid_user' and password == 'secure_password':  
        client_ip = request.remote_addr
        jwt_token = create_jwt_token(username, client_ip)
        return jsonify({'token': jwt_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected_resource():
    # Validate JWT and enforce security measures
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Authorization header missing'}), 401

    try:
        payload = jwt.decode(token, app.secret_key, algorithms=['HS256'], audience='your_app_clients', issuer='your_app_name')
        
        # Verify client IP against the IP in the token payload
        client_ip = request.remote_addr
        token_ip = payload.get('ip')

        if token_ip and token_ip != client_ip:
            return jsonify({'message': 'IP verification failed'}), 403

        # Verify user-agent header against the user-agent in the token payload
        client_user_agent = request.headers.get('User-Agent')
        token_user_agent = payload.get('user_agent')

        if token_user_agent and token_user_agent != client_user_agent:
            return jsonify({'message': 'User-Agent verification failed'}), 403

        return jsonify({'message': 'Access granted'}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

if __name__ == '__main__':
    app.run(debug=True)






#####====Main Home====#####

# tok = session.get('authenticated')
#     if tok:
#         decoded_payload = jwt.decode(tok, skc, algorithms=['HS256'])
#         #return decoded_payload['username']
    
#         token = session.get('authenticated')
#         if not token:
#             return jsonify({'message': 'Authorization header missing'}), 401

#         try:
#             payload = jwt.decode(token, skc, algorithms=['HS256'])

#             # Verify client IP against the IP in the token payload
#             client_ip = request.remote_addr
#             token_ip = payload.get('ip')

#             if token_ip and token_ip != client_ip:
#                 return jsonify({'message': 'IP verification failed'}), 403

#             # Verify user-agent header against the user-agent in the token payload
#             client_user_agent = request.headers.get('User-Agent')
#             token_user_agent = payload.get('user_agent')

#             if token_user_agent and token_user_agent != client_user_agent:
#                 return jsonify({'message': 'User-Agent verification failed'}), 403

#             return jsonify({'message': 'Access granted'}), 200
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': 'Token expired'}), 401
#         except jwt.InvalidTokenError:
#             return jsonify({'message': 'Invalid token'}), 401