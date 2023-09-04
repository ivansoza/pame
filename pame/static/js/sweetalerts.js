
$(function() {
    var Toast = Swal.mixin({
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 3000
    });

    // Función para mostrar notificaciones de éxito
    function showSuccessNotification(message) {
      Toast.fire({
        icon: 'success',
        title: message
      });
    }

    // Función para mostrar notificaciones de error
    function showErrorNotification(message) {
      Swal.fire({
        icon: 'error',
        title: 'Oops...',
        text: message,
        footer: '<a href="">Why do I have this issue?</a>'
      });
    }   
  });
