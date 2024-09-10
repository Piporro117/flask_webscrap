#------configuraciones para modo produccion
DEBUG = True
SECRET_KEY = 'secreta'
SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/login_database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False