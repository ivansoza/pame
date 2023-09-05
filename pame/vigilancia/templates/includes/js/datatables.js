<script>
    $(document).ready(function() {
      new DataTable('#tabla', {
        dom: '<"top"fl>rt<"bottom"Bip><"clear">',
        lengthMenu: [5, 10, 25, 50, 100], // Cambiamos el menú de longitud para incluir 5 entradas
        pageLength: 5, // Establecemos el número inicial de entradas por página en 5
        buttons: [
          {
            extend: 'copy',
            text: '<i class="fas fa-copy"></i> Copiar', // Icono de copiar
          },
          {
            extend: 'excel',
            text: '<i class="fas fa-file-excel"></i> Exportar a Excel', // Icono de exportar a Excel
          },
          {
            extend: 'print',
            text: '<i class="fas fa-print"></i> Imprimir', // Icono de imprimir
          },
          'colvis',
        ],
        "language": {
                  "sProcessing": "Procesando...",
                  "sLengthMenu": "Mostrar _MENU_ Registros",
                  "sZeroRecords": "No se encontraron resultados",
                  "sEmptyTable": "Ningún dato disponible en esta tabla",
                  "sInfo": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                  "sInfoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                  "sInfoFiltered": "(filtrado de un total de _MAX_ Registros)",
                  "sSearch": "Buscar:",
                  "sInfoThousands": ",",
                  "sLoadingRecords": "Cargando...",
                  "oPaginate": {
                      "sFirst": "Primero",
                      "sLast": "Último",
                      "sNext": "Siguiente",
                      "sPrevious": "Anterior"
                  },
                  "oAria": {
                      "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                      "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                  },
                  "buttons": {
                      "copy": "Copiar",
                      "colvis": "Visibilidad"
                  }
              },
        
      });
    });
</script>
  