from calendar import month
from datetime import datetime
from datetime import date
from datetime import timedelta
import json
import pdfkit
from time import time
from flask import Flask, make_response, render_template, request, flash, redirect, abort, url_for
from flask_bootstrap import Bootstrap
from pymysql import OperationalError
from modelo.DAO import db, Departamentos, Turnos, Estados, Puestos, Ciudades, Empleados, FormasDePago, Periodos, Sucursales, DocumentacionEmpleado, \
    HistorialPuestos, Asistencias, Percepciones, Deducciones, AusenciasJustificadas, Nominas, NominasDeducciones, NominasPercepciones
from flask_login import current_user, login_user, logout_user, login_required, LoginManager

app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://userAgroRH:Hola.123@localhost/agroquimica_v1'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'cl4v3'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = u"¡Debes de iniciar sesión!"


@login_manager.user_loader
def load_user(id):
    return Empleados.query.get(int(id))


##Login
@app.route('/')
def inicio():
    return render_template('Comunes/login.html')


@app.route('/Empleados/validarSesion', methods=['post'])
def validarSesion():
    user = Empleados()
    email = request.form['email']
    password = request.form['password']
    user = user.validar(email, password)
    if user != None:
        login_user(user)
        return redirect(url_for('principal'))
    else:
        flash('! Datos de Sesión incorrectos !')
        return render_template('Comunes/login.html')


@app.route('/cerrarSesion')
def cerrarSesion():
    logout_user()
    return redirect(url_for('inicio'))


##Comunes
@app.route('/index')
def principal():
    return render_template('Comunes/index.html', )


@app.route('/catalogos')
def catalogos():
    return render_template('Comunes/catalogos.html')
#Errores


#Departamentos
@app.route('/departamentos/pagina/<int:page>')
def consultarPaginadepartamentos(page=1):
    try:
        d=Departamentos()
        paginacion=d.consultarPagina(page)
        departamentos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay departamentos registrados")
        departamentos=None
    return render_template('Departamentos/consulta.html', departamentos=departamentos, paginas=paginas, pagina=page)



@app.route('/departamentosNuevo')
def departamentosNuevo():
    return render_template('Departamentos/nuevo.html')


@app.route('/departementosAgregar', methods=['post'])
def departamentosAgregar():
    d = Departamentos()
    d.nombre = request.form['nombre']
    d.estatus = request.form['estatus']
    d.insertar()
    flash('¡Departamento registrado con éxito!')
    return render_template('Departamentos/nuevo.html')


@app.route('/departamentos/ver/<int:id>')
def departamentosConsultar(id):
    d = Departamentos()
    return render_template('Departamentos/modificar.html', departamentos=d.consultaIndividual(id))


@app.route('/departamentosActualizar', methods=['post'])
def departamentosActualizar():
    d = Departamentos()
    d.idDepartamento = request.form['id']
    d.nombre = request.form['nombre']
    d.estatus = request.form['estatus']
    d.actualizar()
    flash('¡Departamento actualizado con éxito!')
    return redirect(url_for('departamentosConsultar', id=d.idDepartamento))


@app.route('/departamentosEliminar/<int:id>')
def departamentosEliminar(id):
    d = Departamentos()
    d.eliminar(id)
    flash('¡Deparatamento eliminado con éxito!')
    return redirect(url_for('departamentos'))


#






#Turnos
@app.route('/turnos/pagina/<int:page>')
def consultarPaginaTurnos(page=1):
    try:
        t=Turnos()
        paginacion=t.consultarPagina(page)
        turnos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay turnos registrados")
        turnos=None
    return render_template('turnos/consulta.html', turnos=turnos, paginas=paginas, pagina=page)


@app.route('/turnosNuevo')
def turnosNuevo():
    return render_template('Turnos/nuevo.html')


@app.route('/turnosAgregar', methods=['post'])
def turnosAgregar():
    t = Turnos()
    t.nombre = request.form['nombre']
    t.horaInicio = request.form['horaInicio']
    t.horaFin = request.form['horaFin']
    t.dias = request.form['dias']
    t.insertar()
    flash('¡Turno registrado con éxito!')
    return render_template('Turnos/nuevo.html')


@app.route('/turnos/ver/<int:id>')
def turnosConsultar(id):
    t = Turnos()
    return render_template('Turnos/modificar.html', turnos=t.consultaIndividual(id))


@app.route('/turnosActualizar', methods=['post'])
def turnosActualizar():
    t = Turnos()
    t.idTurno = request.form['id']
    t.nombre = request.form['nombre']
    t.horaInicio = request.form['horaInicio']
    t.horaFin = request.form['horaFin']
    t.dias = request.form['dias']
    t.actualizar()
    flash('¡Turno actualizado con éxito!')
    return redirect(url_for('turnosConsultar', id=t.idTurno))


@app.route('/turnosEliminar/<int:id>')
def turnosEliminar(id):
    t = Turnos()
    t.eliminar(id)
    flash('¡Turno eliminado con éxito!')
    return redirect(url_for('turnos'))
#




#Estados

@app.route('/estados/pagina/<int:page>')
def consultarPaginaEstados(page=1):
    try:
        e=Estados()
        paginacion=e.consultarPagina(page)
        estados=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay estados registrados")
        estados=None
    return render_template('Estados/consulta.html', estados=estados, paginas=paginas, pagina=page)


@app.route('/estadosNuevo')
def estadosNuevo():
    return render_template('Estados/nuevo.html')


@app.route('/estadosAgregar', methods=['post'])
def estadosAgregar():
    e = Estados()
    e.nombre = request.form['nombre']
    e.siglas = request.form['siglas']
    e.estatus = request.form['estatus']
    e.insertar()
    flash('¡Estado registrado con éxito!')
    return render_template('Estados/nuevo.html')


@app.route('/estados/ver/<int:id>')
def estadosConsultar(id):
    e = Estados()
    return render_template('Estados/modificar.html', estados=e.consultaIndividual(id))


@app.route('/estadosActualizar', methods=['post'])
def estadosActualizar():
    e = Estados()
    e.idEstado = request.form['id']
    e.siglas = request.form['siglas']
    e.estatus = request.form['estatus']
    e.actualizar()
    flash('¡Estado actualizado con éxito!')
    return redirect(url_for('estadosConsultar', id=e.idEstado))


@app.route('/estadosEliminar/<int:id>')
def estadosEliminar(id):
    e = Estados()
    e.eliminar(id)
    flash('¡Estado eliminado con éxito!')
    return redirect(url_for('estados'))
#




#Puestos


@app.route('/puestos/pagina/<int:page>')
def consultarPaginaPuestos(page=1):
    try:
        p=Puestos()
        paginacion=p.consultarPagina(page)
        puestos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay puestos registrados")
        puestos=None
    return render_template('puestos/consulta.html', puestos=puestos, paginas=paginas, pagina=page)


@app.route('/puestosNuevo')
def puestosNuevo():
    return render_template('Puestos/nuevo.html')


@app.route('/puestosAgregar', methods=['post'])
def puestosAgregar():
    p = Puestos()
    p.nombre = request.form['nombre']
    p.salarioMinimo = request.form['salarioMinimo']
    p.salarioMaximo = request.form['salarioMaximo']
    p.estatus = request.form['estatus']
    p.insertar()
    flash('¡Puesto registrado con éxito!')
    return render_template('Puestos/nuevo.html')


@app.route('/puestos/ver/<int:id>')
def puestosConsultar(id):
    p = Puestos()
    return render_template('Puestos/modificar.html', puestos=p.consultaIndividual(id))


@app.route('/puestosActualizar', methods=['post'])
def puestosActualizar():
    p = Puestos()
    p.idPuesto = request.form['id']
    p.nombre = request.form['nombre']
    p.salarioMinimo = request.form['salarioMinimo']
    p.salarioMaximo = request.form['salarioMaximo']
    p.estatus = request.form['estatus']
    p.actualizar()
    flash('¡Puesto actualizado con éxito!')
    return redirect(url_for('puestosConsultar',id=p.idPuesto))


@app.route('/puestosEliminar/<int:id>')
def puestosEliminar(id):
    p = Puestos()
    p.eliminar(id)
    flash('¡Puesto eliminado con éxito!')
    return redirect(url_for('puestos'))

#

#Ciudades

@app.route('/ciudades/pagina/<int:page>')
def consultarPaginaCiudades(page=1):
    try:
        c=Ciudades()
        paginacion=c.consultarPagina(page)
        ciudades=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay ciudades registradas")
        ciudades=None
    return render_template('Ciudades/consulta.html', ciudades=ciudades, paginas=paginas, pagina=page)


@app.route('/ciudadesNuevo')
def ciudadesNuevo():
    e = Estados()
    estados = e.consultaGeneral()
    return render_template('Ciudades/nuevo.html', estados=estados)


@app.route('/ciudadesAgregar', methods=['post'])
def ciudadesAgregar():
    c = Ciudades()
    c.nombre = request.form['nombre']
    c.idEstado = request.form['estado']
    c.estatus = request.form['estatus']
    c.insertar()
    e = Estados()
    estados = e.consultaGeneral()
    flash('¡Ciudad registrada con éxito!')
    return render_template('Ciudades/nuevo.html', estados=estados)


@app.route('/ciudades/ver/<int:id>')
def ciudadesConsultar(id):
    c = Ciudades()
    e = Estados()
    return render_template('Ciudades/modificar.html', ciudades=c.consultaIndividual(id), estados=e.consultaGeneral())


@app.route('/ciudadesActualizar', methods=['post'])
def ciudadesActualizar():
    c = Ciudades()
    c.idCiudad = request.form['id']
    c.nombre = request.form['nombre']
    c.idEstado = request.form['estado']
    c.estatus = request.form['estatus']
    c.actualizar()
    flash('¡Ciudad actualizada con éxito!')
    return redirect(url_for('ciudadesConsultar',id=c.idCiudad))


@app.route('/ciudades/eliminar/<int:id>')
def ciudadesEliminar(id):
    c = Ciudades()
    c.eliminar(id)
    flash('¡Puesto eliminado con éxito!')
    return redirect(url_for('ciudades'))


#



#Formas de pago

@app.route('/formasPago/pagina/<int:page>')
def consultarPaginaformasPago(page=1):
    try:
        fp=FormasDePago()
        paginacion=fp.consultarPagina(page)
        formasPago=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay Formas de pago registradas")
        formasPago=None
    return render_template('formasPago/consulta.html', formasPago=formasPago, paginas=paginas, pagina=page)



@app.route('/formasPagoNuevo')
def formasPagoNuevo():
    return render_template('FormasPago/nuevo.html')


@app.route('/formasPagoAgregar', methods=['post'])
def formasPagoAgregar():
    fp = FormasDePago()
    fp.nombre = request.form['nombre']
    fp.estatus = 'A'
    fp.insertar()
    flash('¡Forma de pago registrada con éxito!')
    return render_template('FormasPago/nuevo.html')


@app.route('/formasPago/ver/<int:id>')
def formasPagoConsultar(id):
    fp = FormasDePago()
    return render_template('FormasPago/modificar.html', formasPago=fp.consultaIndividual(id))


@app.route('/formasPagoActualizar', methods=['post'])
def formasPagoActualizar():
    fp = FormasDePago()
    fp.idFormaPago = request.form['id']
    fp.nombre = request.form['nombre']
    fp.estatus = request.form['estatus']
    fp.actualizar()
    flash('¡Forma de pago actualizada con éxito!')
    return redirect(url_for('formasPagoConsultar', id=fp.idFormaPago))


#Fin



#Periodos
@app.route('/periodos/pagina/<int:page>')
def consultarPaginaPeriodos(page=1):
    try:
        p=Periodos()
        paginacion=p.consultarPagina(page)
        periodos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash('No hay periodos registrados')
        periodos=None
    return render_template('Periodos/consulta.html', periodos=periodos, paginas=paginas, pagina=page)

@app.route('/periodosNuevo')
def periodosNuevo():
    return render_template('Periodos/nuevo.html')


@app.route('/periodosAgregar', methods=['post'])
def periodosAgregar():
    p = Periodos()
    p.nombre = request.form['nombre']
    p.fechaIncio = request.form['fechaIncio']
    p.fechaFin = request.form['fechaFin']
    p.estatus = 'A'
    p.insertar()
    flash('¡Periodo registrado con éxito!')
    return render_template('Periodos/nuevo.html')


@app.route('/periodos/ver/<int:id>')
def periodoConsultar(id):
    p = Periodos()
    return render_template('Periodos/modificar.html', periodos=p.consultaIndividual(id))


@app.route('/periodosActualizar', methods=['post'])
def periodosActualizar():
    p = Periodos()
    p.idPeriodo = request.form['id']
    p.nombre = request.form['nombre']
    p.fechaIncio = request.form['fechaIncio']
    p.fechaFin = request.form['fechaFin']
    p.estatus = request.form['estatus']
    p.actualizar()
    flash('¡Periodo actualizado con éxito!')
    return redirect(url_for('periodoConsultar', id=p.idPeriodo))

#Fin



#Empleados

@app.route('/empleadosAdmin/pagina/<int:page>')
def consultarPaginaEmpleadosAdmin(page=1):
    try:
        e=Empleados()
        paginacion=e.consultarPagina(page)
        empleados=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay empleados registrados")
        empleados=None
    return render_template('Empleados/consulta.html', empleados=empleados, paginas=paginas, pagina=page)


@app.route('/empleadosStaff/pagina/<int:page>/<int:suc>')
def consultarPaginaEmpleadosStaff(suc,page=1):
    try:
        e=Empleados()
        paginacion=e.consultarPagina2(page,suc)
        empleados=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay empleados registrados")
        empleados=None
    return render_template('Empleados/consulta.html', empleados=empleados, paginas=paginas, pagina=page)



@app.route('/empleadosNuevo')
def empleadosNuevo():
    e = Estados()
    c = Ciudades()
    estados = e.consultaGeneral()
    ciudades = c.consultaGeneral()
    d = Departamentos()
    departamentos = d.consultaGeneral()
    p = Puestos()
    puestos = p.consultaGeneral()
    s = Sucursales()
    sucursales = s.consultaGeneral()
    t = Turnos()
    turnos = t.consultaGeneral()

    return render_template('Empleados/nuevo.html', estados=estados, ciudades=ciudades, departamentos=departamentos, puestos=puestos, sucursales=sucursales,
                           turnos=turnos)


@app.route('/empleadosAgregar', methods=['post'])
def empleadosAgregar():
    e = Empleados()
    hp = HistorialPuestos()
    e.nombre = request.form['nombre']
    e.apellidoPaterno = request.form['apellidoPaterno']
    e.apellidoMaterno = request.form['apellidoMaterno']
    e.sexo = request.form['sexo']
    e.fechaNacimiento = request.form['fechaNacimiento']
    e.curp = request.form['curp']
    e.estadoCivil = request.form['estadoCivil']
    e.fechaContratacion = request.form['fechaContratacion']
    e.salarioDiario = request.form['salarioDiario']
    e.nss = request.form['nss']
    e.diasVacaciones = request.form['diasVacaciones']
    e.diasPermiso = request.form['diasPermiso']
    e.fotografia = request.files['fotografia'].read()
    e.direccion = request.form['direccion']
    e.colonia = request.form['colonia']
    e.codigoPostal = request.form['codigoPostal']
    e.escolaridad = request.form['escolaridad']
    e.especialidad = request.form['especialidad']
    e.email = request.form['email']
    e.telefono = request.form['telefono']
    e.password = request.form['password']
    e.tipo = request.form['tipo']
    e.estatus = 'A'
    e.idDepartamento = request.form['idDepartamento']
    e.idPuesto = request.form['idPuesto']
    e.idCiudad = request.form['idCiudad']
    e.idSucursal = request.form['idSucursal']
    e.idTurno = request.form['idTurno']

    #Fin
    e.insertar()
    flash('¡Empleado registrado con éxito!')
    return redirect(url_for('empleadosNuevo'))


@app.route('/empleados/foto/<int:id>')
def consultarImagenEmpleado(id):
    e = Empleados()
    return e.consultaIndividual(id).fotografia


@app.route('/empleados/ver/<int:id>')
def empleadosConsultar(id):
    e = Empleados()
    es = Estados()
    c = Ciudades()
    d = Departamentos()
    p = Puestos()
    s = Sucursales()
    t = Turnos()

    hp = HistorialPuestos()
    histoPue = hp.consultaGeneral()


    verid = 0
    verpuesto = 0
    verempleado = 0
    verdepartamento = 0
    versueldo = 0
    verfecha = ""

    for h in histoPue:
        if (h.idEmpleado == id):
            if (h.fechaFin == None):
                verid = h.idHistorial
                verempleado = h.idEmpleado
                verpuesto = h.idPuesto
                verdepartamento = h.idDepartamento
                versueldo = h.salario
                verfecha = h.fechaInicio

    return render_template('Empleados/modificar.html', empleados=e.consultaIndividual(id), estados=es.consultaGeneral(), ciudades=c.consultaGeneral(),
                           departamentos=d.consultaGeneral(), puestos=p.consultaGeneral(), sucursales=s.consultaGeneral(), turnos=t.consultaGeneral(), verid=verid, verpuesto=verpuesto, verdepartamento=verdepartamento, versueldo=versueldo, verempleado=verempleado, verfecha=verfecha)



@app.route('/empleadosActualizar', methods=['post'])
def empleadosActualizar():
    e = Empleados()
    hp = HistorialPuestos()
    hpa = HistorialPuestos()
    e.idEmpleado = request.form['idEmpleado']
    e.nombre = request.form['nombre']
    e.apellidoPaterno = request.form['apellidoPaterno']
    e.apellidoMaterno = request.form['apellidoMaterno']
    e.sexo = request.form['sexo']
    e.fechaNacimiento = request.form['fechaNacimiento']
    e.curp = request.form['curp']
    e.estadoCivil = request.form['estadoCivil']
    e.fechaContratacion = request.form['fechaContratacion']
    e.nss = request.form['nss']
    e.diasVacaciones = request.form['diasVacaciones']
    e.diasPermiso = request.form['diasPermiso']
    foto = request.files['fotografia'].read()
    if foto:
        e.fotografia = foto

    e.direccion = request.form['direccion']
    e.colonia = request.form['colonia']
    e.codigoPostal = request.form['codigoPostal']
    e.escolaridad = request.form['escolaridad']
    e.especialidad = request.form['especialidad']
    e.email = request.form['email']
    e.telefono = request.form['telefono']
    e.password = request.form['password']
    e.tipo = request.form['tipo']
    e.idCiudad = request.form['idCiudad']
    e.idSucursal = request.form['idSucursal']
    e.idTurno = request.form['idTurno']

    ##Variables
    puesto = request.form['puestoActual']
    departamento = request.form['departamentoActual']
    salario = request.form['sueldoActual']
    historial = request.form['idActualHistorial']
    fechaInicio = request.form['fechaInicio']

    puestoNuevo = request.form['idPuesto']
    departamentoNuevo = request.form['idDepartamento']
    estatusNuevo = request.form['estatus']
    salarioNuevo = request.form['salarioDiario']

    if estatusNuevo == 'I':
        e.estatus = request.form['estatus']
        hpa.idHistorial = historial
        hpa.idEmpleado = request.form['idEmpleado']
        hpa.idPuesto = puesto
        hpa.idDepartamento = departamento
        hpa.fechaInicio = fechaInicio
        hpa.fechaFin = date.today()
        hpa.salario = salario
        hpa.actualizar()

    if(departamento != departamentoNuevo or puesto != puestoNuevo):
        hpa.idHistorial = historial
        hpa.idEmpleado = request.form['idEmpleado']
        hpa.idPuesto = puesto
        hpa.idDepartamento = departamento
        hpa.fechaInicio = fechaInicio
        hpa.fechaFin = date.today()
        hpa.salario = salario
        hpa.actualizar()

        e.idDepartamento = request.form['idDepartamento']
        e.idPuesto = request.form['idPuesto']
        e.salarioDiario = request.form['salarioDiario']

        hp.idEmpleado = request.form['idEmpleado']
        hp.idPuesto = request.form['idPuesto']
        hp.idDepartamento = request.form['idDepartamento']
        hp.fechaInicio = date.today()
        hp.salario = request.form['salarioDiario']
        hp.insertar()

    if(salario != salarioNuevo):
        e.salarioDiario = request.form['salarioDiario']

        hpa.idHistorial = historial
        hpa.idEmpleado = request.form['idEmpleado']
        hpa.idPuesto = puesto
        hpa.idDepartamento = departamento
        hpa.salario = request.form['salarioDiario']
        hpa.fechaInicio = fechaInicio
        hpa.actualizar()

    e.actualizar()

    flash('¡Empleado actualizado con éxito!')
    return redirect(url_for('empleadosConsultar', id=e.idEmpleado))

#####Modificar con currentUser


@app.route('/modificarCurrentUser')
def modificarCurrentUser():
    c = Ciudades()
    e = Estados()
    d = Departamentos()
    p = Puestos()
    s = Sucursales()
    t = Turnos()
    return render_template('Empleados/cumodificar.html', ciudades=c.consultaGeneral(), estados=e.consultaGeneral(),
                           departamentos=d.consultaGeneral(), puestos=p.consultaGeneral(), sucursales=s.consultaGeneral(), turnos=t.consultaGeneral())


@app.route('/actualizardatos', methods=['post'])
def actualizardatos():
    e = Empleados()
    e.idEmpleado = request.form['idEmpleado']
    e.estadoCivil = request.form['estadoCivil']
    foto = request.files['fotografia'].read()
    if foto:
        e.fotografia = foto
    e.direccion = request.form['direccion']
    e.colonia = request.form['colonia']
    e.codigoPostal = request.form['codigoPostal']
    e.escolaridad = request.form['escolaridad']
    e.especialidad = request.form['especialidad']
    e.email = request.form['email']
    e.telefono = request.form['telefono']
    e.password = request.form['password']
    e.idCiudad = request.form['idCiudad']
    e.actualizar()
    flash('¡Empleado actualizado con éxito!')
    return redirect(url_for('modificarCurrentUser'))


###Métodos AJAX empleados
@app.route('/empleados/email/<string:email>', methods=['get'])
def consultarEmail(email):
    e = Empleados()
    return json.dumps(e.consultarEmail(email))


@app.route('/empleados/nss/<string:nss>', methods=['get'])
def consultarNss(nss):
    e = Empleados()
    return json.dumps(e.consultarNss(nss))


@app.route('/empleados/curp/<string:curp>', methods=['get'])
def consultarCurp(curp):
    e = Empleados()
    return json.dumps(e.consultarCurp(curp))


@app.route('/empleados/telefono/<string:telefono>', methods=['get'])
def consultarTelefono(telefono):
    e = Empleados()
    return json.dumps(e.consultarTelelfono(telefono))


@app.route('/empleados/consultaPuestos/<int:idPuesto>/<string:salarioDiario>', methods=['get'])
def consultaPuestos(idPuesto, salarioDiario):
    p = Puestos()
    return json.dumps(p.consultaPuestos(idPuesto, salarioDiario))


#Fin


#Expedientes

@app.route('/expedientes/pagina/<int:id>/<int:page>')
def consultarPaginaExpedientes(id,page=1):
    try:
        e = Empleados()
        ex=DocumentacionEmpleado()
        paginacion=ex.consultarPagina(page,id)
        expedientes=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay expedientes registrados")
        expedientes=None
    return render_template('Expedientes/consulta.html', expedientes=expedientes, paginas=paginas, pagina=page,empleados=e.consultaIndividual(id))


@app.route('/expedientes/empleado/<int:id>')
def verDocumento(id):
    exp = DocumentacionEmpleado()
    return exp.consultaIndividual(id).documento


@app.route('/expedientes/ver/<int:id>')
def consultaExpedientes(id):
    exp = DocumentacionEmpleado()
    return render_template('Expedientes/modificar.html', expedientes=exp.consultaIndividual(id))


@app.route('/expedientes/Nuevo/<int:id>')
def expedientesNuevo(id):
    e = Empleados()
    return render_template('Expedientes/nuevo.html', empleados=e.consultaIndividual(id))


@app.route('/expedientesAgregar', methods=['post'])
def expedientesAgregar():
    ex = DocumentacionEmpleado()
    ex.nombreDocumento = request.form['nombreDocumento']
    ex.fechaEntrega = date.today()
    ex.ultimaModificacion = date.today()
    ex.documento = request.files['documento'].read()
    ex.idEmpleado = request.form['idEmpleado']

    ex.insertar()
    flash('¡Documento agregado al expediente con éxito!')
    return redirect(url_for('expedientesNuevo', id=ex.idEmpleado))


@app.route('/expedienteActualizar', methods=['post'])
def expedientesActualizar():
    ex = DocumentacionEmpleado()
    ex.idDocumento = request.form['idDocumento']
    ex.nombreDocumento = request.form['nombreDocumento']
    ex.fechaEntrega = request.form['fechaEntrega']
    ex.ultimaModificacion = date.today()
    archivito = request.files['documento'].read()
    if archivito:
        ex.documento = archivito
    ex.idEmpleado = request.form['idEmpleado']
    ex.actualizar()
    flash('¡Documento actualizado en el expediente con éxito!')
    return redirect(url_for('consultaExpedientes', id=ex.idDocumento))


@app.route('/expediente/eliminar/<int:id>')
def expedintesEliminar(id):
    exp = DocumentacionEmpleado()
    exp.eliminar(id)
    flash('¡Documento eliminado del expediente con éxito!')

    if current_user.is_authenticated() and (current_user.is_admin()):
        return redirect(url_for('consultarPaginaEmpleadosAdmin', page=1))
    
    if current_user.is_authenticated() and (current_user.is_staff()):
        return redirect(url_for('consultarPaginaEmpleadosStaff', suc=current_user.idSucursal, page=1))

###Current user expedientes

@app.route('/cuExpedientes/pagina/<int:id>/<int:page>')
def consultarPaginacuExpedientes(id,page=1):
    try:
        ex=DocumentacionEmpleado()
        paginacion=ex.consultarPagina(page,id)
        cuExpedientes=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay expedientes registrados")
        cuExpedientes=None
    return render_template('Expedientes/cuconsulta.html', cuExpedientes=cuExpedientes, paginas=paginas, pagina=page)



@app.route('/cuExpedientesNuevo')
def cuExpedientesNuevo():
    return render_template('Expedientes/cunuevo.html')


@app.route('/cuExpedientesAgregar', methods=['post'])
def cuExpedientesAgregar():
    ex = DocumentacionEmpleado()
    ex.nombreDocumento = request.form['nombreDocumento']
    ex.fechaEntrega = date.today()
    ex.ultimaModificacion = date.today()
    ex.documento = request.files['documento'].read()
    ex.idEmpleado = request.form['idEmpleado']

    ex.insertar()
    flash('¡Documento agregado al expediente con éxito!')
    return redirect(url_for('cuExpedientesNuevo'))


@app.route('/cuExpedientes/ver/<int:id>')
def cuConsultaExpedientes(id):
    exp = DocumentacionEmpleado()
    return render_template('Expedientes/cumodificar.html', expedientes=exp.consultaIndividual(id))


@app.route('/cuExpedientesActualizar', methods=['post'])
def cuExpedientesActualizar():
    ex = DocumentacionEmpleado()
    ex.idDocumento = request.form['idDocumento']
    ex.nombreDocumento = request.form['nombreDocumento']
    ex.fechaEntrega = request.form['fechaEntrega']
    ex.ultimaModificacion = date.today()
    archivito = request.files['documento'].read()
    if archivito:
        ex.documento = archivito
    ex.idEmpleado = request.form['idEmpleado']
    ex.actualizar()
    flash('¡Documento actualizado en el expediente con éxito!')
    return redirect(url_for('cuConsultaExpedientes', id=ex.idDocumento))


@app.route('/cuExpedientes/eliminar/<int:id>')
def cuExpedientesEliminar(id):
    exp = DocumentacionEmpleado()
    exp.eliminar(id)

    flash('¡Documento eliminado del expediente con éxito!')
    return redirect(url_for('consultarPaginacuExpedientes', page=1,id=current_user.idEmpleado))

#_____________________________________________________________Inicio de sucursales


@app.route('/sucursales/pagina/<int:page>')
def consultarPaginaSucursales(page=1):
    try:
        suc=Sucursales()
        paginacion=suc.consultarPagina(page)
        sucursales=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay sucursales registradas")
        sucursales=None
    return render_template('sucursales/consulta.html', sucursales=sucursales, paginas=paginas, pagina=page)



@app.route('/sucursalesNuevo')
def sucursalesNuevo():
    c = Ciudades()
    ciudades = c.consultaGeneral()
    e=Estados()
    estados=e.consultaGeneral()
    return render_template('Sucursales/nuevo.html', ciudades=ciudades, estados=estados)


@app.route('/sucursalesAgregar', methods=['post'])
def sucursalesAgregar():
    su = Sucursales()
    su.nombre = request.form['nombre']
    su.telefono = request.form['telefono']
    su.direccion = request.form['direccion']
    su.colonia = request.form['colonia']
    su.codigoPostal = request.form['codigoPostal']
    su.presupuesto = request.form['presupuesto']
    su.estatus = 'A'
    su.idCiudad = request.form['idCiudad']
    su.insertar()
    c = Ciudades()
    ciudades = c.consultaGeneral()
    flash('¡Sucursal registrada con éxito!')
    return render_template('Sucursales/nuevo.html', ciudades=ciudades)


@app.route('/sucursales/ver/<int:id>')
def sucursalesConsultar(id):
    su = Sucursales()
    c = Ciudades()
    e= Estados()
    return render_template('Sucursales/modificar.html', sucursales=su.consultaIndividual(id), ciudades=c.consultaGeneral(), estados=e.consultaGeneral())


@app.route('/sucursalesActualizar', methods=['post'])
def sucursalesActualizar():
    su = Sucursales()
    su.idSucursal = request.form['id']
    su.nombre = request.form['nombre']
    su.telefono = request.form['telefono']
    su.direccion = request.form['direccion']
    su.colonia = request.form['colonia']
    su.codigoPostal = request.form['codigoPostal']
    su.presupuesto = request.form['presupuesto']
    su.idCiudad = request.form['idCiudad']
    su.actualizar()
    flash('¡Sucursal actualizada con éxito!')
    return redirect(url_for('sucursalesConsultar', id=su.idSucursal))


@app.route('/sucursales/eliminar/<int:id>')
def sucursalesEliminar(id):
    su = Sucursales()
    su.eliminar(id)
    flash('¡Sucursal eliminada con éxito!')
    return redirect(url_for('sucursales'))

#Métodos ajax


@app.route('/sucursales/telefono/<string:telefono>', methods=['get'])
def consultarTelefonoSuc(telefono):
    s = Sucursales()
    return json.dumps(s.consultarTelelfonoSuc(telefono))
#_____________________________________________________________Fin de sucursales

#Asistencias
@app.route('/asistenciasCurrent/pagina/<int:id>/<int:page>')
def consultarPaginaAsistenciasCurrent(id, page=1):

   
    a=Asistencias()
    em = Empleados()
    asistencias2 = a.consultaGeneral()
    empleados = em.consultaGeneral()
    fechaActual = date.today()

    contador = 0

    for a in asistencias2:
      if(a.idEmpleado == current_user.idEmpleado):
          if(a.fecha == fechaActual):
            contador = 1

    print(contador)
    try:
        paginacion=a.consultarPagina(page,id)
        asistencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay asistencias registradas")
        asistencias=None
    return render_template('Asistencias/consulta.html', asistencias=asistencias, paginas=paginas, pagina=page, empleados=empleados, fechaActual=fechaActual, contador=contador, asistencias2=asistencias2)


@app.route('/AsistenciasCurrentEntrada', methods=['post'])
def AsistenciasCurrentEntrada():
   
    asis = Asistencias()
    asis.fecha = date.today()
    asis.horaEntrada = datetime.now().time()
    diaSemana = date.today().weekday()
    if diaSemana == 0:
        asis.dia = 'Lunes'
    elif diaSemana == 1:
        asis.dia = 'Martes'
    elif diaSemana == 2:
        asis.dia = 'Miercoles'
    elif diaSemana == 3:
        asis.dia = 'Jueves'
    elif diaSemana == 4:
        asis.dia = 'Viernes'
    elif diaSemana == 5:
        asis.dia = 'Sábado'
    else:
        asis.dia = 'Domingo'

    asis.idEmpleado = request.form['idEmpleado']
    asis.insertar()
    flash('¡Entrada registrada con éxito!')
    return redirect(url_for('consultarPaginaAsistenciasCurrent', page=1, id=current_user.idEmpleado))


@app.route('/AsistenciasCurretSalida/actualizar/<int:id>')
def AsistenciasCurrentSalida(id):
    asis = Asistencias()
    asis.idAsistencia = id
    asis.horaSalida = datetime.now().time()
    asis.actualizar()
    flash('Salida marcada con éxito')
    return redirect(url_for('consultarPaginaAsistenciasCurrent', page=1,id=current_user.idEmpleado))

@app.route('/asistencias/pagina/<int:id>/<int:page>')
def consultarPaginaAsistencias(id,page=1):
    try:
        a=Asistencias()
        e = Empleados()
        paginacion=a.consultarPagina(page,id)
        asistencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay asistencias registrados")
        asistencias=None
    return render_template('asistencias/consultaGeneral.html', asistencias=asistencias, paginas=paginas, pagina=page,empleados=e.consultaIndividual(id))

#Fin
#Bloque de percepciones


@app.route('/percepciones/pagina/<int:page>')
def consultarPaginaPercepciones(page=1):
    try:
        p=Percepciones()
        paginacion=p.consultarPagina(page)
        percepciones=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay percepciones registrados")
        percepciones=None
    return render_template('percepciones/consulta.html', percepciones=percepciones, paginas=paginas, pagina=page)


@app.route('/percepcionesNuevo')
def persepcionesNuevo():
    return render_template('Percepciones/nuevo.html')


@app.route('/percepcionesAgregar', methods=['post'])
def percepcionesAgregar():
    pe = Percepciones()
    pe.nombre = request.form['nombre']
    pe.descripcion = request.form['descripcion']
    pe.estatus = 'A'
    pe.insertar()
    flash('¡Percepcion registrada con éxito!')
    return render_template('Percepciones/nuevo.html')


@app.route('/percepciones/ver/<int:id>')
def percepcionesConsultar(id):
    pe = Percepciones()
    return render_template('Percepciones/modificar.html', percepciones=pe.consultaIndividual(id))


@app.route('/percepcionesActualizar', methods=['post'])
def percepcionesActualizar():
    pe = Percepciones()
    pe.idPercepcion = request.form['id']
    pe.nombre = request.form['nombre']
    pe.descripcion = request.form['descripcion']
    pe.estatus = request.form['estatus']
    pe.actualizar()
    flash('¡Percepcion actualizada con éxito!')
    return redirect(url_for('percepcionesConsultar', id=pe.idPercepcion))
#Fin

#Bloque deducciones


@app.route('/deducciones/pagina/<int:page>')
def consultarPaginadeducciones(page=1):
    try:
        de=Deducciones()
        paginacion=de.consultarPagina(page)
        deducciones=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay deducciones registradas")
        deducciones=None
    return render_template('deducciones/consulta.html', deducciones=deducciones, paginas=paginas, pagina=page)


@app.route('/deduccionesNuevo')
def deduccionesNuevo():
    return render_template('Deducciones/nuevo.html')


@app.route('/deduccionesAgregar', methods=['post'])
def deduccionesAgregar():
    de = Deducciones()
    de.nombre = request.form['nombre']
    de.descripcion = request.form['descripcion']
    de.porcentaje = request.form['porcentaje']
    de.estatus = 'A'
    de.insertar()
    flash('¡Deduccion registrada con éxito!')
    return render_template('Deducciones/nuevo.html')


@app.route('/deducciones/ver/<int:id>')
def deduccionesConsultar(id):
    de = Deducciones()
    return render_template('Deducciones/modificar.html', deducciones=de.consultaIndividual(id))


@app.route('/deduccionesActualizar', methods=['post'])
def deduccionesActualizar():
    de = Deducciones()
    de.idDeduccion = request.form['id']
    de.nombre = request.form['nombre']
    de.descripcion = request.form['descripcion']
    de.porcentaje = request.form['porcentaje']
    de.estatus = request.form['estatus']
    de.actualizar()
    flash('¡Deduccion actualizada con éxito!')
    return redirect(url_for('deduccionesConsultar' , id=de.idDeduccion))
#Fin

#Historial Puestos

@app.route('/historialPuestos/pagina/<int:id>/<int:page>')
def consultarPaginahistorialPuestos(id,page=1):
    try:
        hp=HistorialPuestos()
        e = Empleados()
        paginacion=hp.consultarPagina(page,id)
        historialPuestos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay historial de puestos registrado")
        historialPuestos=None
    return render_template('HistorialPuestos/consulta.html', historialPuestos=historialPuestos, paginas=paginas, pagina=page,empleados=e.consultaIndividual(id))



@app.route('/cuHistorialPuestos/pagina/<int:id>/<int:page>')
def consultarPaginacuHistorialPuestos(id,page=1):
    try:
        hp=HistorialPuestos()
        paginacion=hp.consultarPagina(page,id)
        historialPuestos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay historial de puestos registrado")
        historialPuestos=None
    return render_template('HistorialPuestos/cuconsulta.html', historialPuestos=historialPuestos, paginas=paginas, pagina=page)


#Fin


#AusenciasJustificadas
@app.route('/cuausencias/pagina/<int:id>/<int:page>')
def consultarPaginaCuAusencias(id,page=1):
    try:
        aj=AusenciasJustificadas()
        paginacion=aj.consultarPagina(page,id)
        ausencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay ausencias justificadas registradas")
        ausencias=None
    return render_template('AusenciasJustificadas/cuconsulta.html', ausencias=ausencias, paginas=paginas, pagina=page)


@app.route('/vacaciones/current/Nuevo')
def vacacionesNuevo():
    tipo= 'V'
    fecha1=date.today()
    fecha2=fecha1+timedelta(days=1)
    return render_template('AusenciasJustificadas/cunuevo.html', tipo=tipo,fecha1=fecha1,fecha2=fecha2)


@app.route('/permisos/current/nuevo')
def permisosNuevo():
    tipo='P'
    fecha1=date.today()
    fecha2=fecha1+timedelta(days=1)
    return render_template('AusenciasJustificadas/cunuevo.html', tipo=tipo,fecha1=fecha1,fecha2=fecha2)


@app.route('/incapacidad/current/nuevo')
def incapacidadNuevo():
    tipo='I'
    fecha1=date.today()
    fecha2=fecha1+timedelta(days=1)
    return render_template('AusenciasJustificadas/cunuevo.html', tipo=tipo,fecha1=fecha1,fecha2=fecha2)


@app.route('/ausencias/cuagregar', methods=['post'])
def agregarVacaciones():
    aj=AusenciasJustificadas()

    fecha1=request.form['fechaInicio']
    fecha2=request.form['fechaFin']

    aj.fechaSolicitud=date.today()
    aj.fechaInicio=fecha1
    aj.fechaFin=fecha2

    tipo=request.form['tipo']
    
    if tipo=='Vacaciones':
        aj.tipo='V'
    
    if tipo=='Permiso':
        aj.tipo='P'
    
    if tipo=='Incapacidad':
        aj.tipo='I'

    aj.idEmpleadoSolicita=request.form['idEmpleadoSolicita']
    aj.estatus='P'


    aj.dias=request.form['dias']
    aj.motivo=request.form['motivo']

    aj.insertar()
    flash('¡Solicitud ingresada con éxito!')
    return redirect(url_for('consultarPaginaCuAusencias',id=current_user.idEmpleado,page=1))


@app.route('/ausencias/cuConsulta/<int:id>')
def verAusenciasCurrent(id):
     aj=AusenciasJustificadas()
     return render_template('AusenciasJustificadas/cumodificar.html' , ausencias=aj.consultaIndividual(id))


@app.route('/ausencias/empleado/<int:id>')
def verEvidencia(id):
    aj=AusenciasJustificadas()
    return aj.consultaIndividual(id).evidencia

@app.route('/ausencias/cuactualizar' , methods=['post'])
def ausenciasCuactializar():
    aj=AusenciasJustificadas()
    aj.idAusencia=request.form['idAusencia']
    aj.fechaInicio=request.form['fechaInicio']
    aj.fechaFin=request.form['fechaFin']
    aj.dias=request.form['dias']
    aj.motivo=request.form['motivo']
    archivito = request.files['evidencia'].read()
    if archivito:
        aj.evidencia = archivito
    aj.actualizar()
    flash('¡Solicitud actualizada con éxito!')
    return redirect(url_for('verAusenciasCurrent', id= aj.idAusencia))


@app.route('/ausencias/eliminar/<int:id>')
def ausenciasEliminar(id):
    aj = AusenciasJustificadas()
    aj.eliminar(id)
    flash('¡Solicitud eliminada correctamente!')
    return redirect(url_for('consultarPaginaCuAusencias',id=current_user.idEmpleado,page=1))




@app.route('/solicitudesxdep/pagina/<int:id>/<int:page>/<string:st>')
def consultarPaginaSolicitudes(st,id,page=1):
    try:
        aj=AusenciasJustificadas()
        paginacion=aj.consultaPagina2(page,id,st)
        ausencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay solicitudes registradas")
        ausencias=None
    return render_template('AusenciasJustificadas/consulta.html', ausencias=ausencias, paginas=paginas, pagina=page)



@app.route('/solicitudesAdminRH/pagina/<int:page>/<string:st>')
def consultarPaginaSolicitudesAdminRH(st,page=1):
    try:
        aj=AusenciasJustificadas()
        paginacion=aj.consultaPagina3(page,st)
        ausencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay solicitudes registradas")
        ausencias=None
    return render_template('AusenciasJustificadas/consulta.html', ausencias=ausencias, paginas=paginas, pagina=page)


@app.route('/solicitudesAdmin/pagina/<int:page>/<string:st>')
def consultarPaginaSolicitudesAdmin(st,page=1):
    try:
        aj=AusenciasJustificadas()
        paginacion=aj.consultaPagina4(page,st)
        ausencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay solicitudes registradas")
        ausencias=None
    return render_template('AusenciasJustificadas/consulta.html', ausencias=ausencias, paginas=paginas, pagina=page)




@app.route('/ausencias/Consulta/<int:id>')
def verAusenciasGeneral(id):
     aj=AusenciasJustificadas()
     return render_template('AusenciasJustificadas/modificar.html' , ausencias=aj.consultaIndividual(id))


#Modificar jefes

@app.route('/ausencias/aprobarJefes', methods=['post'])
def ausenciasAprobarJefes():
    aj=AusenciasJustificadas()
    e=Empleados()

    aj.idAusencia=request.form['idAusencia']
    aj.observaciones=request.form['observaciones']
    aj.estatus=request.form['estatus']
    aj.idEmpleadoAutoriza=current_user.idEmpleado

    #Variables
    estatus=request.form['estatus']
    tipo=request.form['tipo']
    diasVacaciones= request.form['diasVacaciones']
    diasPermiso=request.form['diasPermiso']
    diasSolicitados= request.form['dias']
    estatusAnterior= request.form['estatusAnterior']

    aj.estatus=estatus
    if estatusAnterior!='A':
        if estatus=='A':
            if tipo=='Vacaciones':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasVacaciones= int(diasVacaciones) - int(diasSolicitados)
                e.actualizar()
            
        
            if tipo=='Permiso':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasPermiso= int(diasPermiso) - int(diasSolicitados)
                e.actualizar()
           
    if estatusAnterior!='C':
        if estatus=='C':
            if tipo=='Vacaciones':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasVacaciones= int(diasVacaciones) + int(diasSolicitados)
                e.actualizar()
           

            if tipo=='Permiso':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasPermiso=int(diasPermiso) + int(diasSolicitados)
                e.actualizar()
         

    aj.actualizar()
    flash('Solicitud actualizada con éxito')
    return redirect(url_for('verAusenciasGeneral', id=aj.idAusencia))
   
        

   
@app.route('/ausenciasXempleado/pagina/<int:id>/<int:page>')
def consultarPaginaAusenciasXempleado(id,page=1):
    try:
        aj=AusenciasJustificadas()
        e = Empleados()
        paginacion=aj.consultarPagina5(page,id)
        ausencias=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay ausencias justificadas registradas")
        ausencias=None
    return render_template('AusenciasJustificadas/consultaxEmpleado.html', ausencias=ausencias, paginas=paginas, pagina=page, empleados=e.consultaIndividual(id))
    

@app.route('/ausenciasxEmpleado/Consulta/<int:id>')
def verAusenciasxEmpleadoGeneral(id):
     aj=AusenciasJustificadas()
     return render_template('AusenciasJustificadas/modificarxEmpleado.html' , ausencias=aj.consultaIndividual(id))



@app.route('/ausencias/aprobarJefes2', methods=['post'])
def ausenciasAprobarJefes2():
    aj=AusenciasJustificadas()
    e=Empleados()

    aj.idAusencia=request.form['idAusencia']
    aj.observaciones=request.form['observaciones']
    aj.estatus=request.form['estatus']
    aj.idEmpleadoAutoriza=current_user.idEmpleado

    #Variables
    estatus=request.form['estatus']
    tipo=request.form['tipo']
    diasVacaciones= request.form['diasVacaciones']
    diasPermiso=request.form['diasPermiso']
    diasSolicitados= request.form['dias']
    estatusAnterior= request.form['estatusAnterior']

    aj.estatus=estatus
    if estatusAnterior!='A':
        if estatus=='A':
            if tipo=='Vacaciones':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasVacaciones= int(diasVacaciones) - int(diasSolicitados)
                e.actualizar()
            
        
            if tipo=='Permiso':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasPermiso= int(diasPermiso) - int(diasSolicitados)
                e.actualizar()
           
    if estatusAnterior!='C':
        if estatus=='C':
            if tipo=='Vacaciones':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasVacaciones= int(diasVacaciones) + int(diasSolicitados)
                e.actualizar()
           

            if tipo=='Permiso':
                e.idEmpleado=request.form['idEmpleadoSolicita']
                e.diasPermiso=int(diasPermiso) + int(diasSolicitados)
                e.actualizar()
         

    aj.actualizar()
    flash('Solicitud actualizada con éxito')
    return redirect(url_for('verAusenciasxEmpleadoGeneral', id=aj.idAusencia))


  #####Imprimir PDFs Ausencias


@app.route('/imprimirSolicitudVacaciones/<int:id>')
def solicitudVacaciones(id):
    aj=AusenciasJustificadas()
    asistencias2= aj.consultaGeneral()

    for aju in asistencias2:
        if(aju.idAusencia==id):
            fechaSolicitud=aju.fechaSolicitud
            fechaInicio=aju.fechaInicio
            fechaFin=aju.fechaFin        


    dto = fechaSolicitud
    dto2=fechaInicio
    dto3=fechaFin

    dia=dto.day
    diaI=dto2.day
    diaF=dto3.day

    mes=dto.month
    mesI=dto2.month
    mesF=dto3.month

    if(mes==1):
        cadena='Enero'

    if(mes==2):
        cadena='Febrero'
    if(mes==3):
        cadena='Marzo'
    if(mes==4):
        cadena='Abril'
    if(mes==5):
        cadena='Mayo'
    if(mes==6):
        cadena='Junio'
    if(mes==7):
        cadena='Julio'
    if(mes==8):
        cadena='Agosto'
    if(mes==9):
        cadena='Septiembre'
    if(mes==10):
        cadena='Octubre'
    if(mes==11):
        cadena='Noviembre'
    if(mes==12):
        cadena='Diciembre'
    
    ano=dto.year
    anoI=dto2.year
    anoF=dto3.year


    rendered=render_template('Formatos/solicitudVacaciones.html', ausencias=aj.consultaIndividual(id), dia=dia,diaI=diaI, diaF=diaF, mesI=mesI, 
        mesF=mesF, cadena=cadena, ano=ano, anoI=anoI, anoF=anoF)

 
    css=['static/css/estilosDocs.css']
   
    
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=solicitudVacaciones.pdf"
    return response



@app.route('/imprimirSolicitudPermisos/<int:id>')
def solicitudPermisos(id):
    aj=AusenciasJustificadas()
    asistencias2= aj.consultaGeneral()

    for aju in asistencias2:
        if(aju.idAusencia==id):
            fechaSolicitud=aju.fechaSolicitud
            fechaInicio=aju.fechaInicio
            fechaFin=aju.fechaFin        


    dto = fechaSolicitud
    dto2=fechaInicio
    dto3=fechaFin

    dia=dto.day
    diaI=dto2.day
    diaF=dto3.day

    mes=dto.month
    mesI=dto2.month
    mesF=dto3.month

    if(mes==1):
        cadena='Enero'

    if(mes==2):
        cadena='Febrero'
    if(mes==3):
        cadena='Marzo'
    if(mes==4):
        cadena='Abril'
    if(mes==5):
        cadena='Mayo'
    if(mes==6):
        cadena='Junio'
    if(mes==7):
        cadena='Julio'
    if(mes==8):
        cadena='Agosto'
    if(mes==9):
        cadena='Septiembre'
    if(mes==10):
        cadena='Octubre'
    if(mes==11):
        cadena='Noviembre'
    if(mes==12):
        cadena='Diciembre'
    
    ano=dto.year
    anoI=dto2.year
    anoF=dto3.year


    rendered=render_template('Formatos/solicitudPermisos.html', ausencias=aj.consultaIndividual(id), dia=dia,diaI=diaI, diaF=diaF, mesI=mesI, 
        mesF=mesF, cadena=cadena, ano=ano, anoI=anoI, anoF=anoF)

 
    css=['static/css/estilosDocs.css']
   
    
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=solicitudPermisos.pdf"
    return response

@app.route('/imprimirSolicitudIncapacidad/<int:id>')
def solicitudIncapacidad(id):
    aj=AusenciasJustificadas()
    asistencias2= aj.consultaGeneral()

    for aju in asistencias2:
        if(aju.idAusencia==id):
            fechaSolicitud=aju.fechaSolicitud
            fechaInicio=aju.fechaInicio
            fechaFin=aju.fechaFin        


    dto = fechaSolicitud
    dto2=fechaInicio
    dto3=fechaFin

    dia=dto.day
    diaI=dto2.day
    diaF=dto3.day

    mes=dto.month
    mesI=dto2.month
    mesF=dto3.month

    if(mes==1):
        cadena='Enero'

    if(mes==2):
        cadena='Febrero'
    if(mes==3):
        cadena='Marzo'
    if(mes==4):
        cadena='Abril'
    if(mes==5):
        cadena='Mayo'
    if(mes==6):
        cadena='Junio'
    if(mes==7):
        cadena='Julio'
    if(mes==8):
        cadena='Agosto'
    if(mes==9):
        cadena='Septiembre'
    if(mes==10):
        cadena='Octubre'
    if(mes==11):
        cadena='Noviembre'
    if(mes==12):
        cadena='Diciembre'
    
    ano=dto.year
    anoI=dto2.year
    anoF=dto3.year


    rendered=render_template('Formatos/solicitudIncapacidad.html', ausencias=aj.consultaIndividual(id), dia=dia,diaI=diaI, diaF=diaF, mesI=mesI, 
        mesF=mesF, cadena=cadena, ano=ano, anoI=anoI, anoF=anoF)

 
    css=['static/css/estilosDocs.css']
   
    
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=solicitudIncapacidad.pdf"
    return response

#Fin



#Métodos para la nómina

#Ver periodos#

@app.route('/periodosxnomina/pagina/<int:page>')
def consultarPaginaPeriodosxnomina(page=1):
    try:
        p=Periodos()
        paginacion=p.consultarPagina2(page)
        periodos=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash('No hay periodos registrados')
        periodos=None
    return render_template('Nomina/periodosxnomina.html', periodos=periodos, paginas=paginas, pagina=page)




##Ver empleados de la sucursal que se les generó la nomina en cierto periódo y están en proceso de "generación"
@app.route('/nominasEnGeneracion/pagina/<int:page>/<int:per>/<int:suc>')
def consultarNominasEnGeneracion(per,suc,page=1):
    try:
        p=Periodos()
        nom=Nominas()
        paginacion=nom.consultarPagina(page,per,suc)
        nominas=paginacion.items
        paginas=paginacion.pages
        estatus='G'
    except OperationalError:
        flash("No hay empleados registrados")
        nominas=None
    return render_template('Nomina/consultaNomina.html', nominas=nominas, paginas=paginas, pagina=page, estatus=estatus, periodos=p.consultaIndividual(per), )

##Ver empleados de la sucursal que se les generó la nomina en cierto periódo y están en proceso de "captura"
@app.route('/nominasEnCaptura/pagina/<int:page>/<int:per>/<int:suc>')
def consultarNominasEnCaptura(per,suc,page=1):
    try:
        p=Periodos()
        nom=Nominas()
        paginacion=nom.consultarPagina2(page,per,suc)
        nominas=paginacion.items
        paginas=paginacion.pages
        estatus='C'
    except OperationalError:
        flash("No hay empleados registrados")
        nominas=None
    return render_template('Nomina/consultaNomina.html', nominas=nominas, paginas=paginas, pagina=page, estatus=estatus,periodos=p.consultaIndividual(per))

##Ver empleados de la sucursal que se les generó la nomina en cierto periódo y están en proceso de "Revision"
@app.route('/nominasEnRevision/pagina/<int:page>/<int:per>/<int:suc>')
def consultarNominasEnRevision3(per,suc,page=1):
    try:
        p=Periodos()
        nom=Nominas()
        paginacion=nom.consultarPagina3(page,per,suc)
        nominas=paginacion.items
        paginas=paginacion.pages
        estatus='R'
    except OperationalError:
        flash("No hay empleados registrados")
        nominas=None
    return render_template('Nomina/consultaNomina.html', nominas=nominas, paginas=paginas, pagina=page, estatus=estatus ,periodos=p.consultaIndividual(per))

##Ver empleados de la sucursal que se les generó la nomina en cierto periódo y están "Autorizadas"
@app.route('/nominasAutorizadas/pagina/<int:page>/<int:per>/<int:suc>')
def consultarNominasAutorizadas(per,suc,page=1):
    try:
        p=Periodos()
        nom=Nominas()
        paginacion=nom.consultarPagina4(page,per,suc)
        nominas=paginacion.items
        paginas=paginacion.pages
        estatus='A'
    except OperationalError:
        flash("No hay empleados registrados")
        nominas=None
    return render_template('Nomina/consultaNomina.html', nominas=nominas, paginas=paginas, pagina=page, estatus=estatus,periodos=p.consultaIndividual(per))





#Activar la nómina del empleado en un determinado periódo
@app.route('/activarNominaXSucXPer/<int:suc>/<int:per>')
def activarNominaXSucXPer(per,suc):

    e=Empleados()
    empleados=e.consultaGeneral()
    p=Periodos()
    n=Nominas()
    fp=FormasDePago()
    fapa=fp.consultaGeneral()
    nominas=n.consultaGeneral()
    fechaHoy=date.today()

    return render_template('Nomina/nuevo.html', empleados=empleados ,periodos=p.consultaIndividual(per), nominas=nominas, fapa=fapa, fechaHoy=fechaHoy)

#####Ajax para verificar si existe la nomina de empleado en un periodo
@app.route('/consultarNominasExiste/<int:idEmpleado>/<int:idPeriodo>', methods=['get'])
def consultarExisteNominaPeriodo(idEmpleado,idPeriodo):
    n=Nominas()
    return json.dumps(n.consultarEmpleadoNomina(idEmpleado,idPeriodo))


@app.route('/nominasAlta', methods=['post'])
def altaDeNominas():
    n=Nominas()
    n.fechaElaboracion=request.form['fechaElaboracion']
    n.fechaPago=request.form['fechaPago']
    n.subtotal=0
    n.retenciones=0
    n.total=0
    n.diasTrabajados=0
    n.estatus='G'
    n.idEmpleado=request.form['idEmpleado']
    n.idFormaPago=request.form['idFormaPago']
    n.idPeriodo=request.form['idPeriodo']
    flash('Nómina generada de manera exitosa')
    n.insertar()
    return  redirect(url_for('activarNominaXSucXPer', per=n.idPeriodo, suc=current_user.idSucursal))


@app.route('/consultaNomina/ver/<int:id>/<int:empleado>/<string:fechaInicio>/<string:fechaFin>')
def verNomina(id,empleado,fechaInicio,fechaFin):
    n=Nominas()
    a=Asistencias()
    e=Empleados()
    np=NominasPercepciones()
    nd=NominasDeducciones()

    asistencias=a.consultaGeneral()
    empleados=e.consultaGeneral()
    conNomPer=np.consultaGeneral()
    conNomDec=nd.consultaGeneral()

    diasTrabajo=0
    date_object1 = datetime.strptime(fechaInicio, "%Y-%m-%d").date()
    date_object2 = datetime.strptime(fechaFin, "%Y-%m-%d").date()

    salario=0
    quincena=0

    sumaPer=0

    sumaDec=0

    for cnd in conNomDec:
        if(int(cnd.idNomina)==int(id)):
            print (cnd.importe)
            sumaDec=sumaDec+float(cnd.importe)
  
    for cnp in conNomPer:
        if(int(cnp.idNomina)==int(id)):
            print (cnp.importe)
            sumaPer=sumaPer+float(cnp.importe)


    for asis in asistencias:
        if(asis.idEmpleado==empleado):
            if(asis.fecha>=date_object1 and asis.fecha<=date_object2):
                diasTrabajo+=1
    
    for emp in empleados:
        if(emp.idEmpleado==empleado):
            print(emp.idEmpleado)
            salario=emp.salarioDiario

    quincena= salario*diasTrabajo


    print(diasTrabajo)
    print(quincena)
    totalPercepeciones=float(quincena)+float(sumaPer)
    sueldoNeto=totalPercepeciones-sumaDec

    return render_template('Nomina/modificar.html' ,nominas=n.consultaIndividual(id), diasTrabajo=diasTrabajo, quincena=quincena, sumaPer=sumaPer, 
        conNomPer=conNomPer,totalPercepeciones=totalPercepeciones,conNomDec=conNomDec,sumaDec=sumaDec, sueldoNeto=sueldoNeto)



@app.route('/capturaNomina', methods=['post'])
def capturaNomina():
    n=Nominas()

    n.idNomina=request.form['idNomina']
    idEmpleado=request.form['idEmpleado']
    fecha1=request.form['fechaInicio']
    fecha2=request.form['fechaFin']
    n.subtotal=request.form['subtotal']
    n.retenciones=float(request.form['retenciones'])
    n.total=request.form['total']
    n.diasTrabajados=request.form['diasTrabajados']
    n.estatus=request.form['estatus']

    n.actualizar()
    flash('Se registraron los cambios en la nómina de manera exitosa')
    return redirect(url_for('verNomina',id=n.idNomina,empleado=idEmpleado,fechaInicio=fecha1,fechaFin=fecha2))


@app.route('/cuNominasConsulta/pagina/<int:page>')
def cuNominasConsulta(page=1):
    try:
        n=Nominas()
        paginacion=n.consultarPagina5(page)
        nominas=paginacion.items
        paginas=paginacion.pages
    except OperationalError:
        flash("No hay Formas de pago registradas")
        nominas=None
    return render_template('Nomina/cuconsulta.html', nominas=nominas, paginas=paginas, pagina=page)

@app.route('/imprimirReciboNomina/<int:id>/<string:fechaInicio>/<string:fechaFin>')
def imprimirReciboNomina(fechaInicio,fechaFin,id):
    n=Nominas()
    np=NominasPercepciones()
    a=Asistencias()
    e=Empleados()
    empleados=e.consultaGeneral()
    asistencias=a.consultaGeneral()
    nd=NominasDeducciones()
    conNomPer=np.consultaGeneral()
    conNomDec=nd.consultaGeneral()
    diasTrabajo=0
    date_object1 = datetime.strptime(fechaInicio, "%Y-%m-%d").date()
    date_object2 = datetime.strptime(fechaFin, "%Y-%m-%d").date()

    quincena=0

    for asis in asistencias:
        if(asis.idEmpleado==current_user.idEmpleado):
            if(asis.fecha>=date_object1 and asis.fecha<=date_object2):
                diasTrabajo+=1

    for emp in empleados:
        if(emp.idEmpleado==current_user.idEmpleado):
            print(emp.idEmpleado)
            salario=emp.salarioDiario

    quincena= salario*diasTrabajo

    rendered=render_template('Formatos/reciboNomina.html', nominas=n.consultaIndividual(id), conNomDec=conNomDec,conNomPer=conNomPer, quincena=quincena)
    css=['static/css/estilosDocs.css']
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=reciboNomina.pdf"
    return response

@app.route('/imprimirReciboNomina2/<int:id>/<int:empleado>/<string:fechaInicio>/<string:fechaFin>')
def imprimirReciboNomina2(empleado,fechaInicio,fechaFin,id):
    n=Nominas()
    np=NominasPercepciones()
    a=Asistencias()
    e=Empleados()
    empleados=e.consultaGeneral()
    asistencias=a.consultaGeneral()
    nd=NominasDeducciones()
    conNomPer=np.consultaGeneral()
    conNomDec=nd.consultaGeneral()
    diasTrabajo=0
    date_object1 = datetime.strptime(fechaInicio, "%Y-%m-%d").date()
    date_object2 = datetime.strptime(fechaFin, "%Y-%m-%d").date()

    quincena=0

    for asis in asistencias:
        if(asis.idEmpleado==empleado):
            if(asis.fecha>=date_object1 and asis.fecha<=date_object2):
                diasTrabajo+=1

    for emp in empleados:
        if(emp.idEmpleado==empleado):
            print(emp.idEmpleado)
            salario=emp.salarioDiario

    quincena= salario*diasTrabajo

    rendered=render_template('Formatos/reciboNomina.html', nominas=n.consultaIndividual(id), conNomDec=conNomDec,conNomPer=conNomPer, quincena=quincena)
    css=['static/css/estilosDocs.css']
    pdf = pdfkit.from_string(rendered, False, css=css)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "attachment; filename=reciboNomina.pdf"
    return response

#Percepciones
@app.route('/percepciones/nuevo/pagina/<int:page>/<int:idnom>')
def percepcionesnuevo(idnom,page=1):

    try:
        n=Nominas()
        p=Percepciones()
        np=NominasPercepciones()

        conNomPer=np.consultaGeneral()

        percepciones=p.consultaGeneral()
        paginacion=np.consultarPagina(page,idnom)
        nomperp=paginacion.items
        paginas=paginacion.pages

        sumaPer=0
        for cnp in conNomPer:
            if(int(cnp.idNomina)==int(idnom)):
                print (cnp.importe)
                sumaPer=sumaPer+float(cnp.importe)

    except OperationalError:
        flash("No hay empleados registrados")
        nomperp=None
    return render_template('NominaPercepciones/consulta.html',percepciones=percepciones,nomperp=nomperp, paginas=paginas, pagina=page, sumaPer=sumaPer,
        nominas=n.consultaIndividual(idnom))


@app.route('/nomPercepciones/agregar', methods=['post'])
def nomPercepcionesAgregar():
    np=NominasPercepciones()
    p=Percepciones()
    percepciones=p.consultaGeneral()

    np.idNomina=request.form['idNomina']
    np.idPercepcion=request.form['idPercepcion']
    diasPagados=request.form['diasPagados']
    salarioDiario=request.form['salarioDiario']
    
    importe=float(diasPagados)*float(salarioDiario)

    np.diasPagados=diasPagados
    np.importe=importe

    np.insertar()
    flash('Percepcion ingresada con éxito')
    return redirect(url_for('percepcionesnuevo',page=1, idnom=np.idNomina))



@app.route('/eliminar/noPercepciones/<int:id>/<int:nomina>')
def eliminarNoPercepciones(id,nomina):
    np=NominasPercepciones()
    np.eliminar(id)
    flash('Percepción eliminada con éxito')
    return redirect(url_for('percepcionesnuevo', page=1, idnom=nomina))



##NominasDeducciones

@app.route('/deducciones/nuevo/pagina/<int:page>/<int:idnom>/<string:subtotal>')
def deduccionesnuevo(idnom,subtotal,page=1):
    try:
        n=Nominas()
        d=Deducciones()
        nd=NominasDeducciones()

        conNomDec=nd.consultaGeneral()

        deducciones=d.consultaGeneral()
        paginacion=nd.consultarPagina(page,idnom)
        nomdec=paginacion.items
        paginas=paginacion.pages

        sumaDec=0
        for cnd in conNomDec:
            if(int(cnd.idNomina)==int(idnom)):
                print (cnd.importe)
                sumaDec=sumaDec+float(cnd.importe)
        



    except OperationalError:
        flash("No hay empleados registrados")
        nomdec=None
    return render_template('NominaDeducciones/consulta.html',deducciones=deducciones, nomdec=nomdec, paginas=paginas, pagina=page, sumaDec=sumaDec,
        nominas=n.consultaIndividual(idnom), subtotal=subtotal)


@app.route('/nomDeducciones/agregar', methods=['post'])
def nomDeduccionesAgregar():
    nd=NominasDeducciones()
    d=Deducciones()
    dedu=d.consultaGeneral()


    salarioNeto=request.form['salarioNeto']
    idDeduccion=request.form['idDeduccion']
    porcentaje=0
    importe=0
    for de in dedu:
        if(int(de.idDeduccion)==int(idDeduccion)):
            porcentaje=de.porcentaje

    print(porcentaje)
    importe=(float(porcentaje)/100)*float(salarioNeto)
    print(importe)

    nd.idNomina=request.form['idNomina']
    nd.idDeduccion=idDeduccion
    nd.importe=importe

    nd.insertar()
    
    flash('Deducción ingresada con éxito')
    return redirect(url_for('deduccionesnuevo',page=1, idnom=nd.idNomina,subtotal=salarioNeto))


@app.route('/eliminar/noDeducciones/<int:id>/<int:nomina>/<string:subtotal>')
def eliminarNoDeducciones(id,nomina,subtotal):
    nd=NominasDeducciones()
    nd.eliminar(id)
    flash('Deducción eliminada con éxito')
    return redirect(url_for('deduccionesnuevo', page=1, idnom=nomina, subtotal=subtotal))


#Retornar ciudades en select dinámico
@app.route('/retornar/ciudades/<int:id>')
def retornarciudades(id):
    c=Ciudades()
    ciudades=c.consultaEstado(id)
    return ciudades



if __name__ == '__main__':
    db.init_app(app)
    app.run(port=8000, debug=True)
