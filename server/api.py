from flask import Flask, request, jsonify
import microservices as ms


app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Welcome to the AI Model API!"    


@app.route('/get_response', methods=['POST'])
def get_response_route():
    data = request.get_json()
    response = ms.get_response(data)
    return jsonify(response)






if __name__ == '__main__':
    app.run(debug=True)