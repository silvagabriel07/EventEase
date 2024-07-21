from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def create_image_file():
    image = Image.new('RGB', (100, 100), color='red')
    image_file = BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    return SimpleUploadedFile("image.jpg", image_file.read(), content_type="image/jpeg")