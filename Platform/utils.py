from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

def create_image_file():
    image = Image.new('RGB', (100, 100), color='red')
    image_file = BytesIO()
    image.save(image_file, 'JPEG')
    image_file.seek(0)
    return SimpleUploadedFile("image.jpg", image_file.read(), content_type="image/jpeg")

def remove_obj_img(obj, field_img_name):
    if hasattr(obj, field_img_name):
        setattr(obj, field_img_name, obj._meta.get_field(field_img_name).get_default())
        obj.save()
        return True
    return False

