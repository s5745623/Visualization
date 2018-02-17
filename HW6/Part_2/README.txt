README

Dataset link: https://data.montgomerycountymd.gov/Public-Safety/Crime/icn6-v9z3

Information: 
			Dataset Identifier: yc8a-5df8
			Total Rows: 71497
			Source Domain: data.montgomerycountymd.gov
			Created: 3/24/2015, 7:42:50 PM
			Last Updated: 10/20/2017, 4:01:23 AM
			Category: Public Safety
			Attribution: Montgomery County, MD
			License: Public Domain
			Owner: MCG ESB Service
			Num. of Attributes: 26

Describtion: Montgomery county's raw crime data, organized by MCG ESB Service

How to use API: Go to the website, click the greyish API icon on the top right corner. Then chose the format you wish to get, copy the link. By clicking the API docs to see more information of how to use the API, adding '$$app_token=' at the end of the link just copyed enable the server to identified user, also '$limit=' let the user to limit the data wish to download.
I use the requests.get function to get the data, and put into pandas dataframe, then drop the unnecessary columns, finally save the dataframe to csv format.

GET link: https://data.montgomerycountymd.gov/resource/yc8a-5df8.csv?$limit=3&$$app_token=tX2XTxtf7mZd8F5eQ7enqtsPO

POST: uncleaned-
address_number	agency	beat	case_number	city	crimename1	crimename2	crimename3	date	district	end_date	geolocation	geolocation_address	geolocation_city	geolocation_state	geolocation_zip	incident_id	latitude	location	longitude	nibrs_code	offence_code	place	police_district_number	pra	sector	start_date	state	victims	zip_code
11100	MCPD	4L2	16061525	SILVER SPRING	Crime Against Property	Shoplifting	LARCENY - SHOPLIFTING	2016-11-30T17:47:10.000	WHEATON		POINT (-77.051635982809 39.037385878653)					201109736	39.03738588	11100  VEIRS MILL RD	-77.05163598	23C	2303	Retail - Mall	4D	321	L	2016-11-30T17:47:00.000	MD	1	20902
1500	RCPD	1B1	16040137	POTOMAC	Crime Against Property	Burglary/Breaking and Entering	BURGLARY - FORCED ENTRY-NONRESIDENTIAL	2016-08-08T10:34:10.000	ROCKVILLE	2016-08-08T10:00:00.000	POINT (-77.171839768997 39.062338023663)					201092733	39.06233802	1500  DUNSTER RD	-77.17183977	220	2203	Recreation Center	1D	227	B	2016-08-07T17:00:00.000	MD	1	20854
	GPD	6P3	16039786	GAITHERSBURG	Crime Against Society	Driving Under the Influence	DRIVING UNDER THE INFLUENCE LIQUOR	2016-08-06T04:05:31.000	MONTGOMERY VILLAGE		POINT (-77.19896 39.1413)					201092500	39.1413		-77.19896	90D	5404	Street - In vehicle	6D	431	P	2016-08-06T04:01:00.000	MD	1	20877
		
		cleaned-
address_number	agency	city	crimename1	crimename2	crimename3	date	district	place	police_district_number	start_date	state	victims
11100	MCPD	SILVER SPRING	Crime Against Property	Shoplifting	LARCENY - SHOPLIFTING	2016-11-30T17:47:10.000	WHEATON	Retail - Mall	4D	2016-11-30T17:47:00.000	MD	1
1500	RCPD	POTOMAC	Crime Against Property	Burglary/Breaking and Entering	BURGLARY - FORCED ENTRY-NONRESIDENTIAL	2016-08-08T10:34:10.000	ROCKVILLE	Recreation Center	1D	2016-08-07T17:00:00.000	MD	1
	GPD	GAITHERSBURG	Crime Against Society	Driving Under the Influence	DRIVING UNDER THE INFLUENCE LIQUOR	2016-08-06T04:05:31.000	MONTGOMERY VILLAGE	Street - In vehicle	6D	2016-08-06T04:01:00.000	MD	1