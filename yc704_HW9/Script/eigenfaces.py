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
	facematrix = np.matrix(flat1)
	#facematrix = facevector1

	for i in range(1,len(images_list)):
		img = Image.open(images_list[i]).convert('L')
		imagearray = np.array(img) 
		flat = imagearray.ravel()
		facevector = np.matrix(flat)
		facematrix = np.r_[facematrix, facevector]
	

	facematrix_T = np.transpose(facematrix)
	
	return facematrix_T


def mean_face(ImageMatrix):

	row = ImageMatrix.shape[0]

	average = [] 
	for i in range(row):
		average.append(np.mean(ImageMatrix[i,:]))

	np_average = np.array(average)
	np_average = np.reshape(np_average, (112,92))
	#print(np_average.shape)
	path = os.getcwd()
	figpath = path + '/first5/'
	im = Image.fromarray(np.uint8(np_average),'L')
	#print(np_average)
	im.save(figpath + 'meanface.jpg')


def normalize(ImageMatrix):
	
	row = ImageMatrix.shape[0]
	#print(ImageMatrix.shape)

	normalized_ImageMatrix = []

	for j in range(row):
		normalized_ImageMatrix.append(ImageMatrix[j,:]-np.mean(ImageMatrix[j,:]))#row - row

	normalized_ImageMatrix = np.array(normalized_ImageMatrix)
	normalized_ImageMatrix = normalized_ImageMatrix.reshape(10304,400)
 	
	path = os.getcwd()
	with open(path + '/first5/eigen.txt', 'w') as f:
		f.write('The normalized matrix:' + '\n' + '{}'.format(normalized_ImageMatrix) + '\n')
	f.close()


	normalized_ImageMatrix_T = np.transpose(normalized_ImageMatrix)
	
	#Corvariance
	[a,b] = normalized_ImageMatrix.shape
	#print(normalized_A.shape)
	if(a>b):
		print('ATA')
		print('The normalized matrix:' + '\n' + '{}'.format(normalized_ImageMatrix))
		FinalMatrix = np.dot(normalized_ImageMatrix_T, normalized_ImageMatrix)#ATA
	elif (a<b):
		print('AAT')
		print('The normalized matrix:' + '\n' + '{}'.format(normalized_ImageMatrix))
		FinalMatrix = np.dot(normalized_ImageMatrix, normalized_ImageMatrix_T )#AAT


	return FinalMatrix, normalized_ImageMatrix


def eigen(FinalMatrix,normalized_ImageMatrix):
	
	#get eigencector
	eigenvalue, eigenvector = LA.eig(FinalMatrix)
	eigenvector = np.real(eigenvector)

	k = int(input("Enter an k eigenvalue <= 400: "))
	while (int(k)>400):
		print('\nMaximum k is 400, please re-enter!')
		k = int(input("Enter k <= 400: "))

	sorted_eigen = np.argsort(eigenvalue)[::-1]
	TopK_eigenvalue = sorted_eigen[:k]

	TopK_eigenvector = []
	for i in range(k):
		TopK_eigenvector.append(eigenvector[: ,TopK_eigenvalue[i]])

	#save eigenvectors
	path = os.getcwd()
	with open(path + '/first5/eigen.txt', 'a') as f:
		for j in range(k):
			f.write("eigenvector {}: ".format(j+1) + "\n" + "{}".format(TopK_eigenvector[j]) + "\n")
	f.close()

	#eigenfaces
	np_eigenvector = np.array(TopK_eigenvector)

	eigenface_list = []
	# print(normalized_ImageMatrix.shape)
	# print(np_eigenvector.shape)
	# print(range(len(TopK_eigenvector)))
	for i in range(len(TopK_eigenvector)):

		eigenface = np.dot(normalized_ImageMatrix, np_eigenvector[i])#(10304,1)
		# print(eigenface.shape)
		eigenface_list.append(eigenface)
		eigenface_image = np.reshape(eigenface, (112,92))

		#save eigenfaces
		fig = plt.figure()
		plt.imshow(eigenface_image, cmap=plt.get_cmap('Greys'))
		#plt.show()
		path = os.getcwd()
		figpath = path + '/first5/'
		fig.savefig(figpath + 'eigenface1_{}.jpg'.format(i))
		plt.close()


	eigenface_matrix = np.asmatrix(np.array(eigenface_list))

	print("The eigenface matrix: " + "\n" + "{}".format(eigenface_matrix.T))

	return eigenface_matrix



if __name__ == "__main__":
	
	images_list = get_image_path()
	ImageMatrix = FaceMatrix(images_list)
	mean_face(ImageMatrix)
	FinalMatrix,normalized_ImageMatrix = normalize(ImageMatrix)
	FinalMatrix = eigen(FinalMatrix,normalized_ImageMatrix)





