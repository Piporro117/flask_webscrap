#creacion de la aplicacion flask
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy #conectar a las base de datos
from flask_bootstrap import Bootstrap #implementar bootsrao
from flask_login import LoginManager
from flask_bcrypt import Bcrypt #encriptacion


#-----incializacion de objetos -----------------
database = SQLAlchemy()
bootstrap = Bootstrap()
bcrypt = Bcrypt()

login_manager = LoginManager()
login_manager.login_view = "authentication.login_usuario" #que vista se encarga de hacer el login
login_manager.session_protection = "strong" # que tan fuerte sea la proteccion del login manager

#-----creacion del metodo crear app, con parametro de que configuracion tendra--------------
def create_app(config_type):
    app = Flask(__name__)

    #---configuracion, la sacara del un archivo de la carpeta config
    #va a la cafpeta config, y busca el archivo que le digamos la configuracion en el archivo dado
    configuracion = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(configuracion)

    #--inicializacion de las demas cosas
    database.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    #---blueprints a pasar
    from app.auth import authentication
    app.register_blueprint(authentication)

    #-----regresar la app
    return app


