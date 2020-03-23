## [I. Target Schema](#target-schema---elastic-csv)


## [II. Data Sources](#data-sources) - with schemas

  [Detailed Data Google Sheet](#cssegisanddata---covid-19-johns-hopkins)
 
  [CSSE GIS](#cssegisanddata---covid-19-johns-hopkins)


# I. Target Schema - Elastic csv


|**Field_OrdinalPosition**|**Field_Name**|**Field_Type**|**Sample**|**Comments** |
| --- | --- | --- | --- | --- |
|**1**|	date|Date|2/25/2020|NOT datetime - probably best to have a standard date string format ("YYYY-MM-DD", e.g.)   |
|**2**|	city|	Text|	Innsbruck|	  |
|**3**| province|	Text|	Tyrol|	  |
|**4**|	country|	Text|	Austria|	 |  
|**5**|	lat/long|	Geocode coord|	47.25,11.3333|	  |
|**6**|	confirmed|	Integer|	2|	Total Confirmed Cases |  
|**7**|	recovered|	Integer|	1|	Total Recovered Cases |
|**8**|	dead|	Integer|	1|	Total Cases in which Patient died |  
|**9**|	daily_diff_confirm|	Integer|	2|	Daily Change Confirmed Cases  | 
|**10**|	daily_diff_recover|	Integer|	 0| Daily Change Recovered Cases | 
|**11**|	daily_diff_dead|	Integer|	1| Daily Change Death Cases  |
|**12**|	admin_level	|Text|	0|	 | | 
|**13**|	source| Text| JHU| | |


<br />



# II. Data Sources


## A. Collaborative Google Sheet [Detailed Data](https://docs.google.com/spreadsheets/d/1-YNneqVqTGy2Uzp_0pPNBezhxyEp6M_a2A2GI1MTxx0/edit#gid=1872189130)

|**Field_OrdinalPosition**|**Field_Name**|**Field_Type**|**Sample**|**Comments**| 
| --- | --- | --- | --- | --- |
|1|Date|Date|2020-1-31| 
|2|Total|Integer|20|Total Cases
|3|New|Integer|5|New Daily Cases
|4|**Region**|Text|VDA| 
|5|**Country**|Text|Italy| 
|6|Total Death|Integer|3|Total Deaths


<br />

## B. CSSEGISandData - COVID-19 (Johns Hopkins)

from **csse_covid_19_time_series/** folder:

https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv

https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv

|**Field_OrdinalPosition**|**Field_Name**|**Field_Type**|**Sample**|**Comments**| 
| --- | --- | --- | --- | --- |
|1 | Province/State	| Text |	Anhui 	
|2 |	Country/Region | Text	|	China
|3 |	Lat	|	Decimal |	31.8257 	
|4 |	Long |Decimal |	117.2264	
|5 |	1/22/20	| Date	|	 1
|6 |	1/23/20	| Date	|	  9
|7 |	1/24/20	| Date	|	 15
|8 |	1/25/20	| Date	|	 39


