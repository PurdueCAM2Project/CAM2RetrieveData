##Purpose
This folder contains used parsing scripts ONLY. Meaning they work, or at least used to work, and are all on the database. This folder exist because scripts might not run in the future due various reason (eg. changes on the website), but we know they are on the database. And we do not have to check on the database / discard / move them around even if they fail to run in the future.

####General Rule : <br>
* This folder contains all 7 continents and a cross continent (Worldwide) folder.<br> 
* Each website including traffic camera should be in the correct region folder. If websites is based on US, a parser program should go to the "US" folder. 
* If there are multiple scripts for a country, create a sub folder in the directory.
* Each folder has sub folders for countries in that region. 
* There is also a traffic_cameras & non_traffic_cameras folder for programs that parse cameras from multiple countries within that region.

##Naming Conventions
####Filename Rule: <br>
* File name must be related to the website name. 
* If it is from HongKong, China, file name should be Hongkong_CN.py in "Asia" folder. 
* File name MUST always end with `.py`
	
####Output Filename Rule:
* Output filename MUST always start with 'list_' followed by the name of the parsing script (without '.py') and should have file extension '.txt' If the output filename does not match this convention, the testing script will not work. <br> eg. list_Hongkong_CN.txt
* each script MUST output only ONE .txt file

####Traffic camera filename Rule :
* In the US:<br>
State wide camera: `<state_abbreviation>.py` eg: NY.py <br>
County or city wide: `<State>_<City>_<Source>.py` eg: MS_Lafayette.py, NY_NewYorkCity_dotsignals.py
	
* Not US: <br>
`<City><Country>_<Source>.py` eg: Hongkong_CN.py, Barcelona_ES.py
