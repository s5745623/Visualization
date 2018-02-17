import requests

def main():

	file = open("ZipCodes.txt","r")
	f = file.read()
	zipcodes=f.split('\n')
	
	for i in range(len(zipcodes)):
		linkpart1 = 'http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode='
		ZipCodes = zipcodes[i]
		linkpart2 = '&date=2017-10-16&distance=25&API_KEY=F535B0F8-0B56-46F0-A301-1AEBAEE93B5B'
		
		link = linkpart1 + ZipCodes + linkpart2

		r = requests.get(link)
		data = r.json()
		#print(data[0]['AQI'])

		Data = data[0]
		AQI = Data['AQI']
		State = Data['StateCode']
		ReportArea = Data['ReportingArea']
		Lat = Data['Latitude']
		Long = Data['Longitude']

		with open('OUTPUT_AQI.txt','a') as txt:
			txt.write(ZipCodes+ ',' + State + ',' + ReportArea+ ',' + str(Lat)+ ',' + str(Long) + ','+ str(AQI) +'\n')
		txt.close()	

main()





		
