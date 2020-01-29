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

  })





