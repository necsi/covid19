**Target Schema - Elastic csv**


|**Field_OrdinalPosition**|**Field_Name**|**Field_Type**|**Sample**|**Comments** |
| --- | --- | --- | --- | --- |
**1**|	date|Date|2/25/2020|NOT datetime - probably best to have a standard date string format ("YYYY-MM-DD", e.g.)    
**2**|	city|	Text|	Innsbruck|	  
**3**| province|	Text|	Tyrol|	  
**4**|	country|	Text|	Austria|	   
**5**|	lat/long|	Geocode coord|	47.25,11.3333|	  
**6**|	confirmed|	Integer|	2|	Total Confirmed Cases   
**7**|	recovered|	Integer|	1|	Total Recovered Cases
**8**|	dead|	Integer|	1|	Total Cases in which Patient died  
**9**|	daily_diff_confirm|	Integer|	2|	Daily Change Confirmed Cases  
**10**|	daily_diff_recover|	Integer|	 0| Daily Change Recovered Cases  
**11**|	daily_diff_dead|	Integer|	1| Daily Change Death Cases  
**12**|	admin_level	|Text|	0|	  
**13**|	source| Text| JHU| 
