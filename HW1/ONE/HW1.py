####################################
# Yuan-Yao Chang
# ANLY503
# HW 1
####################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dataFile = open('USA_Cancer_Stats_1999_2012_CDC_orgSite_New.csv','r')
df = pd.read_csv(dataFile, sep=',', encoding='latin1')

#drop unnecessary column
df = df.drop(['AgeGroup','StateCode','RaceCode','SexCode','LeadingCancerSitesCode'],1)

#group by State 

grouped_State = df.groupby('State')
grouped_State =  grouped_State['Count'].agg(np.sum).sort_values(ascending=False)

#group by Cancer US
grouped_Cancer = df.groupby('LeadingCancerSites')
grouped_Cancer =  grouped_Cancer['Count'].agg(np.sum).sort_values(ascending=False)

#Age Group
grouped_Age = df.groupby('AgeGroupCode')
grouped_Age =  grouped_Age['Count'].agg(np.sum).sort_values(ascending=False)


#group by Cancer District of Columbia
df_dc = df.loc[df['State'] == 'District of Columbia']
grouped_Cancer_dc = df_dc.groupby('LeadingCancerSites')
grouped_Cancer_dc =  grouped_Cancer_dc['Count'].agg(np.sum).sort_values(ascending=False)


#plot 
#US Cancer by States
fig = plt.figure(figsize=(15,20))
plt.title('US Cancer by States')
#grouped_State = grouped_State.to_dict()

X = np.arange(len(grouped_State))
plt.bar(X, list(grouped_State), align='center', width=0.5)
plt.xticks(X, grouped_State.index,rotation=90)
ymax = max(list(grouped_State)) + 1
plt.ylim(0, ymax)
#plt.show()
plt.savefig("HW1_1")
plt.close()

#Cancer Type Count
fig = plt.figure(figsize=(15,20))
plt.title('Cancer Type Count')
#grouped_Cancer = grouped_Cancer.to_dict()
X = np.arange(len(grouped_Cancer))
plt.bar(X, list(grouped_Cancer), align='center', width=0.5)
plt.xticks(X, grouped_Cancer.index,rotation=90)
ymax = max(list(grouped_Cancer)) + 1
plt.ylim(0, ymax)
#plt.show()
plt.savefig("HW1_2")
plt.close()

#Cancer Type Count in DC
fig = plt.figure(figsize=(15,20))
plt.title('Cancer Type Count in DC')
#grouped_Cancer_dc = grouped_Cancer_dc.to_dict()
X = np.arange(len(grouped_Cancer_dc))
plt.bar(X, list(grouped_Cancer_dc), align='center', width=0.5, color='red')
plt.xticks(X, grouped_Cancer_dc.index,rotation=90)
ymax = max(list(grouped_Cancer_dc)) + 1
plt.ylim(0, ymax)
#plt.show()
plt.savefig("HW1_3")
plt.close()



#Cancer Type Count in DC Pie Chart
fig = plt.figure(figsize=(15,15))
plt.title('Cancer Type Count in DC Pie Chart')
plt.pie(list(grouped_Cancer_dc),  labels=grouped_Cancer_dc.index, autopct='%1.1f%%', startangle=50)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.savefig("HW1_4")
plt.close()



