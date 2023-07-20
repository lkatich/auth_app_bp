# User authorization boiler-plate flask app

This is a boilerplate app written on Flask - solution that provides a foundation for implementing user authentication and authorization features in web applications. 
The app includes pre-built functionality for user creation, login, logout, and some other basic users operation CRUD (get all users, update user, delete user)

With this app as a starting point, developers can easily customize and extend the functionality to meet the specific needs of their web applications. They can add additional features, integrate with other systems or APIs, and adapt the user interface to match the branding and design requirements.

App uses docker images of postgres (to store users data) and redis (to store users tokens for authorization) which is suitable for testing but surely need to be checnges to the real services in prod.
It also uses sqlalchemy with alembic to have a clearest work with DB migrations

<h4>Preconditions needed:</h4>

Python3.10 or newer

Docker



To start working with the app, run docker-compose to start the services:

```
docker-compose up --build
```

To start testing the app - create first user by send POST request to http://127.0.0.1:5001/api/v1/rbac/user with the payload like:

{"email": "test@bp.com", "username": "test", "password": "Start123"}

(no token verification is added to that endpoint, so the users may be created easily, for real work this endpoint should also go with verification)

Then use that (or further created) user email/password to login to the app (http://localhost:5001/api/v1/rbac/auth) and get the token, like:

{
    "user_uuid": "4145ae94-ec79-4a12-9e8f-51aeb02ea953",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2ODk4NjM1NjUsImV4cCI6MTY4OTg2NzE2NSwidXVpZCI6IjQxNDVhZTk0LWVjNzktNGExMi05ZThmLTUxYWViMDJlYTk1MyJ9.5ddkkp2ogE3Kaw-o5axUF-1WpKjZvfqY7aTj5SH0Pe8"
}

Use this token to work with other user's CRUD and to logout






