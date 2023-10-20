const contenedorQR = document.getElementById('contenedorQR');
const formulario = document.getElementById('formulario');

// Crear un objeto para llevar un registro de los códigos QR utilizados
const codigosQRUtilizados = {};

const QR = new QRCode(contenedorQR);

formulario.addEventListener('submit', (e) => {
  e.preventDefault();

  const link = formulario.link.value.trim(); // Eliminar espacios en blanco al principio y al final

  // Verificar si el enlace está en un formato válido (puedes personalizar esta validación)
  if (!esEnlaceValido(link)) {
    alert("El enlace no es válido. Por favor, ingresa un enlace válido.");
    return;
  }

  // Verificar si el código ya ha sido utilizado
  if (codigosQRUtilizados[link]) {
    alert("Este código QR ya ha sido utilizado.");
  } else {
    // Generar el código QR
    QR.makeCode(link);
    
    // Marcar el código QR como utilizado
    codigosQRUtilizados[link] = true;
  }
});

// Función para validar si el enlace es válido (puedes personalizar esta función según tus requisitos)
function esEnlaceValido(enlace) {
  // Ejemplo de validación: comprobar si el enlace comienza con "http://" o "https://"
  return enlace.startsWith("http://") || enlace.startsWith("https://");
}