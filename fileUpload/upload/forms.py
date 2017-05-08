"""
Author: Sam Saud Almahri
Date: April 2017
"""
from django import forms

from fileUpload.upload.models import ImageUploadModel

class FileUpload(forms.ModelForm):
	class Meta:
		model = ImageUploadModel
		fields = ('upload',)
