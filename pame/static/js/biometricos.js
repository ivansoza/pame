
  // Variables globales para la cámara y el estado de captura
  var videoElement;
  var canvasElement;
  var firmaCanvasElement;
  var firmaPad;

  // Función para abrir la ventana modal debajo del botón
  function abrirModal(modalId) {
    var modal = document.getElementById(modalId);
    var boton = document.getElementById(modalId.replace("myModal", "abrirModal"));
    
    var rect = boton.getBoundingClientRect();
    var topOffset = rect.bottom + 10;
    var leftOffset = rect.left;

    modal.style.top = topOffset + "px";
    modal.style.left = leftOffset + "px";
    modal.style.display = "flex"; /* Cambiar display a flex para usar alineación vertical */

    if (modalId === "myModal1") {
      iniciarCamara();
    } else if (modalId === "myModal3") {
      iniciarFirma();
    }
  }

  // Función para iniciar la cámara
  function iniciarCamara() {
    videoElement = document.getElementById('video');
    canvasElement = document.getElementById('canvas');

    navigator.mediaDevices.getUserMedia({ video: true })
      .then(function(stream) {
        videoElement.srcObject = stream;
        videoElement.play();
      })
      .catch(function(error) {
        console.error('Error al acceder a la cámara:', error);
      });
  }

  // Función para capturar la foto desde la cámara
  function capturarFoto() {
    var context = canvasElement.getContext('2d');
      
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;
    context.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

    document.getElementById('capturedImage').src = canvasElement.toDataURL('image/png');
    document.getElementById('capturedImage').style.display = 'block';
    document.getElementById('video').style.display = 'none';
    document.getElementById('capturedImageData').value = canvasElement.toDataURL('image/png');

    document.getElementById('capturarBtn').disabled = true;
    document.getElementById('volverBtn').style.display = 'block';
  }

  // Función para volver a tomar foto
  function volverATomar() {
    document.getElementById('capturedImage').style.display = 'none';
    document.getElementById('video').style.display = 'block';
    document.getElementById('capturarBtn').disabled = false;
    document.getElementById('volverBtn').style.display = 'none';
  }

  // Función para capturar la huella dactilar
  function capturarHuella() {
    // Aquí puedes agregar tu lógica para capturar la huella dactilar
    // Puedes mostrar un mensaje, hacer una petición al servidor, etc.
    alert('Capturando huella dactilar...');
  }

  // Función para iniciar el pad de firma
  function iniciarFirma() {
    firmaCanvasElement = document.getElementById('firmaCanvas');
    firmaPad = new SignaturePad(firmaCanvasElement);
  }

  // Función para capturar la firma
  function capturarFirma() {
    // Aquí puedes guardar la imagen de la firma o realizar otras acciones con la firma capturada
    alert('Firma capturada correctamente.');

    document.getElementById('capturarFirmaBtn').disabled = true;
    document.getElementById('volverAFirmarBtn').style.display = 'block';
  }

  // Función para volver a firmar
  function volverAFirmar() {
    firmaPad.clear();

    document.getElementById('capturarFirmaBtn').disabled = false;
    document.getElementById('volverAFirmarBtn').style.display = 'none';
  }

  // Función para cerrar la ventana modal
  function cerrarModal(modalId) {
    var modal = document.getElementById(modalId);
    modal.style.display = "none";

    // Detener la cámara al cerrar la ventana modal
    if (videoElement) {
      videoElement.srcObject.getTracks().forEach(track => track.stop());
    }
  }

  
  // Función para guardar la foto
  function guardarFoto() {
    var imageData = canvasElement.toDataURL('image/png');
    // Aquí puedes enviar imageData al servidor o guardarla localmente
    console.log('Guardando foto:', imageData);
  }

  // Función para guardar la huella
  function guardarHuella() {
    // Aquí puedes agregar tu lógica para guardar la huella dactilar
    alert('Huella guardada correctamente.');
  }

  // Función para guardar la firma
  function guardarFirma() {
    var firmaImageData = firmaPad.toDataURL();
    // Aquí puedes enviar firmaImageData al servidor o guardarla localmente
    console.log('Guardando firma:', firmaImageData);
  }
  