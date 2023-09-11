from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('test.html')

@app.route('/offer', methods=['POST'])
def offer():
    offer = json.loads(request.data)

    # For simplicity, we'll echo back the offer as the answer
    answer = offer
    
    return jsonify(answer)

if __name__ == '__main__':
    app.run()
