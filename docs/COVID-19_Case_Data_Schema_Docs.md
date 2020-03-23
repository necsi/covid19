**Target Schema - Elastic csv


:-:|:--|:--|:--|:--|:--
**1**|**Field_OrdinalPosition**|**Field_Name**|**Field_Type**|**Sample**|**Comments**
**2**|1|date|Date|2/25/2020|NOT datetime - probably best to have a standard date string format ("YYYY-MM-DD", e.g.)
**3**|2|city|Text|Innsbruck| 
**4**|3|province|Text|Tyrol| 
**5**|4|country|Text|Austria| 
**6**|5|lat/long|Geocode coord|47.25,11.3333| 
**7**|6|confirmed|Integer|2|Total Confirmed Cases
**8**|7|recovered|Integer| |Total Recovered Cases
**9**|8|dead|Integer| |Total Cases in which Patient died
**10**|9|daily_diff_confirm|Integer|2|Daily Change Confirmed Cases
**11**|10|daily_diff_recover|Integer| |Daily Change Recovered Cases
**12**|11|daily_diff_dead|Integer| |Daily Change Death Cases
**13**|12|admin_level|Text|0| 
**14**|13|source|Text|JHU| 

