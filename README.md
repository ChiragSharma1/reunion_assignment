
# Reunion Assignment


## Setting up the project

```
# Download and install Python 3.9

# Download and install Git.

# Fork the Repository.

# Clone the repository to your local machine $ https://github.com/<your-name-here>/reunion_assignment.git

# Change directory to $ cd reunion

# pip install -r requirements.txt

#CREATING DATABASE POSTGRESS

# Open the PostgreSQL shell. You can find the PSQL Shell in the Start Menu.

# The shell will prompt you for Server, Database, Port, and Username details. You can set it to default by clicking on the Enter button in the keyboard without providing any value. Finally, the shell will prompt you for the Password.

You should provide the password that you used during the PostgreSQL installation. 

# Now lets create PostgreSQL Database

# CREATE DATABASE reunion;    \\ creating database with name reunion

# CREATE USER <yourname> WITH PASSWORD '<password>';

# ALTER ROLE <yourname> SET client_encoding TO 'utf8';
#ALTER ROLE <yourname> SET default_transaction_isolation TO 'read committed';
#ALTER ROLE <yourname> SET timezone TO 'UTC';

#GRANT ALL PRIVILEGES ON DATABASE reunion TO <yourname>;

# \c reunion

# now update Setting.py in  project - 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'helloworld',
        'USER': '<yourname>',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# python manage.py makemigrations

# python manage.py migrate

# python manage.py runserver


```

## Deployed version

Deployed Server Link - [Link](https://reunion-assignment-app.herokuapp.com/)

Postman collection is available [here](https://www.postman.com/chiragsharma1/workspace/my-workspace/collection/17585058-0af9e5a1-2772-4b7d-8609-c567c4116365)



## API Reference

##Authentication 

```http
url  - POST /api/authenticate
```
Request Body - 
```json
{
  "username":"UserName",
  "password":"password of user"
}
```

It will return a JWT token , you can user access token then for accessing other api's

I have created some Dummy user for testing purpose
Dummy User's credentials - 
username - tushar  | harsh | diya
password - Reunion@123  (same password for all)


**Note - Use this JWT assess token by putting it in header of following url's or in postman you can put in parents header so that all url's can access it at once**  

- POST /api/follow/{id} authenticated user would follow user with {id}

- POST /api/unfollow/{id} authenticated user would unfollow a user with {id}

- GET /api/user should authenticate the request and return the respective user profile.
    - RETURN: User Name, number of followers & followings.

- POST api/posts/ would add a new post created by the authenticated user.
    - Input: Title, Description
    - RETURN: Post-ID, Title, Description, Created Time(UTC).

- DELETE api/posts/{id} would delete post with {id} created by the authenticated user.

- POST /api/like/{id} would like the post with {id} by the authenticated user.

- POST /api/unlike/{id} would unlike the post with {id} by the authenticated user.

- POST /api/comment/{id} add comment for post with {id} by the authenticated user.
    - Input: Comment
    - Return: Comment-ID

- GET api/posts/{id} would return a single post with {id} populated with its number of likes and comments

- GET /api/all_posts would return all posts created by authenticated user sorted by post time.
    - RETURN: For each post return the following values
        - id: ID of the post
        - title: Title of the post
        - desc: Description of the post
        - created_at: Date and time when the post was created
        - comments: Array of comments, for the particular post
        - likes: Number of likes for the particular post


## Tech Stack Used

- **Django Rest Framework** for making api's
- **PostgreSQL** used as a Database

## Tools
- **Postman** for testing API's
