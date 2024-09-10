#------CREACION DE LAS DATABASE
from datetime import datetime
from app import database, bcrypt #importamos los objetos de base de datos y encriptacion
from app import login_manager #paraa proteger las rutas
from flask_login import UserMixin #componentes para las tablas de usuarios


#creacion de la tabla usaurio
class Usuario(UserMixin, database.Model):
    #poner nombre a la tabla
    __tablename__ = "usuarios"

    #creacion de los atributos de la tabña
    id = database.Column(database.Integer, primary_key=True)
    usuario_nombre = database.Column(database.String(20))
    usuario_email = database.Column(database.String(60), unique=True, index=True) 
    usuario_contrasena = database.Column(database.String(80))
    creada_fecha = database.Column(database.DateTime, default=datetime.now)

    #funciones para realizar validaciones con los campos de las base de datos

    #recibe una contrasena, si la contrasena es igual a la de la base de datos, si no es pues no es la misma
    def checar_contrasena(self, contrasena):
        return bcrypt.check_password_hash(self.usuario_contrasena, contrasena)
    
    #metodo para crear los usuarios
    @classmethod
    def crear_usuario(cls, usuario, email, contrasena):
        usuario = cls(usuario_nombre=usuario,
                      usuario_email=email,
                      usuario_contrasena=bcrypt.generate_password_hash(contrasena).decode("utf-8")
                      )
        

        #agregar el objeto a la base de datos
        database.session.add(usuario)
        database.session.commit()
        return usuario
    

#crear un login manager, osea un cargador de usuarios, para ver que usuario esta logeado(activo o no activo)
@login_manager.user_loader
def load_user(id):
    return Usuario.query.get(int(id))

