"""
Author: Sam Saud Almahri
Date: April 2017
"""

from __future__ import unicode_literals

from django.db import models


class ImageUploadModel(models.Model):
	upload = models.ImageField(upload_to = 'images/', default='none')
	

		