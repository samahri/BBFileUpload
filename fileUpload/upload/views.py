from django.http import HttpResponse
from django.shortcuts import render, redirect, render_to_response
from django.conf import settings

import os

from forms import FileUpload
from models import ImageUploadModel


from doorMeasure.determineDoorSize import determine_door_size

# froms view function with the Forms class

def upload(request, fridgeNumber):
	if request.method == 'POST':
		form = FileUpload(request.POST, request.FILES)
		ImageUploadModel.objects.all().delete()
		if form.is_valid():
			form.save()
			image = ImageUploadModel.objects.latest('id')
			imageUrl = settings.BASE_DIR + image.upload.url
	
			pathHeight, pathWidth = determine_door_size(imageUrl)
			
			if int(fridgeNumber) == 1:
				fridgeHeight = 169
				fridgeWidth = 75

			elif int(fridgeNumber) == 2:
				fridgeHeight = 151.9
				fridgeWidth = 61

			elif int(fridgeNumber) == 3:
				fridgeHeight = 167.96
				fridgeWidth = 76.2

			return render(request, 'results.html', {'imageUrl':image.upload.url, 'pathHeight':pathHeight, 'pathWidth': pathWidth,
													'fridgeHeight':fridgeHeight, 'fridgeWidth': fridgeWidth, 
													'fridgeNumber':fridgeNumber})
	else:
		form = FileUpload()

	return render(request, 'upload_form.html', {'form': form})

def showHomePage(request):
	return render_to_response('index.html')

def showFridge(request, fridgeNumber):
	return render_to_response('fridgeDisplay.html', {'fridgeNumber':fridgeNumber})

# def showUplads(request):
# 	images = ImageUploadModel.objects.all()
# 	return render(request, 'home.html', {'images': images})