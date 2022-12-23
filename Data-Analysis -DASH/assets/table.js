$(document).ready(function() { //Inicio
    var myTable = $('#myTable').DataTable();
  
    $('#myTable Tbody').on( 'click', 'Tr', function () {
       $(this).toggleClass('selected');
    });
    $('#btnValoresSeleccionados').click(function() {
        $('#myTable Tbody Tr').each(function(indexFila){
          if($(this).hasClass('selected')) { 
							alert("La fila: "+indexFila+" se ha seleccionado");
						}
          $(this).children('Td').each(function(indexColumna){
            if(indexColumna==3){
              campo1=$(this).text()
              alert(campo1+" :children");
            };
          });
          
        });//fin de '#myTable tbody tr'
      
    });//Obtiene datos de una fila
    $.each(myFila,function(index, contenido){ 
       if(index==2){
          alert(contenido);
       };
    }); 
  
} );