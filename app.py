from flask import Flask, request, render_template, redirect, url_for,flash
from models import db, Empresario, Subsector, Ciudad, Empresa


app= Flask(__name__)
app.secret_key = 'proyecto_sie'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/sie' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

TIPO_PERSONA = ['Natural','Jurídica']
ROL_EMPRESARIO = ['Propietario','Representante Legal','Otro']

@app.route("/")
def inicio():
    return render_template("index.html")

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

    return redirect(url_for("listar_empresario"))



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

@app.route("/empresa/registrar")
def registrar_empresa():

    empresarios = Empresario.query.all()
    subsectores = Subsector.query.all()
    ciudades = Ciudad.query.all()

    return render_template(
        "registrar_empresa.html",
        empresarios=empresarios,
        subsectores=subsectores,
        ciudades=ciudades
    )

@app.route("/empresa/guardar", methods=["POST"])
def guardar_empresa():

    nueva_empresa = Empresa(
        id_empresario = request.form["empresario"],
        nombre_empresa = request.form["nombre_empresa"],
        tipo_oferta = request.form["tipo_oferta"],
        actividad_economica = request.form["actividad"],
        tipo_persona_juridica = request.form["tipo_persona"],
        tamano_empresa = request.form["tamano"],
        punto_venta = request.form["punto_venta"],
        direccion_comercial = request.form["direccion"],
        numero_empleados = request.form["empleados"],
        telefono_contacto = request.form["telefono"],
        correo_empresarial = request.form["correo"],
        sitio_web = request.form["web"],
        id_subsector = request.form["subsector"],
        id_ciudad = request.form["ciudad"]
    )

    db.session.add(nueva_empresa)
    db.session.commit()

    flash("Empresa registrada correctamente")

    return redirect(url_for("listar_empresa"))

@app.route("/empresa/listar")
def listar_empresa():

    empresas = Empresa.query.all()

    return render_template(
        "listar_empresa.html",
        empresas=empresas
    )
    
@app.route("/empresa/eliminar/<int:id>")
def eliminar_empresa(id):

    empresa = Empresa.query.get(id)

    db.session.delete(empresa)
    db.session.commit()

    flash("Empresa eliminada correctamente")

    return redirect(url_for("listar_empresa"))

if __name__ == "__main__":
    app.run(debug=True)