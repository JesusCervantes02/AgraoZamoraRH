$(document).ready(function(){
    $('#est').change(function(){
        let value = $(this).val();
       $.ajax({
            type: 'GET',
            url: '/retornar/ciudades/'+value,
            dataType:'json',
            success:function(data){
                $("#ciudades option").each(function() {
                     $(this).remove();
                });
                    console.log(data);
                for(var i = 0; data.length;i++){
                     $("#ciudades").append("<option value="+data[i].id+">"+data[i].nombre+"</option>");
                }


            }
       });
    });
});


