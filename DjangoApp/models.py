from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django_resized  import ResizedImageField
from PIL import Image, ExifTags

# Create your models here.
class UserInfo(models.Model):
    id=models.IntegerField(primary_key=True)
    firstname = models.CharField(max_length=100,null=True)
    lastname = models.CharField(max_length=100,null=True)
    phonenumber = models.CharField(max_length=10,null=True)
    gender = models.CharField(max_length=100,null=True)
    avatar = models.ImageField(null=True, default=None)
    introduction=models.CharField(max_length=200,null=True)
    date = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField(null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    star = models.FloatField(default=0)
    address = models.CharField(max_length=100)
    image = ResizedImageField(size=[700, 400], blank=True, null=True,quality=90)
    imagePhone = ResizedImageField(size=[300, 200], blank=True, null=True,quality=70, upload_to="phone",force_format='WEBP')
    lat = models.CharField(max_length=200,blank=True,null=True)
    lng = models.CharField(max_length=200,blank=True,null=True)
    idUser = models.ForeignKey("UserInfo", on_delete=models.CASCADE, null= True)
    tags = models.ManyToManyField(Tag)
    numcreact=models.IntegerField(default=0)
    totalstar=models.IntegerField(default=0)
    def __str__(self):
        return self.title
    def save(self, *args, **kwargs):
        if self.imagePhone:
            # Open the image using Pillow
            image = Image.open(self.imagePhone)
            
            # Check for EXIF data and rotation information
            if hasattr(image, '_getexif'):
                exif = image._getexif()
                if exif and ExifTags.TAGS.get(orientation := exif.get(0x0112)):
                    if orientation == 3:
                        image = image.rotate(180, expand=True)
                    elif orientation == 6:
                        image = image.rotate(270, expand=True)
                    elif orientation == 8:
                        image = image.rotate(90, expand=True)
            
            # Save the modified image
            image.save(self.imagePhone.path, 'WEBP')

        super().save(*args, **kwargs)
class Comment(models.Model):
    id=models.AutoField(primary_key=True)
    content=models.CharField(max_length=200)
    date=models.DateTimeField(auto_now_add=True)
    idPost=models.ForeignKey("Post",on_delete=models.CASCADE,null=True)
    idUsercomment=models.ForeignKey("UserInfo",on_delete=models.CASCADE,null=True)
    idcommentReply=models.ForeignKey("self",on_delete=models.CASCADE,null=True,blank=True)

class React(models.Model):
    id=models.AutoField(primary_key=True)
    star= models.IntegerField(default=0)
    idpost=models.ForeignKey("Post",on_delete=models.CASCADE,null=True)
    iduser=models.ForeignKey("UserInfo",on_delete=models.CASCADE,null=True)
    
class HistoryChat(models.Model):
    id=models.AutoField(primary_key=True)
    content=models.CharField(max_length=1000)
    iduser=models.ForeignKey("UserInfo",on_delete=models.CASCADE,null=True)
    fromAI=models.BooleanField(default=0)
    