#------CREACION DE LAS RUTAS
from flask import render_template, request, flash, redirect, url_for
from app.auth.forms import LoginFormulario, RegistroFormulario, ScrapyFormulario
from app.auth import authentication
from app.auth.models import Usuario
from flask_login import login_user, logout_user, login_required, current_user

#para el scrapy
from bs4 import BeautifulSoup
import requests
from lxml import etree #manejar la estructura de un html como si fuera python 


#ruta de registro de usuairos
@authentication.route("/registrarse", methods=["GET", "POST"])
def registrar_usuario():
    #si el usuario esta en sesion, ya esta logueado por lo que no podra ir a esta pagina
    if current_user.is_authenticated:
        flash("Ya estas con una cuenta")
        return redirect(url_for("authentication.pagina_principal"))
    
    form = RegistroFormulario()

    #si nos envia el formulario correctamente, se crea el usuario y redirige a la pagina de perfil
    if form.validate_on_submit():
        Usuario.crear_usuario(
            usuario=form.usuario.data,
            email= form.email.data,
            contrasena = form.contrasena.data
        )
        flash("Registro completado")
        return redirect(url_for("authentication.login_usuario"))
    

    return render_template("registrarse.html", form=form)
 

 #ruta raiz de nuestra blueprint
@authentication.route("/")
def index():
    return render_template("index.html")


#ruta del login
@authentication.route("/login", methods=['POST', 'GET'])
def login_usuario():
    if current_user.is_authenticated:
        flash("Ya estas con una cuenta iniciada")
        return redirect(url_for('authentication.pagina_principal'))
    
    form = LoginFormulario()

    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(usuario_email=form.email.data).first()

        #si no exite el usuario o la contrasena no es vaalida
        if not usuario or not usuario.checar_contrasena(form.contrasena.data):
            flash("Credenciales invalidas")
            return redirect(url_for('authentication.login_usuario'))

        #
        login_user(usuario, form.mantenerte_logeado.data)
        return redirect(url_for('authentication.pagina_principal'))

    return render_template('login.html', form=form)


#ruta pagina princial
@authentication.route('/pagina_principal')
@login_required
def pagina_principal():
    return render_template('home.html')


#ruta para salir de sesion
@authentication.route('/logout', methods=['GET'])
@login_required
def logout_usuario():
    logout_user()
    return redirect(url_for('authentication.login_usuario'))


#pagina para la busqueda de articulos
@authentication.route('/scrapy_data', methods=['GET', 'POST'])
@login_required
def scrapy_data():
    form = ScrapyFormulario()

    #funciona como post
    if form.validate_on_submit():
        busqueda = form.articulo_buscar.data
        url = f"https://listado.mercadolibre.com.mx/{busqueda}#D[A:{busqueda}]"
        response = requests.get(url=url)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack']//div[@class='ui-search-item__group ui-search-item__group--title']//a/@href")
        if len(data_articles) ==0:
           data = {"links":["No se encontro informacion para la consulta realizada"]}
        else:
            data = {"links":data_articles}
        return render_template("scrapy.html", **data)
    
    return render_template("scrapy.html", form=form)


#-------------ERRORES---------------------
@authentication.app_errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html')
