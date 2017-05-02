from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings

import os

from forms import FileUpload
from models import ImageUploadModel


from doorMeasure.determineDoorSize import determine_door_size

# froms view function with the Forms class

def upload(request):
	if request.method == 'POST':
		form = FileUpload(request.POST, request.FILES)
		ImageUploadModel.objects.all().delete()
		if form.is_valid():
			form.save()
			image = ImageUploadModel.objects.latest('id')
			imageUrl = settings.BASE_DIR + image.model_pic.url
	
			height, width = determine_door_size(imageUrl)
			return render(request, 'home.html', {'imageUrl':image.model_pic.url, 'height':height, 'width': width,})
	else:
		form = FileUpload()

	return render(request, 'upload_form.html', {'form': form})

def showHomePage(request):
	return render_to_response('index.html')

def showFridge1(request):
	return render_to_response('fridge1.html')

# def showUplads(request):
# 	images = ImageUploadModel.objects.all()
# 	return render(request, 'home.html', {'images': images})