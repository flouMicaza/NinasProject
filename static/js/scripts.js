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

 //evento para cuando se aprieta un botón de editar curso.
function editar_clase(id_clase) {
    $("#clase_"+ id_clase).css("display","none")
    $("#clase_edit_" + id_clase).css({
        "display": "flex",
        "justify-content":"space-between"
    })
}