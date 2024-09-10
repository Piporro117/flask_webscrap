#---INICIALIZACION DEL BLUPRINT AUTH
from flask import Blueprint

#creacion del blueprint con su nombre e indicar donde estan sus templates
authentication = Blueprint("authentication", __name__, template_folder="templates")

#indicar donde estan sus rutas
from app.auth import views