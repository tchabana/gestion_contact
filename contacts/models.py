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
        qr_image = qrcode.make(f"Nom: {self.first_name} \n PreNom: {self.last_name} \n Tel: {self.phone}")  # Générer le code QR en utilisant les informations du contact
        canvas = Image.new('RGB',(400,400),'white')     # Créer une image blanche de 400x400 pixels
        
        drow = ImageDraw.Draw(canvas)           # Créer un objet "drow" pour dessiner sur le canevas
        canvas.paste(qr_image)                  # Coller l'image du code QR sur le canevas blanc
        file_name = f"qr_{self.pk}.png"         # Générer un nom de fichier unique pour l'image du code QR
        
        buffer = BytesIO()                      # Créer un tampon de mémoire (buffer) pour enregistrer l'image en format PNG
        canvas.save(buffer,'png')
        
        self.qr_code_image.save(file_name,File(buffer),save=False) # Enregistrer l'image dans le champ qr_code_image
        canvas.close  # Fermer le canevas
        return super().save(*args, **kwargs) # Appeler la méthode save() de la classe parent (super) pour effectuer la sauvegarde en base de données
