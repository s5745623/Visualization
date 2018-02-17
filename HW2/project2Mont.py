#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: yuanyaozhang
"""

import pandas as pd
from pprint import pprint
import datetime
import numpy as np
#from orangecontrib.associate.fpgrowth import *

#########collectiong new data##########
'''
url = ("https://data.montgomerycountymd.gov/resource/yc8a-5df8.json?$$app_token=tX2XTxtf7mZd8F5eQ7enqtsPO")
dataMontgomeryCrime_1 = pd.read_json(url)
dataMontgomeryCrime_1.to_csv('dataMontgomeryCrime_Original.csv')
'''
dataFile = open('dataMontgomeryCrime_Original.csv','r')
dataMontgomeryCrime = pd.read_csv(dataFile, sep=',', encoding='latin1')


#######data cleaning##########
# remove unnecessary column
dataMontgomeryCrime = dataMontgomeryCrime.drop(['Unnamed: 0',':@computed_region_tx5f_5em3',':@computed_region_rbt8_3x7n',':@computed_region_kbsp_ykn9',':@computed_region_d7bw_bq6x',':@computed_region_6ryf_isx3'
                                                ,'incident_id','sector','police_district_number'], axis=1)
dataMontgomeryCrime.fillna(0)


# narrative, place, address
dataMontgomeryCrime['narrativeCrime, place, address'] = dataMontgomeryCrime[['narrative', 'place','location']].apply(tuple, axis=1)


#########time
dataMontgomeryCrime['date'] = pd.to_datetime(dataMontgomeryCrime['date'])

period ={0:'0:00-4:00',1:'4:00-8:00',2:'8:00-12:00',3:'12:00-16:00',4:'16:00-20:00',5:'20:00-24:00'}
def findTimePeriod(x):
    if (x <= datetime.time(4,00)) & (x > datetime.time(0,00)):
        return period[0]
    elif (x <= datetime.time(8,00)) & (x > datetime.time(4,00)):
        return period[1]
    elif (x <= datetime.time(12,00)) & (x > datetime.time(8,00)):
        return period[2]
    elif (x <= datetime.time(16,00)) & (x > datetime.time(12,00)):
        return period[3]
    elif (x <= datetime.time(20,00)) & (x > datetime.time(16,00)):
        return period[4]
    elif (x <= datetime.time(23,00)) & (x > datetime.time(20,00)):
        return period[5]

dataMontgomeryCrime['time'] = dataMontgomeryCrime['date'].dt.time       
dataMontgomeryCrime['time_section'] = dataMontgomeryCrime['time'].apply(findTimePeriod)


##########day_of_week
dataMontgomeryCrime['day_of_week'] = dataMontgomeryCrime['date'].dt.dayofweek
days = {0:'Mon',1:'Tues',2:'Weds',3:'Thurs',4:'Fri',5:'Sat',6:'Sun'}
dataMontgomeryCrime['day_of_week'] = dataMontgomeryCrime['day_of_week'].apply(lambda x: days[x])

###############################################

dataMontgomeryCrime2 = dataMontgomeryCrime.drop(['incident_type','zip_code','latitude','longitude','address_number','case_number','pra','start_date','end_date','date'], axis=1)

print(dataMontgomeryCrime.describe())
print()
print(dataMontgomeryCrime2.mode())

print('Statistic of Narrative')
Narrative = dataMontgomeryCrime['narrative'].value_counts()
print(Narrative)
print()

print('Statistic of time_section')
time_section = dataMontgomeryCrime['time_section'].value_counts()
print(time_section)
print()

print('Statistic of day_of_week')
day_of_week = dataMontgomeryCrime['day_of_week'].value_counts()
print(day_of_week)
print()

'''Bin the data 300-400 is Robbery,400-500 is AGG ASSLT, 500-600 is BURG NO FORCE)'''
#####clean the class of string which is meanless when in numeric
dataMontgomeryCrime1 = dataMontgomeryCrime[dataMontgomeryCrime.incident_type != 'D']
dataMontgomeryCrime1 = dataMontgomeryCrime1[dataMontgomeryCrime.incident_type != 'DMV']
dataMontgomeryCrime1 = dataMontgomeryCrime1[dataMontgomeryCrime.incident_type != 'N']
dataMontgomeryCrime1 = dataMontgomeryCrime1[dataMontgomeryCrime.incident_type != 'M']
dataMontgomeryCrime1 = dataMontgomeryCrime1[dataMontgomeryCrime.incident_type != 'OTH']
dataMontgomeryCrime1 = dataMontgomeryCrime1[dataMontgomeryCrime.incident_type != 'SWR']

dataMontgomeryCrime1['incident_type'] = dataMontgomeryCrime1['incident_type'].astype(int)

minnum = dataMontgomeryCrime1['incident_type'].min()
maxNum = dataMontgomeryCrime1['incident_type'].max()

#after deleting the reluctant data the data start with 11
minNum= minnum - 11

bins = np.arange(minNum, maxNum, 100)
NumBins = pd.cut(dataMontgomeryCrime1['incident_type'], bins, retbins = True)

print('\n\nClass Num:')
pprint(NumBins)

Num1=np.digitize(dataMontgomeryCrime1['incident_type'],bins)
NumBinsCounts = np.bincount(Num1)
print('\n\nClass Num Bin count is:')
pprint(NumBinsCounts)
print()


dataMontgomeryCrime.to_csv('dataMontgomeryCrime1.csv')