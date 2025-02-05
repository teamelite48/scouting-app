from os import environ
from dotenv import load_dotenv


load_dotenv()

_PROD = environ.get("ENVIRONMENT") == "Prod"

class Config:
    """Configuration from environment variables."""
    ENVIRONMENT = environ.get("ENVIRONMENT")
    MONGO_URI = environ.get("MONGO_URI")
    SECRET_KEY = environ.get("SECRET_KEY")
    FLASK_DEBUG = environ.get("FLASK_DEBUG")
    FLASK_APP = "app.py"

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = False

    # Flask-Assets
    if ENVIRONMENT == "development":
        # TODO: Consider adding the app reloading here
        pass


class ProdConfig:
  def __init__(self):
    self.DEBUG = False
    self.PROD = _PROD
    self.MONGO_URI = environ.get('MONGO_URI')
    self.SECRET_KEY = environ.get("SECRET_KEY")


class LocalConfig:
  def __init__(self):
    self.DEBUG = True
    self.PROD = _PROD
    self.MONGO_URI = "mongodb://mongo:mongo@db:27017/"
    self.SECRET_KEY = "15855e9e7f1fae497975c9dc8c3f758de0f91b4b650f50b1ac9fc81075b5b69a"


CONFIG = ProdConfig() if _PROD else LocalConfig()
