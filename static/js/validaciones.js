//---------------------------------VALIDADCIONES TABLA TURNOS-------------------------------------------------//
function validarTurnos(form) {
    var inicio = form.horaInicio.value;
    var fin = form.horaFin.value;
    var mensaje = validarHoras(inicio, fin);
    var div = document.getElementById("notificaciones");
    var ban = false;

    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;

    }
    return ban;
}

function validarHoras(inicio, fin) {
    var salida = "";
    if (fin <= inicio || inicio >= fin) {
        salida = "<p>Ingresa un rango de horas valido.</p> <br>"
    }
    return salida;
}

//------------------------------VALIDACIONES TABLA EMPLEADOS-------------------------------------//
function consultarEmail(){
    var ajax= new XMLHttpRequest();
    var email=document.getElementById("email").value;
    var url="/empleados/email/" + email;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones1");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();
}


function consultarNss(){
    var ajax= new XMLHttpRequest();
    var nss=document.getElementById("nss").value;
    var url="/empleados/nss/" + nss;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones2");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();
}

function consultarTelefono(){
    var ajax= new XMLHttpRequest();
    var telefono=document.getElementById("telefono").value;
    var url="/empleados/telefono/" + telefono;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones3");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();


}


function consultarCurp(){
    var ajax= new XMLHttpRequest();
    var curp=document.getElementById("curp").value;
    var url="/empleados/curp/" + curp;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones4");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();


}


function consultarPuestos(){
    var ajax= new XMLHttpRequest();
    var puesto=document.getElementById("idPuesto").value;
    var salarioDiario=document.getElementById("salarioDiario").value;
    var url="/empleados/consultaPuestos/"+puesto+"/"+salarioDiario;  
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones5");
    ajax.onreadystatechange=function(){ 
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");

            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
                
            }
        }
    };
    ajax.send();
}


function validarEmpleados(form){
    var fechaNacimiento=form.fechaNacimiento.value;
    var fechaContratacion=form.fechaContratacion.value;
    var fechaFin=form.fechaFin.value;
    var mensaje = validarEdad(fechaNacimiento);
    mensaje += validarContrato(fechaContratacion,fechaFin);
    var div = document.getElementById("notificaciones5");
    var ban = false;
    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;
    }
    return ban;
}

function calcularEdad(cadena){
    var hoy = new Date();
    var cumpleanos = new Date(cadena);
    var edad = hoy.getFullYear() - cumpleanos.getFullYear();
    var m = hoy.getMonth() - cumpleanos.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < cumpleanos.getDate())) {
        edad--;
    }
    return edad;
}

function validarEdad(cadena){
    var salida="";
    if(calcularEdad(cadena)<18){
        salida = "<p>La persona que deseas contratar debe de ser mayor de edad.</p> <br>"
    }
    return salida;
}



function validarContrato(fechaContratacion,fechaFin){
    var salida = "";
    if (fechaFin <= fechaContratacion || fechaInicio >= fechaContratacion) {
        salida = "<p>Ingresa un rango de fechas válido.</p> <br>";
    }
    return salida;

}


function verPassword(){
    var check=document.getElementById("ver");
    if(check.checked){
        document.getElementById("password").setAttribute("type","text");
    }
    else{
        document.getElementById("password").setAttribute("type","password");
    }
}


//-------------------VALIDACIONES TABLA SUCURSALES----------------------//

function consultarTelefonoSuc(){
    var ajax= new XMLHttpRequest();
    var telefono=document.getElementById("telefonoSuc").value;
    var url="/sucursales/telefono/" + telefono;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();


}





//--------------------VALIDACIONES TABLA PERIODOSOS----------------------//


function validarPeriodos(form){
    var fechaInicio = form.fechaIncio.value;
    var fechaFin = form.fechaFin.value;
    var mensaje = validarFechas(fechaInicio,fechaFin);
    var div = document.getElementById("notificaciones");
    var ban = false;

    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;

    }
    return ban;
}
function validarFechas(fechaInicio,fechaFin) {
    var salida = "";
    if (fechaFin <= fechaInicio || fechaInicio >= fechaFin){
        salida = "<p>Ingresa un rango de fechas valido.</p> <br>"
    }
    return salida;
}


//--------------------VALIDACIONES TABLA PUESTOS-----------------------------//

function validarPuestos(form){
    var salarioMinimo = form.salarioMinimo.value;
    var salarioMaximo = form.salarioMaximo.value;
    var mensaje = validarSalarios(salarioMinimo,salarioMaximo);
    var div = document.getElementById("notificaciones");
    var ban = false;

    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;

    }
    return ban;
}
function validarSalarios(salarioMinimo,salarioMaximo) {
    var salida = "";
    if (salarioMaximo <= salarioMinimo || salarioMinimo >= salarioMaximo) {
        salida = "<p>Ingresa un rango de salarios válido.</p> <br>"
    }
    return salida;
}


//-----------------------VALIDACIONES TABLA ASISTENCIAS-----------------------//

function validarAsistencias(form){
    var cadena= " "+form.dias.value;
    var fecha = new Date().toISOString();
    var mensaje= validarDiasLaborados(cadena,fecha);
    var div = document.getElementById("notificaciones");
    var ban = false;

    if (mensaje != "") {
        div.innerHTML = mensaje;
        ban = false;
    }
    else {
        div.innerHTML = "";
        ban = true;

    }
    return ban;
}

function validarDiasLaborados(cadena, fecha) {
    var salida = "";
    var fechaComoCadena = fecha; // día lunes
    var dias = [
      "Domingo",
      "Lunes",
      "Martes",
      "Miércoles",
      "Jueves",
      "Viernes",
      "Sábado",
    ];
    var numeroDia = new Date(fechaComoCadena).getDay();
    var nombreDia = dias[numeroDia];
  
    var index = cadena.indexOf(nombreDia);
  
    if (index < 0) {
      salida = "El día " + nombreDia+ " no laboras";
    }
    return salida;
  }
  

/*---------------------VALIDACIONES TABLA AUSENCIAS JUSTIFICADAS----------------------*/ 

  function validarAusenciasJustifcadas(form) {
      var fechaInicio=form.fechaInicio.value;
      var fechaFin=form.fechaFin.value;
      var diasPermiso=form.diasPermiso.value;
      var diasVacaciones=form.diasVacaciones.value;
      var tipo=form.tipo.value;
      var mensaje= validarFechas(fechaInicio, fechaFin);
      mensaje+=diasDisponibles(fechaInicio,fechaFin,diasPermiso,diasVacaciones,tipo);
      var div= document.getElementById("notificaciones");
      var ban= false;
      if(mensaje!=""){
          div.innerHTML=mensaje;
          ban =false;

      }
      else{
          div.innerHTML="";
          ban=true;
      }
      return ban;
  }


  function diasDisponibles(fechaInicio,fechaFin,diasPermiso,diasVacaciones,tipo){
        var salida = "";
        var dia1= new Date(fechaInicio);
        var dia2 = new Date(fechaFin);

        var diferencia= Math.abs(dia2-dia1);
        dias = diferencia/(1000 * 3600 * 24)
        console.log(dias+ "    " + tipo)

        if (tipo=="Permiso"){
            if(dias > diasPermiso){
                salida = "Tus días disponibles para permisos son " + diasPermiso +". Verifica las fechas que estas solicitando";
            }
                return salida;
        }

        if (tipo=="Vacaciones"){
            if(dias > diasVacaciones){
                salida = "Tus días disponibles para vacaciones son " + diasPermiso+". Verifica las fechas que estas solicitando";
            }
                return salida;
        }

        if(tipo=="Incapacidad"){
            if(dias<0){
                salida= "Verifica las fechas"
            }
            return salida;
        }

  }
  

//Calcular días dinamicamente

function calcularDias(){
    var x = document.getElementById("myDate1").value;
    var y=document.getElementById("myDate2").value;

    var fecha1= new Date(x);
    var fecha2= new Date(y);

    var dif=Math.abs(fecha2-fecha1);
    resultado=dif/(1000 * 3600 * 24)

    if(fecha2<fecha1){
        document.getElementById("demo").value =  0;
    }else{
        document.getElementById("demo").value =  resultado;
    }
   
 
}



/*----------------------------Validaciones tabla Nóminas----------------------------*/

/*Validar si la nómina de un wey existe en un determinado periodo de pago*/


function consultarNominaActiva(){
    var ajax= new XMLHttpRequest();
    var idEmpleado=document.getElementById("empleado").value;
    var idPeriodo=document.getElementById("periodo").value
    var url="/consultarNominasExiste/" + idEmpleado+"/"+idPeriodo;
    ajax.open("get", url,true);
    var div = document.getElementById("notificaciones4");
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            var respuesta=JSON.parse(this.responseText);
            if(respuesta.estatus=='Error'){
                div.innerHTML=respuesta.mensaje;
                document.getElementById("registrar").setAttribute("disabled","true");
            }else{
                div.innerHTML="";
                document.getElementById("registrar").removeAttribute("disabled");
            }
        }
    };
    ajax.send();


}







