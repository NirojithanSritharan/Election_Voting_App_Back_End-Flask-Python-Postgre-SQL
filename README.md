# Election_Voting_App_Back_End-Flask-Python-PostgreSql
A web application development (only - back-end) having two basic REST APIs to manage election process by add votes to candidate and get the votes count of each candidate.

#
## Features ( Details about the REST APIs ) 
### POST api/vote

- This API is used to increase the candidate vote count by one with a return success response.

- request body:
    &emsp; type : JSON \
    &emsp; &emsp; &emsp; &emsp; &emsp; &emsp; schems : {"candidate" : \<string\>} 


### GET api/candidate/<candidate_id>/count
- This API is used to calculate the total vote count fo the candidate with the given candidate_id and display the count in the console with a success response.
#

## Built With
Server : Python + Flask \
Database : PostgreSql DB
#

## Requirments
* Python 3.9+ (Version 3.9.7 is used to develop the application)
* Python pip 
* Postgres SQL
#

## Installation

* Install python & pip.
* Setup the PostgreSql database.
* In the src/init_app.py file change the User_Name, Password, Host & Database_name in the database_url or update the database_url with yours.
* On the terminal cd into app folder.
* Run the following command to install required modules.
```
pip install -r requirements.txt 
``` 
* To create the table in the database from the model run the command; 
```
python build_database.py
```
* Run the following command in the terminal to run the app.
```
python app.py 
```
#
## License
[MIT](https://choosealicense.com/licenses/mit/)
