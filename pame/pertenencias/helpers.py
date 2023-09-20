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
