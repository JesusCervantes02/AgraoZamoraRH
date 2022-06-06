from ast import For, In, Str
from distutils.log import error
import json
from linecache import lazycache
from tkinter.tix import Select

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import VARCHAR, Column, Integer, PrimaryKeyConstraint, String, ForeignKey, Date, Boolean, BLOB, Time, Float, null
from flask_login import UserMixin, current_user
from sqlalchemy.orm import relationship
db = SQLAlchemy()


#Bloque Empleados
db = SQLAlchemy()


class Empleados(UserMixin, db.Model):
    __tablename__ = 'empleados'
    idEmpleado = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    apellidoPaterno = Column(String(30), nullable=False)
    apellidoMaterno = Column(String(30), nullable=False)
    sexo = Column(String(1), nullable=False)
    fechaNacimiento = Column(Date, nullable=False)
    curp = Column(String(20), nullable=False)
    estadoCivil = Column(String(20), nullable=False)
    fechaContratacion = Column(Date, nullable=False)
    salarioDiario = Column(Float, nullable=False)
    nss = Column(String(10), nullable=False)
    diasVacaciones = Column(Integer, nullable=False)
    diasPermiso = Column(Integer, nullable=False)
    fotografia = Column(BLOB, nullable=True)
    direccion = Column(String(80), nullable=False)
    colonia = Column(String(50), nullable=False)
    codigoPostal = Column(String(5), nullable=False)
    escolaridad = Column(String(80), nullable=False)
    especialidad = Column(String(100), unique=True)
    email = Column(String(100), nullable=False)
    telefono = Column(String(12), nullable=False)
    password = Column(String(20), nullable=False)
    tipo = Column(String(15), nullable=False)
    estatus = Column(String(1), nullable=False)
    idDepartamento = Column(Integer, ForeignKey(
        'departamentos.idDepartamento'))
    idPuesto = Column(Integer, ForeignKey('puestos.idPuesto'))
    idCiudad = Column(Integer, ForeignKey('ciudades.idCiudad'))
    idSucursal = Column(Integer, ForeignKey('sucursales.idSucursal'))
    idTurno = Column(Integer, ForeignKey('turnos.idTurno'))

    departamentos = relationship('Departamentos', lazy='select')
    puestos = relationship('Puestos', lazy='select')
    ciudades = relationship('Ciudades', lazy='select')
    sucursales = relationship('Sucursales', lazy='select')
    turnos = relationship('Turnos', lazy='select')
    hp = relationship('HistorialPuestos', lazy='select')

#Métodos relacionados con el perfilamiento
    def is_authenticated(self):
        return True

    def is_active(self):
        if self.estatus == 'A':
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.idEmpleado

    def is_admin(self):
        if self.tipo == 'Administrador':
            return True
        else:
            return False

    def is_staff(self):
        if self.tipo == 'Staff':
            return True
        else:
            return False

    def is_empleado(self):
        if self.tipo == 'Empleado':
            return True
        else:
            return False

    def insertar(self):
        lista = []
        hp = HistorialPuestos()
        hp.idEmpleado = self.idEmpleado
        print(self.idEmpleado)
        hp.idPuesto = self.idPuesto
        hp.idDepartamento = self.idDepartamento
        hp.fechaInicio = self.fechaContratacion
        hp.salario = self.salarioDiario
        lista.append(hp)
        self.hp = lista
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def eliminar(self, id):
        obj = self.consultaIndividual(id)
        db.session.delete(obj)
        db.session.commit()

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

   #Consultar todos los empleados administrador
    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Empleados.idSucursal.asc()).order_by(Empleados.idDepartamento.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    
    #Consultar todos los empleados por sucursal
    def consultarPagina2(self,pagina,suc):
        paginacion=self.query.filter(Empleados.idSucursal==suc).order_by(Empleados.idDepartamento.asc()).order_by(Empleados.idDepartamento.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

    #Consultar los todos los empleados activos de una sucursal para darlo de alta en la nómina del periodo
    def consultarPagina3(self,pagina,suc):
        paginacion=self.query.filter(Empleados.idSucursal==suc).filter(Empleados.estatus=='A').order_by(Empleados.idDepartamento.asc()).order_by(Empleados.idDepartamento.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion


    def validar(self, email, password):
        usuario = None
        usuario = self.query.filter(
            Empleados.email == email, Empleados.password == password, Empleados.estatus == 'A').first()
        return usuario

    #Metodos ajax

    def consultarEmail(self, email):
        salida = {"estatus": "", "mensaje": ""}
        usuario = None
        usuario = self.query.filter(Empleados.email == email).first()
        if usuario != None:
            salida["estatus"] = "Error"
            salida["mensaje"] = "El correo "+email + \
                " ya ha sido registrado. Intente con otro"
        else:
            salida["estatus"] = "Ok"
            salida["mensaje"] = "El correo " + email + " esta libre"
        return salida

    def consultarNss(self, nss):
        salida = {"estatus": "", "mensaje": ""}
        usuario = None
        usuario = self.query.filter(Empleados.nss == nss).first()
        if usuario != None:
            salida["estatus"] = "Error"
            salida["mensaje"] = "El numero de seguro social: " + \
                nss+" pertenece a otra persona"
        else:
            salida["estatus"] = "Ok"
            salida["mensaje"] = "El numero de seguro social: " + \
                nss + " esta libre"
        return salida

    def consultarTelelfono(self, telefono):
        salida = {"estatus": "", "mensaje": ""}
        usuario = None
        usuario = self.query.filter(Empleados.telefono == telefono).first()
        if usuario != None:
            salida["estatus"] = "Error"
            salida["mensaje"] = "El telefono: " + telefono + \
                " ya ha sido registrado. Intente con otro"
        else:
            salida["estatus"] = "Ok"
            salida["mensaje"] = "El telefono:: " + telefono + " esta libre"
        return salida

    def consultarCurp(self, curp):
        salida = {"estatus": "", "mensaje": ""}
        usuario = None
        usuario = self.query.filter(Empleados.curp == curp).first()
        if usuario != None:
            salida["estatus"] = "Error"
            salida["mensaje"] = "La CURP: "+curp+" pertenece a otra persona"
        else:
            salida["estatus"] = "Ok"
            salida["mensaje"] = "La CURP: " + curp + " esta libre"
        return salida

#Fin


#Bloque Sucursales
class Sucursales(db.Model):
    __tablename__ = 'sucursales'
    idSucursal = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    telefono = Column(String(12), nullable=False)
    direccion = Column(String(80), nullable=False)
    colonia = Column(String(50), nullable=False)
    codigoPostal = Column(String(5), nullable=False)
    presupuesto = Column(Float, nullable=False)
    estatus = Column(String(1), nullable=False)
    idCiudad = Column(Integer, ForeignKey('ciudades.idCiudad'))

    ciudades = relationship('Ciudades', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultarTelelfonoSuc(self, telefono):
        salida = {"estatus": "", "mensaje": ""}
        usuario = None
        usuario = self.query.filter(Sucursales.telefono == telefono).first()
        if usuario != None:
            salida["estatus"] = "Error"
            salida["mensaje"] = "El telefono: " + telefono + \
                " ya ha sido registrado. Intente con otro"
        else:
            salida["estatus"] = "Ok"
            salida["mensaje"] = "El telefono:: " + telefono + " esta libre"
        return salida

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Sucursales.idSucursal.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

#Bloque Departamentos
class Departamentos(db.Model):
    __tablename__ = 'departamentos'
    idDepartamento = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Departamentos.idDepartamento.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion



#Fin

#Bloque Estados


class Estados (db.Model):
    __tablename__ = 'estados'
    idEstado = Column(Integer, primary_key=True)
    nombre = Column(String(60), nullable=False)
    siglas = Column(String(10), nullable=False, unique=True)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()
    
    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Estados.idEstado.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

# Fin

#Bloque turnos


class Turnos(db.Model):
    __tablename__ = 'turnos'
    idTurno = Column(Integer, primary_key=True)
    nombre = Column(String(20), unique=True, nullable=False)
    horaInicio = Column(Time, nullable=False)
    horaFin = Column(Time, nullable=False)
    dias = Column(String(60), nullable=True)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Turnos.idTurno.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion




#Fin

#Bloque puestos


class Puestos (db.Model):
    __tablename__ = 'puestos'
    idPuesto = Column(Integer, primary_key=True)
    nombre = Column(String(60), nullable=False)
    salarioMinimo = Column(Float, nullable=False)
    salarioMaximo = Column(Float, nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultaPuestos(self, id, salarioDiario):
        salida = {"estatus": "", "mensaje": ""}
        cosa = self.consultaIndividual(id)
        if(float(salarioDiario) >= cosa.salarioMinimo and float(salarioDiario) <= cosa.salarioMaximo):
            salida["estatus"] = "Ok"
            salida["mensaje"] = "El salario de " + cosa.nombre + " es valido"
        else:
            salida["estatus"] = "Error"
            salida["mensaje"] = "El salario que le deseas asignar al " + cosa.nombre + \
                " no se encunetra entre el rango de $ " + \
                str(cosa.salarioMinimo) + " - " + \
                str(cosa.salarioMaximo)+" MXN"

        return salida
    
    
    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Puestos.idPuesto.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion


#Fin


class Ciudades (db.Model):
    __tablename__ = 'ciudades'
    idCiudad = Column(Integer, primary_key=True)
    nombre = Column(String(80), nullable=False)
    idEstado = Column(Integer, ForeignKey('estados.idEstado'))
    estatus = Column(String(1), nullable=False)

    estados = relationship('Estados', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultaGeneral(self):
        #return self.to_json(self.query.all())
        return self.query.all()

    def consultaEstado(self,idEstado):
        lista=self.query.filter(Ciudades.idEstado==idEstado)
        cad=self.to_json(lista)
        return cad

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Ciudades.idEstado.asc()).paginate(pagina, per_page=20,error_out=False)
        return paginacion


    def to_json(self, lista):
        ciudades = {"estatus": "", "lista": ""}
        listaTemp = []
        for o in lista:
            ciudad = {"id": o.idCiudad, "nombre": o.nombre}
            listaTemp.append(ciudad)
        ciudades['lista'] = listaTemp
        return json.dumps(listaTemp)
    #fin

# Bloque formas de pago


class FormasDePago(db.Model):
    __tablename__ = 'formaspago'
    idFormaPago = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()


    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(FormasDePago.idFormaPago.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    # Fin

# Comentario pusiste mal un campo de la base de datos es fechaInicio y pusiste fechaIncio
# Periodos


class Periodos(db.Model):
    __tablename__ = 'periodos'
    idPeriodo = Column(Integer, primary_key=True)
    nombre = Column(String(50), nullable=False)
    fechaIncio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Periodos.idPeriodo.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    
    def consultarPagina2(self,pagina):
        paginacion=self.query.order_by(Periodos.fechaIncio.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion
# Fin

#Bloque Expedientes


class DocumentacionEmpleado(db.Model):
    __tablename__ = 'documentacionEmpleado'
    idDocumento = Column(Integer, primary_key=True)
    nombreDocumento = Column(String(80), nullable=False)
    fechaEntrega = Column(Date, nullable=False)
    ultimaModificacion = Column(Date, nullable=False)
    documento = Column(BLOB, nullable=False)
    idEmpleado = Column(Integer, ForeignKey('empleados.idEmpleado'))

    empleados = relationship('Empleados', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina,id):
        paginacion=self.query.filter(DocumentacionEmpleado.idEmpleado==id).order_by(DocumentacionEmpleado.idDocumento.asc()).paginate(pagina, per_page=5,error_out=False)
        return paginacion



#Bloque HistorialPuestos

class HistorialPuestos(db.Model):
    __tablename__ = 'historialPuestos'
    idHistorial = Column(Integer, primary_key=True)
    idEmpleado = Column(Integer, ForeignKey('empleados.idEmpleado'))
    idPuesto = Column(Integer, ForeignKey('puestos.idPuesto'))
    idDepartamento = Column(Integer, ForeignKey(
        'departamentos.idDepartamento'))
    fechaInicio = Column(Date, nullable=False)
    fechaFin = Column(Date, nullable=True)
    salario = Column(Float, nullable=False)

    empleados = relationship('Empleados', lazy='select')
    puestos = relationship('Puestos', lazy='select')
    departamentos = relationship('Departamentos', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina,id):
        paginacion=self.query.filter(HistorialPuestos.idEmpleado==id).order_by(HistorialPuestos.idHistorial.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion


#Bloque Asistencias

class Asistencias(db.Model):
    __tablename__ = 'Asistencias'
    idAsistencia = Column(Integer, primary_key=True)
    fecha = Column(Date, nullable=False)
    horaEntrada = Column(Time, nullable=False)
    horaSalida = Column(Time)
    dia = Column(String(10), nullable=False)
    idEmpleado = Column(Integer, ForeignKey('empleados.idEmpleado'))

    empleados = relationship('Empleados', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina,id):
        paginacion=self.query.filter(Asistencias.idEmpleado==id).order_by(Asistencias.fecha.desc()).paginate(pagina, per_page=6,error_out=False)
        return paginacion




#Bloque de percepciones


class Percepciones(db.Model):
    __tablename__ = 'percepciones'
    idPercepcion = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(String(80), nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Percepciones.idPercepcion.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion


#Bloque de deducciones


class Deducciones(db.Model):
    __tablename__ = 'deducciones'
    idDeduccion = Column(Integer, primary_key=True)
    nombre = Column(String(30), nullable=False)
    descripcion = Column(String(80), nullable=False)
    porcentaje = Column(Integer, nullable=False)
    estatus = Column(String(1), nullable=False)

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina):
        paginacion=self.query.order_by(Deducciones.idDeduccion.asc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

#Bloque AusenciasJustificadas
class AusenciasJustificadas(db.Model):
    __tablename__='AusenciasJustificadas'
    idAusencia=Column(Integer,primary_key=True)
    fechaSolicitud=Column(Date, nullable=False)
    fechaInicio=Column(Date,nullable=False)
    fechaFin=Column(Date,nullable=False)
    tipo=Column(String(1),nullable=False)
    idEmpleadoSolicita=Column(Integer,ForeignKey('empleados.idEmpleado'))
    idEmpleadoAutoriza = Column(Integer, ForeignKey('empleados.idEmpleado'))
    evidencia =Column(BLOB, nullable=True)
    estatus=Column(String,nullable=False)
    motivo=Column(String,nullable=False)
    dias=Column(Integer,nullable=False)
    observaciones=Column(String(100),nullable=True)

    empleadoSolicita= relationship('Empleados',foreign_keys=[idEmpleadoSolicita] ,lazy='select')
    empleadoAutoriza=relationship('Empleados',foreign_keys=[idEmpleadoAutoriza],lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

##Consulta para los chalanes
    def consultarPagina(self,pagina,id):
        paginacion=self.query.filter(AusenciasJustificadas.idEmpleadoSolicita==id).order_by(AusenciasJustificadas.fechaSolicitud.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

##Consulta para jefes de departamento de sus empleados a su cargo
    def consultaPagina2(self,pagina,id, st):
        paginacion=self.query.filter(AusenciasJustificadas.empleadoSolicita.has(idDepartamento=id)).filter(AusenciasJustificadas.estatus==st).filter(
            AusenciasJustificadas.idEmpleadoSolicita!=current_user.idEmpleado).filter(AusenciasJustificadas.empleadoSolicita.has(idSucursal=current_user.idSucursal)).order_by(
                AusenciasJustificadas.fechaSolicitud.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

##Consultas jefes de RH
    def consultaPagina3(self,pagina,st):
        paginacion=self.query.filter(AusenciasJustificadas.estatus==st).filter(AusenciasJustificadas.empleadoSolicita.has(idSucursal=current_user.idSucursal)).filter(
            AusenciasJustificadas.idEmpleadoSolicita!=current_user.idEmpleado).order_by(AusenciasJustificadas.fechaSolicitud.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

##Consultas para el admin
    def consultaPagina4(self,pagina, st):
        paginacion=self.query.filter(AusenciasJustificadas.estatus==st).order_by(AusenciasJustificadas.fechaSolicitud.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion

##Consulta particular de los empleados "Solo arroja sus solicitudes"
    
    def consultarPagina5(self,pagina,id):
        paginacion=self.query.filter(AusenciasJustificadas.idEmpleadoSolicita==id).order_by(AusenciasJustificadas.fechaSolicitud.desc()).paginate(pagina, per_page=10,error_out=False)
        return paginacion
#Fin

#Bloque Nominas
class Nominas(db.Model):
    __tablename__='nominas'
    idNomina=Column(Integer, primary_key=True)
    fechaElaboracion=Column(Date, nullable=False)
    fechaPago=Column(Date,nullable=False)
    subtotal=Column(Float,nullable=False)
    retenciones=Column(Float, nullable=False)
    total=Column(Float,nullable=False)
    diasTrabajados=Column(Integer,nullable=False)
    estatus=Column(String(1), nullable=False)
    idEmpleado=Column(Integer, ForeignKey('empleados.idEmpleado'))
    idFormaPago=Column(Integer,ForeignKey('formaspago.idFormaPago'))
    idPeriodo=Column(Integer,ForeignKey('periodos.idPeriodo'))

    empleados = relationship('Empleados', lazy='select')
    formasPago=relationship('FormasDePago', lazy='select')
    periodos=relationship('Periodos', lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    #Consultar si la nómina de un empleado fue dada de alta en un periodo de pago determinado

    def consultarEmpleadoNomina(self,idEmpleado,idPeriodo):
        salida={"estatus":"","mensaje":""}
        nomina=None
  
        usuario=self.query.filter(Nominas.idEmpleado==idEmpleado).filter(Nominas.idPeriodo==idPeriodo).first()
        if usuario!=None:
            salida["estatus"]="Error"
            salida["mensaje"]= "La nomina del empleado que seleccionaste. Ya ha sido dada de alta en el periodo."
        else:
            salida["estatus"]="Ok"
            salida["mensaje"]= "Nomina dada de alta de manera correcta"

        return salida


    #Consultar la nóminas que se se "generaron" en determinado periodo
    def consultarPagina(self,pagina,per,suc):
        paginacion=self.query.filter(Nominas.idPeriodo==per).filter(Nominas.estatus=='G').filter(Nominas.empleados.has(idSucursal=suc)).order_by(
            Nominas.fechaElaboracion).paginate(pagina, per_page=10,error_out=False)
        return paginacion

    #Consultar las nóminas "capturadas"
    def consultarPagina2(self,pagina,per,suc):
        paginacion=self.query.filter(Nominas.idPeriodo==per).filter(Nominas.estatus=='C').filter(Nominas.empleados.has(idSucursal=suc)).order_by(
            Nominas.fechaElaboracion).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    
    #Consultar las nóminas en  proceso de "revisión"
    def consultarPagina3(self,pagina,per,suc):
        paginacion=self.query.filter(Nominas.idPeriodo==per).filter(Nominas.estatus=='R').filter(Nominas.empleados.has(idSucursal=suc)).order_by(
            Nominas.fechaElaboracion).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    
    #Consultar la nóminas que han sido autorizadas para pago
    def consultarPagina4(self,pagina,per,suc):
        paginacion=self.query.filter(Nominas.idPeriodo==per).filter(Nominas.estatus=='A').filter(Nominas.empleados.has(idSucursal=suc)).order_by(
            Nominas.fechaElaboracion).paginate(pagina, per_page=10,error_out=False)
        return paginacion
    
    #Consulta individual de cada wey
    def consultarPagina5(self,pagina):
        paginacion=self.query.filter(Nominas.idEmpleado==current_user.idEmpleado).filter(Nominas.estatus=='A').order_by(
            Nominas.idPeriodo).paginate(pagina, per_page=10,error_out=False)
        return paginacion






#Fin


#Bloque Nominas deducciones
class NominasDeducciones(db.Model):
    __tablename__='NominasDeducciones'
    idNomDe=Column(Integer, primary_key=True)
    idDeduccion=Column(Integer, ForeignKey('deducciones.idDeduccion'))
    idNomina=Column(Integer,ForeignKey('nominas.idNomina'))
    importe=Column(Float,nullable=False)

    nominas= relationship('Nominas', lazy='select')
    deducciones=relationship('Deducciones',lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()

    def consultarPagina(self,pagina,nomina):
        paginacion=self.query.filter(NominasDeducciones.idNomina==nomina).order_by(NominasDeducciones.idNomDe.asc()).paginate(pagina, per_page=15,error_out=False)
        return paginacion

#Fin

#Bloque Percepciones
class NominasPercepciones(db.Model):
    __tablename__='NominasPercepciones'
    idNomPe=Column(Integer,primary_key=True)
    idPercepcion=Column(Integer, ForeignKey('percepciones.idPercepcion') )
    idNomina=Column(Integer,ForeignKey('nominas.idNomina'))
    diasPagados=Column(Integer,nullable=False)
    importe=Column(Float,nullable=False)

    nominas= relationship('Nominas', lazy='select')
    percepciones=relationship('Percepciones',lazy='select')

    def insertar(self):
        db.session.add(self)
        db.session.commit()

    def consultaIndividual(self, id):
        return self.query.get(id)

    def actualizar(self):
        db.session.merge(self)
        db.session.commit()

    def consultaGeneral(self):
        return self.query.all()

    def eliminar(self, id):
        objeto = self.consultaIndividual(id)
        db.session.delete(objeto)
        db.session.commit()
    
    def consultarPagina(self,pagina,nomina):
        paginacion=self.query.filter(NominasPercepciones.idNomina==nomina).order_by(NominasPercepciones.importe.asc()).paginate(pagina, per_page=15,error_out=False)
        return paginacion


