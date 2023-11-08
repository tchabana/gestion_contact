from django.db import models

from django.db import models

import qrcode
from django.core.files import File
from io import BytesIO
from PIL import Image ,ImageDraw

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, unique=True)
    qr_code_image = models.ImageField(upload_to="qr_code",null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

    def save(self,*args, **kwargs):
        qr_image = qrcode.make(f"Nom: {self.first_name} \n PreNom: {self.last_name} \n Tel: {self.phone}")
        canvas = Image.new('RGB',(400,400),'white')
        drow = ImageDraw.Draw(canvas)
        canvas.paste(qr_image)
        file_name = f"qr_{self.pk}.png"
        buffer = BytesIO()
        canvas.save(buffer,'png')
        self.qr_code_image.save(file_name,File(buffer),save=False)
        canvas.close
        return super().save(*args, **kwargs)
