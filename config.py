import configparser
from os import environ, getenv

ENV = getenv('APP_ENV', 'DV')


class Config:
    """Configuration from environment variables."""
    config = configparser.ConfigParser()
    config.read('.env')

    if ENV in config:
      CONFIG = config[ENV]
    else:
       raise ValueError(f"Environment '{ENV}' not found in the env file.")

    ENVIRONMENT = CONFIG.get('ENVIRONMENT')
    MONGO_URI = CONFIG.get('MONGO_URI')
    SECRET_KEY = CONFIG.get('SECRET_KEY')
    FLASK_DEBUG = CONFIG.get('FLASK_DEBUG')
    FLASK_APP = "app.py"

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = False

    # Flask-Assets
    if ENVIRONMENT == "DV":
        # TODO: Consider adding the app reloading here
        pass
