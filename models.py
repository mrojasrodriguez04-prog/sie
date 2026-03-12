from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empresario(db.Model):
    __tablename__ = 'empresario'

    id_empresario = db.Column(db.Integer, primary_key=True)
    nombres_completos = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    correo_personal = db.Column(db.String(120), nullable=False)
    tipo_persona = db.Column(db.Enum('Natural','Jurídica'), nullable=False)
    rol_empresario = db.Column(db.Enum('Propietario','Representante Legal','Otro'), nullable=False)
    
    empresas = db.relationship('Empresa', backref='empresario', cascade="all, delete")

class Sector(db.Model):
    __tablename__ = 'sector'
    id_sector = db.Column(db.Integer, primary_key=True)
    nombre_sector = db.Column(db.Enum('Primario','Secundario','Terciario','Cuaternario','Quinario'),nullable=False)
    subsectores = db.relationship('Subsector', backref='sector', lazy=True)

class Subsector(db.Model):
    __tablename__ = 'subsector'
    id_subsector = db.Column(db.Integer, primary_key=True)
    nombre_subsector = db.Column(db.String(100), nullable=False)
    id_sector = db.Column(db.Integer,db.ForeignKey('sector.id_sector'),nullable=False)
    empresas = db.relationship('Empresa', backref='subsector', lazy=True)

class Departamento(db.Model):
    __tablename__ = 'departamento'
    id_departamento = db.Column(db.Integer, primary_key=True)
    nombre_departamento = db.Column(db.Enum(
            'Amazonas','Antioquia','Arauca','Atlántico','Bolívar','Boyacá',
            'Caldas','Caquetá','Casanare','Cauca','Cesar','Chocó',
            'Córdoba','Cundinamarca','Guainía','Guaviare','Huila',
            'La Guajira','Magdalena','Meta','Nariño','Norte de Santander',
            'Putumayo','Quindío','Risaralda','San Andrés y Providencia',
            'Santander','Sucre','Tolima','Valle del Cauca','Vaupés','Vichada'
        ),nullable=False)
    ciudades = db.relationship('Ciudad', backref='departamento', lazy=True)

class Ciudad(db.Model):
    __tablename__ = 'ciudad'
    id_ciudad = db.Column(db.Integer, primary_key=True)
    nombre_ciudad = db.Column(db.String(100), nullable=False)
    id_departamento = db.Column(db.Integer,db.ForeignKey('departamento.id_departamento'),nullable=False)
    empresas = db.relationship('Empresa', backref='ciudad', lazy=True)

class Empresa(db.Model):
    __tablename__ = 'empresa'
    id_empresa = db.Column(db.Integer, primary_key=True)
    id_empresario = db.Column(db.Integer,db.ForeignKey('empresario.id_empresario',ondelete='CASCADE'),nullable=False)
    nombre_empresa = db.Column(db.String(150), nullable=False)
    tipo_oferta = db.Column(db.Enum('Productos','Servicios','Mixta'),nullable=False)
    actividad_economica = db.Column(db.String(150))
    tipo_persona_juridica = db.Column(db.Enum('SAS','LTDA','S.A.','S.C.A.','S. en C','Colectiva.'))
    tamano_empresa = db.Column(db.Enum('Micro','Pequeña','Mediana'),nullable=False)
    punto_venta = db.Column(db.Enum('Físico','Virtual','Mixto'),nullable=False)
    direccion_comercial = db.Column(db.String(150), nullable=False)
    numero_empleados = db.Column(db.Integer)
    telefono_contacto = db.Column(db.String(20))
    correo_empresarial = db.Column(db.String(120))
    sitio_web = db.Column(db.String(150))
    id_subsector = db.Column(db.Integer,db.ForeignKey('subsector.id_subsector'),nullable=False)
    id_ciudad = db.Column(db.Integer,db.ForeignKey('ciudad.id_ciudad'),nullable=False)