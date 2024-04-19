from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/user_data', methods=['POST'])
def user_data():
    data = request.get_json()

    print("data received:", data)
    return jsonify({"received_data": data})

if __name__ == '__main__':
    app.run(debug=True)