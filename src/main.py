from flask import Flask
from flask_cors import CORS
from routes.entry import entry

app = Flask(__name__)

CORS(app)

app.register_blueprint(entry)

if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
