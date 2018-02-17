from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import ward, dendrogram

filenames = [
'DATA/Austen_Emma.txt', 
'DATA/Austen_Pride.txt',
'DATA/Austen_Sense.txt', 
'DATA/CBronte_Jane.txt',
'DATA/CBronte_Professor.txt', 
'DATA/Dickens_Bleak.txt',
'DATA/Dickens_David.txt', 
'DATA/Dickens_Hard.txt',

'DATA/ABronte_Agnes.txt',
'DATA/ABronte_Tenant.txt',
'DATA/CBronte_Villette.txt',
'DATA/EBronte_Wuthering.txt',
]

vectorizer = CountVectorizer(input='filename')
#Using input='filename' means that fit_transform will
#expect a list of file names
#dtm is document term matrix (a sparse matrix)
dtm = vectorizer.fit_transform(filenames) 
print(type(dtm))
#vocab is a vocabulary list of each word that appears
vocab = vectorizer.get_feature_names() # change to a list
dtm = dtm.toarray() # convert to a regular array
print(list(vocab)[500:550])

##Ways to count the word "house" in Emma (file 0 in the list of files)
house_idx = list(vocab).index('house') #index of "house" print(house_idx)
print(dtm[0, house_idx])
#There are 95 occurrences of “house” in Emma
#Counting "house" in Pride and Prejudice (107 in Pride)
print(dtm[1,house_idx])
print(list(vocab)[house_idx]) #this will print “house”
print(dtm) #prints the doc term matrix

##Create a table of word counts to compare Emma and Pride and Prejudice
columns=["BookName", "house","and","almost"]
MyList=["Emma"]
MyList2=["Pride"]
MyList3=["Sense"]
for someword in ["house","and", "almost"]:
	EmmaWord = (dtm[0, list(vocab).index(someword)])
	MyList.append(EmmaWord)
	PrideWord = (dtm[1, list(vocab).index(someword)])
	MyList2.append(PrideWord)
	SenseWord = (dtm[2, list(vocab).index(someword)])
	MyList3.append(SenseWord)
#print(MyList)
#print(MyList2)
df2=pd.DataFrame([columns, MyList,MyList2, MyList3])
print(df2)

#Euclidean Distance
dist = euclidean_distances(dtm)
print(np.round(dist,0))
#The dist between Emma and Pride is 3856

#Cosine Similarity
cosdist = 1 - cosine_similarity(dtm)
print(np.round(cosdist,3)) #cos dist should be .02



#2D

## This type of visualization is called multidimensional scaling (MDS)
mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
## "precomputed" means we will give the dist (as cosine sim)
pos = mds.fit_transform(cosdist) # shape (n_components, n_samples)
xs, ys = pos[:, 0], pos[:, 1]
names=["Austen_Emma", "Austen_Pride", "Austen_Sense", "CBronte_Jane",
"CBronte_Professor", "Dickens_Bleak",
"Dickens_David", "Dickens_Hard",'ABronte_Agnes',
'ABronte_Tenant',
'CBronte_Villette',
'EBronte_Wuthering']

for x, y, name in zip(xs, ys, names):
	plt.scatter(x, y, c='red',marker='s',s=100)
	plt.text(x, y, name)

plt.show()


#3D
mds = MDS(n_components=3, dissimilarity="precomputed", random_state=1)
pos = mds.fit_transform(cosdist)
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2],marker='^',s=150,c='g')
for x, y, z, s in zip(pos[:, 0], pos[:, 1], pos[:, 2], names):
	ax.text(x, y, z, s)

ax.set_xlim3d(-.06,.07) #stretch out the x axis
ax.set_ylim3d(-.012,.008) #stretch out the y axis
ax.set_zlim3d(-.05,.08) #stretch out the z axis
plt.show()



## Clustering Texts and Visualizing
#One method for clustering is Ward’s
#Ward’s method produces a hierarchy of clusterings
# Ward’s method requires a set of pairwise distance measurements

linkage_matrix = ward(cosdist)
dendrogram(linkage_matrix, orientation="left", labels=names,color_threshold=.04)
plt.tight_layout()
plt.show()
