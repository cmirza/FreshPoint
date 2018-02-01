FreshPoint
=================

### Model
- **~~Clean up JSON data~~**
	- ~~Go through captured JSON data and clean syntax~~
- **~~Model Structure~~**
	- ~~Vegetable Table: Name (string), Type (string), Image (string), Desc (string)~~
	- ~~States Table: Name (string)~~
	- ~~Seasons Table: Vegetable ID, State ID, seasons (string)~~
- **~~Import JSON data into Model~~**
	- ~~Create State table with all 50 states~~
	- ~~Create custom management commands for importing JSON~~
	    - ~~Iterate through JSON, creating an entry for each vegetable in Vegetable table~~
	    - ~~Iterate through JSON, creating entry for each season and ID for each vegetable and state in Seasons table~~
- **~~Verify Model is correct~~**
	- ~~Check if responses from the database are consistent with data in JSON file~~

### View
- **Results Page**
	- ~~Get user zip code from text box~~
	- ~~Pass zip code to Google GeoCode API~~
		- ~~https://developers.google.com/maps/documentation/geocoding/start~~
	- ~~Parse JSON response to get state~~
    - Find vegetables for user
    	- Filter Seasons table by user's state
    	- Get Season ID
    		- Get string of current month
    			- if day < ( days in month / 2 )
    				- append 'early'
    			- if day > ( days in month / 2 )
    				- append 'late'
    		- Filter Season ID dict to get current Season ID
    	- Filter results by Season ID
    - Calculate months left until out of season(?)
	- Create context object for 'name', 'type', 'image' and 'description'
	    - Create URL links to detail with 'veg id' and 'state id'
	- Render results template with context

### Template
- **Landing Page**
	- Header
	- Input box for zip code
	- Footer
- **Results Page**
	- Header
	- Input box for zip code
	- Google GeoChart highlighting user's state
	- Body wrapper
   	- Multiple DIVs inside flex box
	- Footer

### Enhancements
- **Apply Material-UI CSS framework**
- **Use PostgreSQL for database**
- **Use React.js to create single page app**
- **Management Mode**
	- Add items, update seasons

## Deployment
- **AWS Beanstalk**




### NOTES

#### AJAX

- JsonResponse in Django 
	returns json dict
