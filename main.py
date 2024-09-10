#-----------archivo principal
#pasar la creacion de la app
#contexto de la aplicacion
#creacion de la tabla de base de datos

from app import create_app, database
from app.auth.models import Usuario

#creamos la aplicacion indicando que su configuracion sera de produccion
aplicacion = create_app("production")

#para la creacion de la base de datos
with aplicacion.app_context():
    database.create_all() # creara todos los modelos osae tablas

    #si no hay un usuario en la base de datos, se crea el usaurio admin
    if not Usuario.query.filter_by(usuario_nombre="admin").first():
        Usuario.crear_usuario(
            usuario="admin",
            email="paseriformeVolador@gamil.com",
            contrasena="admin"
        )


    #corremos la aplicacion
    aplicacion.run()
