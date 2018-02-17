import requests
import pandas as pd 
import io

def main():


	#collecting data limited 3 rows
	url = "https://data.montgomerycountymd.gov/resource/yc8a-5df8.csv?$limit=3&$$app_token=tX2XTxtf7mZd8F5eQ7enqtsPO"

	response = requests.get(url).content
	df = pd.read_csv(io.StringIO(response.decode('utf-8'))) 
	#clean
	print('uncleaned data')
	print(df) 
	#df.to_csv('uncleaned.csv',  index = False)
	df = df.drop(['beat','location','case_number','end_date','geolocation',
		'geolocation_address','geolocation_city','geolocation_state',
		'geolocation_zip','incident_id','latitude','longitude','nibrs_code','offence_code','pra','sector','zip_code'], axis=1)
	print('\n\ncleaned data')
	print(df)
	df.to_csv('OUTPUT_APIname.csv',  index = False)


main()





		
