from __future__ import unicode_literals

from django.db import models


# class imageUploaded(models.Model): 
# 	model_pic = models.ImageField(upload_to = 'images/', default='none')

# Create your models here.
class ImageUploadModel(models.Model):
	# need to install Pillow library (Why? I think "ImageField" uses some of its functions)
	# picArray = models.ForeignKey(imageUploaded)
	upload = models.ImageField(upload_to = 'images/', default='none')
	

		