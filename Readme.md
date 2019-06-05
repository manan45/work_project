####**Rest API's using Python(Flask) and  Mysql Databse**


To run the application on local computer:
1) install virtualenv using this command
    `virtualenv venv -p python3`
2) clone the github repository 
3) activate the virtualenv using 
    `source venv/bin/activate`

4) install the requirements file using
    `pip install -r requirements.txt`

5) for setting up database change the database values in database.py file then run

    `flask db init`

    `flask db migrate`

    `flask db upgrade`

6) run `python run.py`
7) to add to database open http client and enter the url
    `http://localhost:8081/api/add_users`



****API URL's****
1) `/api/users - GET `- To list the users* 
    a) Response with HTTP status code 200 on success



    {
        "first_name": "James",
        "last_name": "Butt",
        "company_name": "Benton, John B Jr",
        "city": "New Orleans",
        "state": "LA",
        "zip": 70116,
        "email": "jbutt@gmail.com",
        "web": "http://www.bentonjohnbjr.com",
        "age": 70
    },
    {
        "first_name": "Josephine",
        "last_name": "Darakjy",
        "company_name": "Chanay, Jeffrey A Esq",
        "city": "Brighton",
        "state": "MI",
        "zip": 48116,
        "email": "josephine_darakjy@darakjy.org",
        "web": "http://www.chanayjeffreyaesq.com",
        "age": 48
    }

b) Also, supports some query parameters:-
    `offset` - a number for pagination
    `limit` - no. of items to be returned, default limit is 5
    `name` - search user by name as a substring in First Name or Last Name (Note, use substring matching algorithm/pattern to match the name)
    `Sort` - name of attribute, the items to be sorted. By default it returns items in ascending order if  this parameter exist, and if the value of parameter is prefixed with ‘-’ character, then it should return items in descending order
    Sample query endpoint:- `/api/users?page=1&limit=10&name=James&sort=-age`
    This endpoint should return list of 10 users whose first name or last name contains substring given name and sort the users by age in descending order of page 1.


2) `/api/users - POST` - To create a new user
    Request Payload should be like in json format :-


    {
        "first_name": "Josephine",
        "last_name": "Darakjy",
        "company_name": "Chanay, Jeffrey A Esq",
        "city": "Brighton",
        "state": "MI",
        "zip": 48116,
        "email": "josephine_darakjy@darakjy.org",
        "web": "http://www.chanayjeffreyaesq.com",
        "age": 48
    }

 Response with HTTP status code 201 on success
 
    {
        "first_name": "Josephine",
        "last_name": "Darakjy",
        "company_name": "Chanay, Jeffrey A Esq",
        "city": "Brighton",
        "state": "MI",
        "zip": 48116,
        "email": "josephine_darakjy@darakjy.org",
        "web": "http://www.chanayjeffreyaesq.com",
        "age": 48
    }
    
 This endpoint will create a new user inside the database

3)`/api/users/<user_id> - GET`- To get the details of a user
    Here {user_id} will be the id of the user in path parameter 
    Response with HTTP status code 200 on success
	
    {
    "id": 1,
    "first_name": "James",
    "last_name": "Butt",
    "company_name": "Benton, John B Jr",
    "city": "New Orleans",
    "state": "LA",
    "zip": 70116,
    "email": "jbutt@gmail.com",
    "web": "http://www.bentonjohnbjr.com",
    "age": 70
    }


4)`/api/users/<user_id> - PUT `- To update the details of a user
Here {id} will be the id of the user in path parameter 

    {
    "first_name": "Josephine",
    "last_name": "Darakjy",
    "age": 48
    }

Response with HTTP status code 200 on success
	
	
	{
            "first_name": "Joesph",
            "last_name": "Darakjy",
            "company_name": "A R Packaging",
            "city": "Berkeley",
            "state": "CA",
            "zip": 94710,
            "email": "joesph_degonia@degonia.org",
            "web": "http://www.arpackaging.com",
            "age": 48
        }


5) `/api/users/<user_id> - DELETE` - To delete the user
    Here <user_id> will be the id of the user in path parameter 
    Response with HTTP status code 200 on success
    
    
    {
    "message": "User Deleted Successfully"
    }
	


