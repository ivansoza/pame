<script>
  $("#tabla").DataTable({
      paging: true,
      lengthMenu: [5, 10, 25, 50, 100], // Cambiamos el menú de longitud para incluir 5 entradas
      pageLength:5,
      lengthChange :true,
      autoWidth: true,
      searching: true,
      bInfo: true,
      bSort: true,

      dom: 'Bfrltip',
      buttons:[
          {extend: 'copy',
          text: '<i class="fas fa-clone"></i>',
          class: 'btn btn-secondary',
          titleAttr: 'Copy',
          exportOptions:{
              columns:[0,1,2]
          }
          },
          {extend: 'excel',
          text: '<i class="fas fa-file-excel"></i>',
          class: 'btn btn-secondary',
          titleAttr: 'Excel',
          exportOptions:{
              columns:[0,1,2]
          }
          },
          {extend: 'print',
          text: '<i class="fas fa-print"></i>',
          class: 'btn btn-secondary',
          titleAttr: 'Excel',
          exportOptions:{
              columns:[0,1,2]
          }
          },
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
</script>