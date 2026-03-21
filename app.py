from flask import Flask, request, render_template, redirect, session, url_for,flash
from werkzeug.security import check_password_hash, generate_password_hash
from models import db, Empresario, Subsector, Ciudad, Empresa, Usuario, Sede,RedSocial



app= Flask(__name__)
app.secret_key = 'proyecto_sie'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sie' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

TIPO_PERSONA = ['Natural','Jurídica']
ROL_EMPRESARIO = ['Propietario','Representante Legal','Otro']

@app.route("/")
def inicio():
    return render_template("login.html")


# LOGIN
@app.route("/validar_login", methods=["POST"])
def validar_login():

    usuario = Usuario.query.filter_by(email=request.form["email"]).first()

    if usuario and check_password_hash(usuario.password, request.form["password"]):

        session["usuario_id"] = usuario.id_usuario
        session["tipo_usuario"] = usuario.tipo_usuario
        session["nombre"] = usuario.nombres

        if usuario.tipo_usuario == "admin":
            return redirect(url_for("panel"))

 
        return redirect(url_for("panel"))

    else:
        flash("Datos incorrectos")
        return redirect(url_for("inicio"))


@app.route("/panel")
def panel():

    if "usuario_id" not in session:
        return redirect(url_for("inicio"))

    return render_template("Panel.html", tipo=session["tipo_usuario"], nombre=session["nombre"])


#Usuario Registro
@app.route("/registro_usuario")
def registro_usuario():

    if session.get("tipo_usuario") != "admin":
        return redirect(url_for("panel"))

    return render_template("registro.html")


@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():

    if session.get("tipo_usuario") != "admin":
        return "Acceso denegado"
    
    email = request.form["email"]

    usuario_existente = Usuario.query.filter_by(email=email).first()

    if usuario_existente:
        flash("⚠️ El correo ya está registrado")
        return redirect(url_for("registro_usuario"))

    password = generate_password_hash(request.form["password"])
    

    nuevo = Usuario(
        nombres=request.form["nombres"],
        apellidos=request.form["apellidos"],
        tipo_doc=request.form["tipo_doc"],
        numero_doc=request.form["numero_doc"],
        email=request.form["email"],
        password=password,
        tipo_usuario=request.form["tipo_usuario"]
    )

    db.session.add(nuevo)
    db.session.commit()

    flash("Usuario creado correctamente")
    return redirect(url_for("panel"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("inicio"))



#Empresarios y Empresas

@app.route("/registrar_empresario")
def registrar_empresario():

    return render_template(
        "registrar_empresario.html",
        tipos=TIPO_PERSONA,
        roles=ROL_EMPRESARIO
    )

@app.route("/guardar_empresario", methods=["POST"])
def guardar_empresario():

    nombres = request.form["nombres"]
    apellidos = request.form["apellidos"]
    correo = request.form["correo"]
    tipo = request.form["tipo"]
    rol = request.form["rol"]
    
    correo_existente = Empresario.query.filter_by(correo_personal=correo).first()

    if correo_existente:
        flash("⚠️ Este correo ya está registrado")
        return redirect(url_for("registrar_empresario"))

    nuevo = Empresario(
        nombres_completos=nombres,
        apellidos=apellidos,
        correo_personal=correo,
        tipo_persona=tipo,
        rol_empresario=rol
    )

    db.session.add(nuevo)
    db.session.commit()

    flash("Empresario registrado correctamente")

    return redirect(url_for("listar_empresarios"))

@app.route("/empresarios")
def listar_empresarios():

    empresarios = Empresario.query.all()

    return render_template("listar_empresarios.html", empresarios=empresarios)

@app.route("/eliminar_empresario/<int:id>")

def eliminar_empresario(id):

    empresario = Empresario.query.get(id)

    db.session.delete(empresario)
    db.session.commit()

    flash("Empresario eliminado correctamente")

    return redirect(url_for("listar_empresarios"))




@app.route("/empresa/registrar/<int:id>")
def registrar_empresa(id):
    
    empresario = Empresario.query.filter_by(id_empresario=id).first()

    if not empresario:
        flash("Empresario no encontrado")
        return redirect(url_for("listar_empresarios"))
    
    subsectores = Subsector.query.all()
    ciudades = Ciudad.query.all()

    return render_template(
        "registrar_empresa.html",
        empresario=empresario,
        subsectores=subsectores,
        ciudades=ciudades
    )

@app.route("/empresa/guardar/<int:id_empresario>", methods=["POST"])
def guardar_empresa(id_empresario):

    nueva_empresa = Empresa(
        id_empresario=id_empresario,
        nombre_empresa=request.form["nombre_empresa"],
        tipo_oferta=request.form["tipo_oferta"],
        actividad_economica=request.form["actividad"],
        tipo_persona_juridica=request.form["tipo_persona"],
        tamano_empresa=request.form["tamano"],
        punto_venta=request.form["punto_venta"],
        direccion_comercial=request.form["direccion"],
        numero_empleados=request.form["empleados"],
        telefono_contacto=request.form["telefono"],
        correo_empresarial=request.form["correo"],
        sitio_web=request.form["web"],
        id_subsector=request.form["subsector"],
        id_ciudad=request.form["ciudad"]
    )

    db.session.add(nueva_empresa)
    db.session.commit()

    flash("Empresa registrada correctamente")

    return redirect(url_for("empresas_por_empresario", id=id_empresario))


@app.route("/empresario/<int:id>/empresas")
def empresas_por_empresario(id):

    empresario = Empresario.query.get_or_404(id)
    empresas = Empresa.query.filter_by(id_empresario=id).all()

    return render_template(
        "empresas_por_empresario.html",
        empresas=empresas,
        empresario=empresario
    )

    
@app.route("/empresa/eliminar/<int:id>")
def eliminar_empresa(id):

    empresa = Empresa.query.get(id)
    id_empresario = empresa.id_empresario

    db.session.delete(empresa)
    db.session.commit()

    flash("Empresa eliminada correctamente")

    return redirect(url_for(
        "empresas_por_empresario",
        id=id_empresario
    ))



#Sedes
@app.route("/sede/nueva/<int:id_empresa>")
def nueva_sede(id_empresa):

    empresa = Empresa.query.get_or_404(id_empresa)
    empresario = Empresario.query.get(empresa.id_empresario)
    return render_template("registrar_sede.html", empresa=empresa, empresario=empresario)

@app.route("/guardar_sede/<int:id_empresa>", methods=["POST"])
def guardar_sede(id_empresa):

    nueva = Sede(
        id_empresa=id_empresa,
        nombre_sede=request.form["nombre_sede"],
        direccion=request.form["direccion"]
    )

    db.session.add(nueva)
    db.session.commit()

    flash("Sede registrada correctamente")

    return redirect(url_for("listar_sedes", id_empresa=id_empresa))

@app.route("/empresa/<int:id_empresa>/sedes")
def listar_sedes(id_empresa):

    empresa = Empresa.query.get_or_404(id_empresa)
    sedes = Sede.query.filter_by(id_empresa=id_empresa).all()
    empresario = Empresario.query.get(empresa.id_empresario)

    return render_template(
        "listar_sedes.html",
        sedes=sedes,
        empresa=empresa,
        empresario=empresario
    )

@app.route("/sede/eliminar/<int:id>")
def eliminar_sede(id):

    sede = Sede.query.get(id)
    id_empresa = sede.id_empresa

    db.session.delete(sede)
    db.session.commit()

    flash("Sede eliminada correctamente")

    return redirect(url_for("listar_sedes", id_empresa=id_empresa))

#redes_sociales
@app.route("/red/nueva/<int:id_empresa>")
def nueva_red(id_empresa):

    empresa = Empresa.query.get_or_404(id_empresa)
    empresario = Empresario.query.get(empresa.id_empresario)
    return render_template("registrar_red.html", empresa=empresa, empresario=empresario)

@app.route("/guardar_red/<int:id_empresa>", methods=["POST"])
def guardar_red(id_empresa):

    nueva = RedSocial(
        id_empresa=id_empresa,
        tipo_red=request.form["tipo_red"],
        url_red=request.form["url_red"]
    )

    db.session.add(nueva)
    db.session.commit()

    flash("Red social registrada correctamente")

    return redirect(url_for("listar_redes", id_empresa=id_empresa))

@app.route("/empresa/<int:id_empresa>/redes")
def listar_redes(id_empresa):

    empresa = Empresa.query.get_or_404(id_empresa)
    
    redes = RedSocial.query.filter_by(id_empresa=id_empresa).all()  
    empresario = Empresario.query.get(empresa.id_empresario)

    

    return render_template(
        "listar_redes.html",
        redes=redes,
        empresa=empresa,
        empresario=empresario 
    )
    
@app.route("/red/eliminar/<int:id>")
def eliminar_red(id):

    red = RedSocial.query.get(id)
    id_empresa = red.id_empresa

    db.session.delete(red)
    db.session.commit()

    flash("Red social eliminada correctamente")

    return redirect(url_for("listar_redes", id_empresa=id_empresa))
    

if __name__ == "__main__":
    app.run(debug=True)