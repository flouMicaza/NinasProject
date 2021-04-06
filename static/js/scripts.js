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

document.addEventListener('DOMContentLoaded', function() {
    var elem = document.querySelector('.collapsible.expandable');
    var instance = M.Collapsible.init(elem, {
      accordion: false
    });
});


//modal asistencia de un curso (para una alumna)
$(document).ready(function(){
    $('.datepicker').datepicker({'format': 'yyyy-mm-dd'});
    $('select').not('.disabled').formSelect();
    $('.modal').modal();
    $('ul.tabs').tabs();
    $('#tabla_estadísticas').DataTable({
        scrollX: true,
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
    })
    $('#tabla_asist_gral').DataTable({
        scrollX: true,
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

});

$( function()
{
    var targets = $( '[rel~=tooltip]' ),
        target  = false,
        tooltip = false,
        title   = false;

    targets.bind( 'mouseenter', function()
    {
        target  = $( this );
        tip     = target.attr( 'title' );
        tooltip = $( '<div id="tooltip"></div>' );

        if( !tip || tip == '' )
            return false;

        target.removeAttr( 'title' );
        tooltip.css( 'opacity', 0 )
               .html( tip )
               .appendTo( 'body' );

        var init_tooltip = function()
        {
            if( $( window ).width() < tooltip.outerWidth() * 1.5 )
                tooltip.css( 'max-width', $( window ).width() / 2 );
            else
                tooltip.css( 'max-width', 340 );

            var pos_left = target.offset().left + ( target.outerWidth() / 2 ) - ( tooltip.outerWidth() / 2 ),
                pos_top  = target.offset().top - tooltip.outerHeight() - 20;

            if( pos_left < 0 )
            {
                pos_left = target.offset().left + target.outerWidth() / 2 - 20;
                tooltip.addClass( 'left' );
            }
            else
                tooltip.removeClass( 'left' );

            if( pos_left + tooltip.outerWidth() > $( window ).width() )
            {
                pos_left = target.offset().left - tooltip.outerWidth() + target.outerWidth() / 2 + 20;
                tooltip.addClass( 'right' );
            }
            else
                tooltip.removeClass( 'right' );

            if( pos_top < 0 )
            {
                var pos_top  = target.offset().top + target.outerHeight();
                tooltip.addClass( 'top' );
            }
            else
                tooltip.removeClass( 'top' );

            tooltip.css( { left: pos_left, top: pos_top } )
                   .animate( { top: '+=10', opacity: 1 }, 50 );
        };

        init_tooltip();
        $( window ).resize( init_tooltip );

        var remove_tooltip = function()
        {
            tooltip.animate( { top: '-=10', opacity: 0 }, 50, function()
            {
                $( this ).remove();
            });

            target.attr( 'title', tip );
        };

        target.bind( 'mouseleave', remove_tooltip );
        tooltip.bind( 'click', remove_tooltip );
    });
});



 //evento para cuando se aprieta un botón de editar curso.
function editar_clase(id_clase) {
    $("#clase_"+ id_clase).css("display","none")
    $("#clase_edit_" + id_clase).css({
        "display": "flex",
        "justify-content":"space-between"
    })
}

//limpiar cache_lock
function clear_cache(scheme, host, url){
    fetch(scheme.concat('://',host,url))
    return true
}

//evento para cerrar edición de curso sin guardar
function cerrar_edicion_clase(id_clase) {
    $("#clase_" + id_clase).css({
        "display": "flex",
        "justify-content":"space-between"
    })
    $("#clase_edit_"+ id_clase).css("display","none")
}


//ordenar clases ascendentemente o descendentemente
function cambiar_orden() {
    let current_url, lista_clases, items_clase, end, i, text, new_order, aux, new_url;

    current_url = window.location.href;

    text = document.getElementById("sort-button").firstChild;
    text.data = current_url.includes("newest") ? "Más antiguas primero" : "Más recientes primero";

    lista_clases = document.getElementById("lista-clases");
    items_clase = lista_clases.getElementsByClassName("items-clase");
    end = items_clase.length - 1;
    for (i = 0; i < end; i++) {
        items_clase[i].parentNode.insertBefore(items_clase[end], items_clase[i]);
    }

    new_order = current_url.includes("newest") ? "oldest" : "newest";
    const r = /(\d+\/curso\/)(\D*)/;
    aux = current_url.replace(r, '$1');
    new_url = aux + new_order + '/';
    window.history.replaceState({}, '', new_url);
}


//permite habilitar/deshabilitar botón para subir soluciones si hay o no un archivo seleccionado
$(document).ready
    (function () {
        //when input's value changes
        $("#file").change(function () {
            if($(this).val()) {
                $("#submit-sol").prop("disabled", false);
            }
            else {
                $("#submit-sol").prop("disabled", true);
            }
        });
    });

// tabla alumnas coordinacion

$(document).ready(function() {
    $('#alumnas_table').DataTable(
        {    "bLengthChange": false,
        oLanguage: {
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

        },
    }
    );
} );

// tabla profesoras coordinacion

$(document).ready(function() {
    $('#profesoras_table').DataTable(
        {"bLengthChange": false,
        oLanguage: {
            sSearch: "Buscar:",
            sInfo: "Mostrando profesoras del _START_ al _END_ de un total de _TOTAL_ profesoras",
            sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            sInfoFiltered: "(filtrado de un total de _MAX_ profesoras)",
            oPaginate: {
                    sFirst:    "Primero",
                    sLast:     "Último",
                    sNext:     "Siguiente",
                    sPrevious: "Anterior"
                },
            sZeroRecords: "No se encontraron resultados",

        },}
    );
} );

// tabla voluntarias coordinacion

$(document).ready(function() {
    $('#voluntarias_table').DataTable( {
        "bLengthChange": false,
        oLanguage: {
            sSearch: "Buscar:",
            sInfo: "Mostrando voluntarias del _START_ al _END_ de un total de _TOTAL_ voluntarias",
            sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            sInfoFiltered: "(filtrado de un total de _MAX_ voluntarias)",
            oPaginate: {
                    sFirst:    "Primero",
                    sLast:     "Último",
                    sNext:     "Siguiente",
                    sPrevious: "Anterior"
                },
            sZeroRecords: "No se encontraron resultados",

        },
    });
} );

$(document).ready(function() {
    $('#cursos_table').DataTable(
        {    "bLengthChange": false,
        oLanguage: {
            sSearch: "Buscar:",
            sInfo: "Mostrando cursos del _START_ al _END_ de un total de _TOTAL_ cursos",
            sInfoEmpty: "Mostrando registros del 0 al 0 de un total de 0 registros",
            sInfoFiltered: "(filtrado de un total de _MAX_ cursos)",
            oPaginate: {
                    sFirst:    "Primero",
                    sLast:     "Último",
                    sNext:     "Siguiente",
                    sPrevious: "Anterior"
                },
            sZeroRecords: "No se encontraron resultados",

        },
    }
    );
} );

var click_counter = 0;
var user_dict = new Map();

function clicked(checked, id) {
    console.log(id);
    if(checked){
        click_counter+=1
        user_dict.set(id, id);
        $("#btn-1").prop("disabled", false);
        $("#btn-2").prop("disabled", false);
    }
    else{
        click_counter-=1
        user_dict.delete(id);
        if (click_counter === 0){
            $("#btn-1").prop("disabled", true);
            $("#btn-2").prop("disabled", true);
        }
    }
}

function eliminar_alerta(message){
    function logMapElements(value, key, map) {
        message = message.concat('\n', value);
    }
    user_dict.forEach(logMapElements);
    return confirm(message);

}
