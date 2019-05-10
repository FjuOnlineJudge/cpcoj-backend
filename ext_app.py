from flask import Flask
from flask_wtf.csrf import CSRFProtect
import config
from exts import db

# https://stackoverflow.com/questions/19437883/when-scattering-flask-models-runtimeerror-application-not-registered-on-db-w
# https://stackoverflow.com/questions/46540664/no-application-found-either-work-inside-a-view-function-or-push-an-application
csrf = CSRFProtect()

def create_app():
	# Ini the flask app
	app = Flask(__name__)
	app.config.from_object(config)
	csrf.init_app(app)
	# Init the database
	db.init_app(app)
	return app

app = create_app()