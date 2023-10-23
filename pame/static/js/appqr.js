document.addEventListener("DOMContentLoaded", function () {
	// Función para generar el código QR
	function generarQR() {
		const qr_link = "{{ initial_qr_link }}";
		const qrcode = new QRCode(document.getElementById("contenedorQR"), qr_link);
	}

	// Agrega un evento para abrir el modal
	const miModal = document.getElementById("miModal");
	miModal.addEventListener("show.bs.modal", function () {
		generarQR();
	});

	// Genera el QR al cargar la página
	generarQR();
});