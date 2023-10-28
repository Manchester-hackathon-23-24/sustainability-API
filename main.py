from flask import Flask
from utils.constants import SECRET_KEY

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

from routes import ALL

for blueprint in ALL:
    app.register_blueprint(blueprint)

if __name__ == '__main__':
    app.run(debug=True)