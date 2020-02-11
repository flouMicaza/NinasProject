//menú aparece por el lado cuando se achica.
document.addEventListener('DOMContentLoaded', function() {
            var elems = document.querySelectorAll('.sidenav');
            var instances = M.Sidenav.init(elems);
        });

//acordiones
 document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.collapsible');
    var instances = M.Collapsible.init(elems);

  });

//modal asistencia de un curso (para una alumna)

$(document).ready(function(){

  $('.modal').modal();
  
$('#tabla_asist_gral').DataTable({
    order:[[0, "asc"]],
    dom: "Blfrtip",
    oLanguage: {
        sLengthMenu: '<span>Alumnas por página:</span><select class="browser-default">' +
            '<option value="10">10</option>' +
            '<option value="20">20</option>' +
            '<option value="30">30</option>' +
            '<option value="40">40</option>' +
            '<option value="50">50</option>' +
            '<option value="-1">Todas</option>' +
            '</select></div>',
        sSearch: "Buscar:",
        sInfo: "Mostrando alumnas del _START_ al _END_ de un total de _TOTAL_ alumnas",
        sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
        sInfoFiltered: "(filtrado de un total de _MAX_ alumnas)",
        oPaginate: {
                sFirst:    "Primero",
                sLast:     "Último",
                sNext:     "Siguiente",
                sPrevious: "Anterior"
            },
        sZeroRecords: "No se encontraron resultados",
    }
    
});
$('select').material_select();
});