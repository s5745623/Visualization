#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from numpy import linalg as LA
from PIL import Image
import os 
import matplotlib.image as mpimg
import matplotlib.pyplot as plt


def get_image_path():

	path = os.getcwd()# get folder in system path
	facedata_folder = os.listdir("FACESdata")#s1-s40 as list
	
	# mac folder log issue
	if ".DS_Store" in facedata_folder:
		facedata_folder.remove(".DS_Store")
	else:
		pass

	images_list = []
	for i in range(len(facedata_folder)):
	#read s1 - s40
		image_path = path + "/FACESdata" + "/" + facedata_folder[i]
		images = os.listdir(image_path)

		for j in range(len(images)):
		#read all images
			image_fullpath = image_path + "/" + images[j]
			images_list.append(image_fullpath)

	return images_list

def FaceMatrix(images_list):

	img1 = Image.open(images_list[0]).convert('L')
	imagearray1 = np.array(img1)
	flat1 = imagearray1.ravel() 
	facevector1 = np.matrix(flat1)
	facematrix = facevector1

	for i in range(1,len(images_list)):
		img = Image.open(images_list[i]).convert('L')
		imagearray = np.array(img) 
		flat = imagearray.ravel()
		facevector = np.matrix(flat)
		facematrix = np.r_[facematrix, facevector]
	
	facematrix_t = np.transpose(facematrix)
	
	return facematrix_t

def normalize(ImageMatrix):
	row = ImageMatrix.shape[0]
	column = ImageMatrix.shape[1]

	normalized_ImageMatrix = []
	for j in range(row):
		normalized_ImageMatrix.append(ImageMatrix[j,:]-np.mean(ImageMatrix[j,:]))

	normalized_ImageMatrix = np.array(normalized_ImageMatrix)
	normalized_ImageMatrix = normalized_ImageMatrix.reshape(10304,400)
 
	return normalized_ImageMatrix

def test1():

	#same steps as above
	path = os.getcwd()
	path = path + '/test1/'
	test1Image = Image.open(path + 'TEST_image.pgm').convert('L')
	imagearray_test1 = np.array(test1Image)
	flat_test1 = imagearray_test1.ravel() 
	facematrix_test1 = np.matrix(flat_test1)
	facematrix_test1 = np.transpose(facematrix_test1)

	test1_list = get_image_path()
	ImageMatrix = FaceMatrix(test1_list)

	row = ImageMatrix.shape[0]#10304
	column = ImageMatrix.shape[1]#400
	#print('{} {}'.format(row,column))

	normalized_test1_ImageMatrix = []
	for i in range(row):
		normalized_test1_ImageMatrix.append(facematrix_test1[i,0]-np.mean(ImageMatrix[i,:]))


	np_normalized_test1_ImageMatrix = np.array(normalized_test1_ImageMatrix)
	normalized_ImageMatrix = normalize(ImageMatrix)
	normalized_ImageMatrix_T = np.transpose(normalized_ImageMatrix)
	normalized_ImageMatrix = normalized_ImageMatrix

	FinalMatrix = np.dot(normalized_ImageMatrix_T, normalized_ImageMatrix)


	#eigen
	eigenvalue, eigenvector = LA.eig(FinalMatrix)
	eigenvector = np.real(eigenvector)

	k = int(input("Enter an k eigenvalue <= 400 for test 1: "))
	while (int(k)>400):
		print('\nMaximum k is 400, please re-enter!')
		k = int(input("Enter k <= 400 for test 1: "))

	sorted_eigen = np.argsort(eigenvalue)[::-1]
	TopK_eigenvalue = sorted_eigen[:k]

	TopK_eigenvector = []
	for i in range(k):
		TopK_eigenvector.append(eigenvector[:,TopK_eigenvalue[i]])
	


	#eigenface
	np_eigenvector = np.array(TopK_eigenvector)

	eigenface_list = []


	for i in range(len(TopK_eigenvector)):
		eigenface = np.dot(normalized_ImageMatrix, np_eigenvector[i])
		eigenface_list.append(eigenface)

	k_eigenmatrix = np.asmatrix(np.array(eigenface_list))
	# print(k_eigenmatrix.shape)
	# print(facematrix_test1.shape)
	test_face = np.dot(k_eigenmatrix, facematrix_test1)#(k, 10304) x (10304, 1)


	# cal euclidean dis
	euclidean_dis_list = []	
	for i in range(column):
		each_image = np.reshape(ImageMatrix[:,i], (10304,1))
		face_all = np.dot(k_eigenmatrix, each_image)
		euclidean_dist = LA.norm(test_face - face_all)
		euclidean_dis_list.append(euclidean_dist)

	#take min is list
	minimum = min(euclidean_dis_list)
	#print(minimum)
	minimum_id = euclidean_dis_list.index(minimum)

	FinalMatrix = np.reshape(ImageMatrix[:,minimum_id], (112,92))
	
	fig = plt.figure()
	plt.imshow(FinalMatrix, cmap=plt.get_cmap('Greys'))
	#plt.show()
	path = os.getcwd()
	figpath = path + '/test1/'
	#fig.savefig(figpath + 'PREDICTED_image.jpg')
	im = Image.fromarray(np.uint8(FinalMatrix),'L')
	im.save(figpath + 'PREDICTED_image.jpg')


if __name__ == "__main__":

	test1()
