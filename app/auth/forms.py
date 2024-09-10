#------CREACION DE LOS FORMULARIOS
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.auth.models import Usuario

#---funciones necesarias 
#funcion para detectar si el email ya habia sido registrado
def email_existe(form, campo):
    email = Usuario.query.filter_by(usuario_email=campo.data).first()
    if email:
        raise ValidationError("Este email ya esta siendo utilizado en otra cuenta")


#crear el fromulario de registro del usuario
class RegistroFormulario(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(4, 16, message="Entre 4 o 16 caracteres por favor")])
    email = StringField("Email", validators=[DataRequired(), Email(), email_existe])
    contrasena = PasswordField("Contrasena", validators=[DataRequired(), EqualTo("confirmar_contrasena", message="La contraseña debe coincidir")])
    confirmar_contrasena = PasswordField("Confrimacion", validators=[DataRequired(), EqualTo("contrasena", message="la contraseñas deben coincidir")])
    submit = SubmitField("Registrarte")


#crecion del fromulario de inciio de sesion
class LoginFormulario(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    contrasena = PasswordField("Contrasena", validators=[DataRequired()])
    mantenerte_logeado = BooleanField("Recordarme")
    submit = SubmitField("Entrar")


#creacion de un formulario  
class ScrapyFormulario(FlaskForm):
    articulo_buscar = StringField("Articulo", validators=[DataRequired()])
    submit= SubmitField("Buscar Articulo")

