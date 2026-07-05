class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///coursemanager.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'dev-secret-key-change-in-production'
    DEBUG = True
