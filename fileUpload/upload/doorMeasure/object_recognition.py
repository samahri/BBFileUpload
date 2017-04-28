# This subroutine determines the shape of a given object
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from scipy.optimize import minimize
import math
#import matplotlib as plt
import os

def preProcessImage(img,n):
	
	# Convert to Grey Scale
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	picName = 'step1.png'
	cv2.imwrite(os.path.join('media/images/',picName) , gray)
	
	# Gaussian Blur
	for n in range(0,n):
		gray = cv2.GaussianBlur(gray, (7, 7), 0)
	#gray = cv2.GaussianBlur(gray, (7, 7), 0)
	#gray = cv2.GaussianBlur(gray, (7, 7), 0)
	# Try to find the edges
	edged = cv2.Canny(gray, 50, 100)
	
	picName = 'step2.png'
	cv2.imwrite(os.path.join('media/images/',picName), edged)
	
	# Higlight the edges
	# We try to close the image
	#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
	#edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	
	#
	#edged = cv2.dilate(edged, None, iterations=5)
	
	kernel = np.ones((5,5),np.uint8)
	edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	#edged = cv2.morphologyEx(edged, cv2.MORPH_OPEN, kernel)
	
	picName = 'step3.png'
	cv2.imwrite(os.path.join('media/images/',picName) , edged)
	
	#edged = cv2.medianBlur(edged,5)
	#cv2.imshow('image',edged)
	#cv2.waitKey(0)
	
	return edged



# Input: Contour
def determine_shape(cnt):
	
	# Connect the Contour
	peri = cv2.arcLength(cnt, True)
	
	# Find the corners of the contour
	approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
	
	# How many corners does the shape have
	corners = len(approx)
	
	# The bounding rectangle function
	x,y,w,h = cv2.boundingRect(cnt)
	
	ratio = float(h)/float(w)
	
	return ratio,corners,x,y,w,h


# This function will locate a fridge in an image according to four points



# This function locates the door according to a given specification
def locate_door(image,tol,Door_ratio,min_ratio, n,info):
	
	img_h, img_w, channels = image.shape 
	img_area = float(img_h*img_w)
	
	edged = preProcessImage(image,n)
	
	thresh = cv2.adaptiveThreshold(edged,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
           cv2.THRESH_BINARY_INV,11,2)	
    
	picName = 'step4.png'
	cv2.imwrite(os.path.join('media/images/',picName), thresh)      
	
	# Now that the image has been thresholded, find contours
	contours,h = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	
	# Sort the Contours according to their areas
	contours = sorted(contours, key = cv2.contourArea , reverse = True)
	
	# The number of doors detected
	door_number =0
	max_door_area = 0
	
	# The number of reference objects detected 
	ref_object = 0
	
	# if info==1:
		# print '=================================='
		# print 'Number of Features:',len(contours)
		# print '=================================='
	
	for cnt in contours:
		ratio,corners,x,y,w,h = determine_shape(cnt)
		
		box_area = float(w)*float(h)
		actual_area = cv2.contourArea(cnt)
		area_diff = (abs(box_area-actual_area)/box_area)*100.0
		
		# The ratio of the object to the rest of the image
		area_ratio = (box_area/img_area)
		
		#print '=============================='
		#print 'r-value:', ratio
		#print 'corners: ',corners
		#print 'Area: w*h', float(w)*float(h)
		#print 'Area:  ', cv2.contourArea(cnt)
		#print 'Diff: ', area_diff
		#print '=============================='
		
		# Here we determine if the object fits dimension parameters
		if  (area_diff<=tol) and (Door_ratio[0]<=ratio<=Door_ratio[1]) and (area_ratio>= min_ratio):
			
			# Increase number of reference objects
			door_number = door_number+1
			
			# Determine the Area of this contour
			x,y,w,h = cv2.boundingRect(cnt)
			area = cv2.contourArea(cnt)	
			
			if area > max_door_area:
				max_door_area=area
				door_cnt=cnt
			
	
	if door_number==0:
		
		# if info==1:
			#print 'Error: No Object Found'
		num_features = 0
		diff = 100000.0
		objectImage_ratio =0.0
		
	else:
		cnt = door_cnt
		x,y,w,h = cv2.boundingRect(cnt)
		
		# draw a bounding rectangle around the door
		#cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
		
		# Draw the contours
		#cv2.drawContours(image,[cnt],0,(0,0,255),2)
		
		door_h = float(h)
		door_w = float(w)
		area = cv2.contourArea(cnt)
		diff = (abs(door_h*door_w-cv2.contourArea(cnt))/abs(door_h*door_w))*100.0
		objectImage_ratio = (float(door_h*door_w)/float(img_area))*100.0
		num_features = len(contours)
		
		# if(info==1):
			# print '=============================='	
			# print 'Object Height:',h
			# print 'Object Width:' ,w
			# print 'H/W ratio: ', door_h/door_w
			# print 'Expected Area:' , door_h*door_w
			# print 'Actual Area:',cv2.contourArea(cnt)
			# print 'Percent Diff: ', diff
			# print 'Object Image Ratio: ', objectImage_ratio 
			# print '=============================='	
		
	return cnt,num_features,diff,objectImage_ratio
		
		

# This function locates the door according to a given specification
def locate_fridge(img):
	
	max_area = 0.6
	min_area = 0.01
	object_num = 0
	
	# absolute dimensions
	ref_length = 0.297 # [Meters]
	ref_width = 0.210 # [Meters]
	ref_area= ref_length*ref_width # [M**2]
		
	
	# Dimensions of the image file
	img_h, img_w, channels = img.shape 
	img_area = float(img_h*img_w)
	f_height = 0
	f_width  = 0
	indx_1 = 0
	
	top_freezer = True
	bottom_freezer = False
		
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	picName = 'step1_fridge.png'
	cv2.imwrite(os.path.join('media/images/',picName) ,gray) 
	
	edged = cv2.Canny(gray, 50, 100)
	
	picName = 'step2_fridge.png'
	cv2.imwrite(os.path.join('media/images/',picName) ,edged)
	
	kernel = np.ones((5,5),np.uint8)
	edged = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
	
	picName = 'step3_fridge.png'
	cv2.imwrite(os.path.join('media/images/',picName) ,edged)
	
	
	# We sort the picture
	corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
	corners = np.int0(corners)
	contours,h = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	contours = sorted(contours, key = cv2.contourArea , reverse = True)[:4]
	
	# We Loop over the Contours
	for cnt in contours:
		peri = cv2.arcLength(cnt, True)
		
		approx = cv2.approxPolyDP(cnt, 0.04 * peri, True)
		
		ratio,corners,x,y,w,h = determine_shape(cnt)
		
		box_area = float(w)*float(h)
		area_ratio = (box_area/img_area)
		
		indx_1 = indx_1+1
		
		if corners>=4 and area_ratio<= max_area and area_ratio>= min_area:
			
			# Increase the number of found objects
			object_num=object_num+1
			
			
			# print 'h:',h
			
			if(object_num==1):
				indx=indx_1
				y1=y
			
			if(object_num <=2):
				f_height = f_height+h
				
				if y>y1 and object_num==2:
					# print 'Bottom Freezer'
					bottom_freezer = True
					top_freezer = False
					
				elif  y<y1 and object_num==2:
					# print 'Top Freezer'
					top_freezer = True
					bottom_freezer = False
				
				# Take the max width
				if w > f_width:
					f_width = w
			
			if(object_num==3):
				fh0 = h
				fw0 = w
				
				
			actual_area = cv2.contourArea(cnt)
			cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
			# print (box_area/img_area)*100.0
	
	# Compute the area of the little paper
	diff_ratio = min(abs((ref_width/ref_length)- (float(fw0)/float(fh0))),abs((ref_width/ref_length)- (float(fh0)/float(fw0))))
	
	# print 'Difference: ', diff_ratio
	
	
	object_area = float(fh0*fw0)
	
	# print 'Height and Width of Fridge: ', f_height, f_width
	# print 'Height and Width of Sheet: ', fh0, fw0
	
	unit_coversion = np.sqrt(ref_area/object_area)
	

	
	fridge_height_m = unit_coversion*float(f_height)
	fridge_width_m = unit_coversion*float(f_width)
	
	# Top freezer 
	if(top_freezer==True):
		#standard_height = range(1.638,1.740,0.001)
		
		if(1.638 <= fridge_height_m <= 1.740):
			print 'true'
		else:
			quench_factor = float(1.638)/float(fridge_height_m)
			fridge_height_m = fridge_height_m*quench_factor
			fridge_width_m = fridge_width_m #*quench_factor
			#print 'FAlSE!'
			
	# In case we have a bottom Freezer		
	elif(bottom_freezer==True):
		if(1.690 <= fridge_height_m <= 1.740):
			print 'true'
		else:
			quench_factor = float(1.638)/float(fridge_height_m)
			fridge_height_m = fridge_height_m*quench_factor
			fridge_width_m = fridge_width_m #*quench_factor
			#print 'FAlSE!'
	
	# print '=================================================='
	
	# if(top_freezer==True):
	# 	print 'The Fridge is a Top Freezer'
	
	# if(bottom_freezer==True):
	# 	print 'The Fridge is a Bottom Freezer'
	
	# print 'Fridge Height: [m] ', fridge_height_m*(1.0+diff_ratio)
	# print 'Fridge Width: [m] ', fridge_width_m*(1.0+diff_ratio)
	# print '=================================================='
	
	
	ratio,corners,x0,y0,w0,h0 = determine_shape(contours[indx])
	#cv2.rectangle(img,(x0,y0),(x0+f_width,y0+f_height),(255,0,0),2)
	cv2.imshow('image',img)
	cv2.waitKey(0)
    
	cv2.putText(img, 'HxW: '+"{:.2f} x {:.2f} [m]".format( fridge_height_m ,fridge_width_m),
		(int(10), int(20)), cv2.FONT_HERSHEY_SIMPLEX,
		0.45, (0, 0, 255), 1)
    	
	picName = 'FRIDGE_ID.png'
	cv2.imwrite(os.path.join('media/images/',picName) , img)
	

# This function optimizes the recognition parameters
def optimize_recognition(image,tol,Door_ratio,min_ratio):
	
	a1= 0.5
	a2= 1.0
	a3=-1.5
	
	val=100000.0
	n0=0
	
	def fitness_func(n):
		cnt,num_features,diff,objectImage_ratio = locate_door(image,tol,Door_ratio,min_ratio, n,0)
		E0 = a1*float(num_features)+a2*float(diff)+a3*float(objectImage_ratio)
		# print n,E0,float(num_features),float(diff),float(objectImage_ratio)
		return E0
		#return float(num_features),float(diff),float(objectImage_ratio)
	
	for i in range(0,5):
		#x1,x2,x3 =  fitness_func(i)
		val_k = fitness_func(i)
		#print 'i', i,val_k
		
		if val_k < val:
			val =val_k
			n0 = i 
	
	#print 'xm', xm.x[0]
	#n0=1
	#cv2.imshow('image',edged)
	#cv2.waitKey(0)
	
	
	return n0

# This function optimizes the recognition parameters
def optimize_recognition_fridge(image,tol,Door_ratio,min_ratio):
	
	a1= 0.5
	a2= 1.0
	a3=-1.5
	
	val=100000.0
	n0=0
	
	def fitness_func(n):
		cnt,num_features,diff,objectImage_ratio = locate_fridge(image,tol,Door_ratio,min_ratio, n,0)
		E0 = a1*float(num_features)+a2*float(diff)+a3*float(objectImage_ratio)
		# print n,E0,float(num_features),float(diff),float(objectImage_ratio)
		return E0
		#return float(num_features),float(diff),float(objectImage_ratio)
	
	for i in range(0,5):
		#x1,x2,x3 =  fitness_func(i)
		val_k = fitness_func(i)
		#print 'i', i,val_k
		
		if val_k < val:
			val =val_k
			n0 = i 
	
	#print 'xm', xm.x[0]
	#n0=1
	#cv2.imshow('image',edged)
	#cv2.waitKey(0)
	
	
	return n0