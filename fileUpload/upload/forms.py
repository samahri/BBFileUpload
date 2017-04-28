from django import forms

from fileUpload.upload.models import ImageUploadModel

class FileUpload(forms.ModelForm):
	class Meta:
		model = ImageUploadModel
		fields = ('model_pic',)
