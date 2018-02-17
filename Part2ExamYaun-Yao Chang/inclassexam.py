import numpy as np
from numpy import linalg as LA


M = np.array([[1,4,2,4],[2,0,0,1],[3,2,0,2],[4,0,3,3],[5,0,0,4],[6,3,1,3]])


#1)
print('\n1)')
row = M.shape[0] 
average = [] 
for i in range(row):
	average.append(np.mean(M[i,:]))


np_average = np.array(average)
np_average = np.reshape(np_average, (6,1))
print('(a)mean column vector:')
print(np_average)
print('(b)mean column vector shape:')
print(np_average.shape)

#2)
print('\n2)')
A = []

for j in range(row):
	A.append(M[j,:]-np.mean(M[j,:]))
A = np.array(A)
A = A.reshape(6,4)
print('matrix A:')
print(A)

#3)
print('\n3)')
M_T = np.transpose(A)

Covariance = np.dot(M,M_T)
print('Covariance matrix (AAT):')
print(Covariance)

#4)
print('\n4)')
eigenvalue, eigenvector = LA.eig(Covariance)

for i in range(len(eigenvalue)):
	eigenvalue[i]=round(eigenvalue[i],3)
eigenvalue = np.real(eigenvalue)
print('eigenvalue:')
print(np.sort(eigenvalue))

#5)
print('\n5)')
for i in range(eigenvector.shape[0]):
	for k in range(eigenvector.shape[1]):
		eigenvector[i][k]=round(eigenvector[i][k],3)
eigenvector = np.real(eigenvector)
print('eigenvector:')
print(np.sort(eigenvector))

#6)
print('\n6)')
M_T = np.transpose(A)

Covariance_T = np.dot(M_T,M)
print('Covariance matrix (ATA):')
print(Covariance_T)

#7)
print('\n7)')
eigenvalue_T, eigenvector_T = LA.eig(Covariance_T)

for i in range(len(eigenvalue_T)):
	eigenvalue_T[i]=round(eigenvalue_T[i],3)
eigenvalue_T = np.real(eigenvalue_T)
print('eigenvalue:')
print(np.sort(eigenvalue_T))

#8)
print('\n8)')
for i in range(eigenvector_T.shape[0]):
	for k in range(eigenvector_T.shape[1]):
		eigenvector_T[i][k]=round(eigenvector_T[i][k],3)
eigenvector_T = np.real(eigenvector_T)
print('eigenvector:')
print(np.sort(eigenvector_T))

#9) in docx
print('\n9) in docx')

#10)
print('\n10)')
sorted_eigen = np.argsort(eigenvalue_T)[::-1]
Top_eigenvalue = sorted_eigen[:1]

Top_eigenvector = eigenvector_T[: ,Top_eigenvalue]
np_eigenvector = np.array(Top_eigenvector)


eigen = np.dot(M, np_eigenvector)
final = np.reshape(eigen, (6,1))

print('TOP1 eigenvector:')
print(final)









