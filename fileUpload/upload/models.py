from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ImageUploadModel(models.Model):
	# description = models.CharField(max_length=255, blank=True)
	# need to install Pillow library (Why? I think "ImageField" uses some of its functions)
	model_pic = models.ImageField(upload_to = 'images/', default='none')
	uploaded_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.model_pic.url 

		