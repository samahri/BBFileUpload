#import the necessary packages
from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import object_recognition as objr
import os
	
def determine_door_size(image_path):
	# Here we define the range of acceptable height to width ratios for doors
	#Door_ratio = [2.0,3.0]
	Door_ratio = [1.8,3.0]
	ref_ratio = [1.3,1.5] # This is the dimension of a paper
	tol = 20.0 # Difference between area-rectagle
	#Door_min_ratio  = 0.01 # 10% at least
	Door_min_ratio  = 0.01 # The minimum area taken by the fridge

	# absolute dimensions
	ref_length = 0.297 # [Meters]
	ref_width = 0.210 # [Meters]
	ref_area= ref_length*ref_width # [M**2]
	ref_min_ratio = 0.005

	info =1

	#=======================================================================
	# construct the argument parse and parse the arguments

	image = cv2.imread(image_path)

	height, width, channels = image.shape 
	pixels = image.size

	# The standard pixel
	# 1080 by 1920
	#pixels_x = 960.0
	#pixels_y = 960.0
	pixels_x = 600.0
	pixels_y = 600.0

	scale_y = height/pixels_y
	scale_x = width/pixels_x

	if(scale_x>1.0 and scale_y > 1.0):
		scale_x = 1.0/scale_x
		scale_y = 1.0/scale_y
	else:
		scale_x = 1.0
		scale_y = 1.0


	image_area = float(height)*float(width)

	# print '=================================================='
	# print 'Image Parameters: ', height,width,channels,pixels
	# print '=================================================='

	# print 'scale', scale_x,scale_y
	#image = cv2.resize(image, (0,0), fx=args["scale"], fy=args["scale"]) 
	image = cv2.resize(image, (0,0), fx=scale_x, fy=scale_x) 


	# Locate the Door
	# Now we optimize
	x0 = objr.optimize_recognition(image,tol,Door_ratio,Door_min_ratio)
	n = int(x0)
	# print 'optimal n:', n,x0
	cnt,num_features,diff_door,objectImage_ratio = objr.locate_door(image,tol,Door_ratio,Door_min_ratio,n,info)
	ratio_door,corners,x,y,w,h = objr.determine_shape(cnt)
	door_h = float(h)
	door_w = float(w)

	# Locate the reference object
	cnt2,num_features,diff,objectImage_ratio = objr.locate_door(image,tol,ref_ratio,ref_min_ratio,1,info)
	ratio,corners,x2,y2,w2,h2 = objr.determine_shape(cnt2)
	# Determine the Approximate Area
	ref_object_area = float(w2)*float(h2)		
	# Now, we determine the unit conversion
	# print 'ratio ref:', ratio
	# print 'ref object: ', diff

	# To correct for slight image distortion
	quench_factor =1.04 #0.95 #0.95 #0.94

	unit_coversion = np.sqrt(ref_area/ref_object_area)*(1.0-(diff/100.0))

	# Draw contours around the objects we found
	cv2.rectangle(image,(x,y),(x+w,y+h),(0,255,0),2)
	cv2.drawContours(image,[cnt],0,(0,0,255),2)	

	cv2.rectangle(image,(x2,y2),(x2+w2,y2+h2),(0,255,0),2)
	cv2.drawContours(image,[cnt2],0,(0,0,255),2)	

	h_meters = door_h*unit_coversion*quench_factor*100.0
	w_meters = door_w*unit_coversion*100.0

	# print  h_meters,w_meters

	standard_door_h = [203.2, 213.36, 243.84]
	standard_door_w = [ 60.96,71.12, 73.152,76.2, 81.28, 91.44,106.68]

	# Compute the standard ratios
	dstandard_ratios = [[abs((standard_door_h[i]/standard_door_w[j])-ratio_door*(1.0+diff_door/100.0)) for i in range(len(standard_door_h))] for j in range(len(standard_door_w))]

	#print standard_ratios

	# If we didn't find a reference object, we estimate the probable dimensions
	if diff==100000.0:
		# Find Min values:
		rmin =100.0
		imin=0
		jmin=0
		for j in range(len(dstandard_ratios)):
			for i in range(len(dstandard_ratios[0])):
				r = dstandard_ratios[j][i]

				if r < rmin:
					rmin =r
					imin =i
					jmin =j
		# print 'Warning: Dimensions Calculated without Reference Object'
		# print 'Estimated object: No ref'		
		# print imin,jmin, standard_door_h[imin], standard_door_w[jmin]
		h_meters = standard_door_h[imin]
		w_meters = standard_door_w[jmin]
	
	else:
		# Find minimum deviation
		diff_h = [abs(standard_door_h[i]-h_meters) for i in range(len(standard_door_h))]
		indx_h = diff_h.index(min(diff_h))
		h_meters = standard_door_h[indx_h]

		diff_w = [abs(standard_door_w[i]-w_meters) for i in range(len(standard_door_w))]
		indx_w = diff_w.index(min(diff_w))
		w_meters = standard_door_w[indx_w]

	# print ''
	# print ''
	# print '=============================================================='
	# print 'Estimated Door Dimensions: '
	# print  'Height: [cm]', h_meters
	# print  'Width: [cm]', w_meters
	# print '=============================================================='

	# cv2.putText(image, 'HxW: '+"{:.2f} x {:.2f} [cm]".format(h_meters ,w_meters),
	# 		(int(10), int(20)), cv2.FONT_HERSHEY_SIMPLEX,
	# 		0.45, (255, 0, 0), 1)


	# cv2.imshow('image',image)
	# cv2.waitKey(0)

	picName = 'DOOR_ID.png'
	cv2.imwrite(os.path.join('media/images/',picName) , image)
	return h_meters ,w_meters
	# return image_path