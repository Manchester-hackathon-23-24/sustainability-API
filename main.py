from flask import Flask

app = Flask(__name__)

from routes import ALL

for blueprint in ALL:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)