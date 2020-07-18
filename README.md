# A quote sharing service using Django Rest Framework

The following project was a step to get fimiliar with Djano Rest Framework. In the application, an api is provided for the user to register themselves using their: 
- first name
- last name
- username
- email
- password

There are validation set for username, email and password. Like, the username and email has to be unique and password must be of minimum 8 letters, it cannot be a common password, it should not also be ralated to the attributes of the user and cannot be entirely numeric. The user login using username and password.  

### About the app

  - The authentication in the application is maintained using JWT, json web token

The user will be provided with the get access token and refresh token as soon as they login using their username and password. Everytime they want to use the application they can they are required to be authenticated. Having the access token in request header will do as:

```
Authorization Bearer <Access Token>
```
If the access token has expired a new access token can regained using the refresh token. 

- A user can see all the quotes posted on the application along with their authors.
- A user can also query/filter quotes using id, username of the author or by text that may contain in the quote
- An author can also update their quote or delete it.
