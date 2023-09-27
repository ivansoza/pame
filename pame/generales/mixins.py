from django.views import View
import os
from PIL import Image
from reportlab.pdfgen import canvas
from django.core.files.base import ContentFile
from io import BytesIO

def image_to_pdf(image_field):
    # Abrir la imagen usando Pillow desde el InMemoryUploadedFile
    img = Image.open(image_field)

    buffer = BytesIO()

    # Usar ReportLab para crear un PDF con la imagen
    width, height = img.size
    p = canvas.Canvas(buffer, pagesize=(width, height))
    
    # En lugar de image_field.path, usamos el objeto img
    p.drawInlineImage(img, 0, 0, width=width, height=height)
    p.showPage()
    p.save()

    pdf = ContentFile(buffer.getvalue())
    return pdf


class HandleFileMixin(View):
    def handle_file(self, instance, file_field_name):
        file = self.request.FILES.get(file_field_name)
        if file:
            # Almacenar la ruta original del archivo para poder eliminarlo luego.
            original_file_path = instance.__getattribute__(file_field_name).path
            
            name, ext = os.path.splitext(file.name)
            if ext.lower() == '.pdf':
                getattr(instance, file_field_name).save(
                    f"{file_field_name}.pdf",
                    file
                )
            else:
                getattr(instance, file_field_name).save(
                    f"{file_field_name}.pdf",
                    image_to_pdf(file)
                )
            
            # Eliminar el archivo original después de guardar el nuevo.
            if os.path.exists(original_file_path):
                os.remove(original_file_path)