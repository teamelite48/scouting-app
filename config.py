import os
import secrets


_PROD = os.environ.get("ENVIRONMENT") == "Prod"

class ProdConfig:
  def __init__(self):
    self.DEBUG = False
    self.PROD = _PROD
    self.MONGO_URI = os.environ('MONGO_URI')
    self.SECRET_KEY = secrets.token_hex()

class LocalConfig:
  def __init__(self):
    self.DEBUG = True
    self.PROD = _PROD
    self.MONGO_URI = "mongodb://mongo:mongo@db:27017/"
    self.SECRET_KEY = "15855e9e7f1fae497975c9dc8c3f758de0f91b4b650f50b1ac9fc81075b5b69a"


CONFIG = ProdConfig() if _PROD else LocalConfig()