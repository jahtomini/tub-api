# Tub API
Tub is a platform where users can share their shower thoughts with one another because __Knowledge is Power__. This is the backend web API for this platform, and it's built with [Python](https://www.python.org) using [Flask](https://flask.palletsprojects.com).

__🌐 Live Link__: https://udacity-fsnd-capstone-jt.herokuapp.com

Database is hosted on Heroku Postgres.

## Getting Started
### Set up your environment

#### Install Python
Follow the instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Enable a Virtual Environment

Working within a virtual environment enables a consistent dependency environment for Python projects. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Install Dependencies

Once you have your virtual environment set up and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all the required packages in the `requirements.txt` file.

#### Environment variables
Run `setup.sh` to export important environment variables to the terminal.

```bash
source setup.sh
```

#### Run the server
To run the server, use the `python` utility to run `app.py`.
```bash
python app.py
```

> **Tip** - __Unable to run on port 3001?__ You can tweak the value of `PORT` in `setup.sh` to an available port of your choice.


## Endpoint Reference
`GET '/all'`

#### Fetches all showerthoughts
- **Returns**: An array of objects with each object representing a showerthought with its content, id and the user name of its creator.
- Permissions: None
- 
```json
[
    {
        "content": "Nighttime is the natural state of the universe and daytime is only caused by a nearby, radiating ball of flame.",
        "creator": "johncena00034",
        "id": 1
    },
    {
        "content": "A bird can fly but a fly cannot bird.",
        "creator": "okayletsgooo",
        "id": 2
    }
]
```

`GET '/random'`
#### Fetches a random showerthought
- **Returns**: An object containing a single showerthought with its content, creator and unique id.
- Permissions: None
```json
{
    "random": {
        "content": "Nighttime is the natural state of the universe and daytime is only caused by a nearby, radiating ball of flame.",
        "creator": "johncena00034",
        "id": 1
    }
}
```

`GET '/users'`
#### Fetches all users
- Permissions: ['get:user']
- **Returns**: An array of objects with each object representing a user with an array showing all followers if any exist as well as an object representing the user's data, containing their id and username.
```json
{
    "users": [
        {
            "followers": null,
            "user": {
                "id": 1,
                "name": "johncena00034"
            }
        },
        {
            "followers": null,
            "user": {
                "id": 2,
                "name": "okayletsgooo"
            }
        },
        {
            "followers": [
                "johncena00034",
                "messi_10"
            ],
            "user": {
                "id": 3,
                "name": "carefulAstronaut"
            }
        },
        {
            "followers": null,
            "user": {
                "id": 4,
                "name": "yilongma"
            }
        },
        {
            "followers": null,
            "user": {
                "id": 5,
                "name": "messi_10"
            }
        }
    ]
}
```

`GET '/users/<user_id>'`
#### Get individual user
- Permissions: ['get:user']
- - **Returns**: An object representing a user containing their unique id, username and an array of showerthoughts.
```json
{
    "id": 1,
    "name": "johncena00034",
    "shower_thoughts": [
        {
            "content": "Nighttime is the natural state of the universe and daytime is only caused by a nearby, radiating ball of flame.",
            "creator": "johncena00034",
            "id": 1
        }
    ]
}
```

`GET '/users/<user_id>/followers'`
#### Get all of a user's followers
- Permissions: ['get:user']
- Returns an object indicating the status of the request, user id, username and an array of all followers. Returns `null` if none exist.
```json
{
    "followers": [
        "johncena00034",
        "messi_10"
    ],
    "success": true,
    "user_id": 3,
    "username": "carefulAstronaut"
}
```

`POST '/shower_thoughts'`
#### Add a new showerthought
- Permissions: ['add:showerthought]
- Request body format:
```
{
    "creator": <username(string)>,
    "content": <showerthought content (string)>
}
```
- Returns a status message indicating the request was successful as well as the showerthought content and creator.
```json
{
    "content": "Smart phones are probably responsible for reducing graffiti in public toilets.",
    "creator": "yilongma",
    "message": "New showerthought created",
    "status": 201,
    "success": true
}
```

`PATCH '/shower_thoughts'`
#### Edit a showerthought
- Permissions: ['edit:showerthought]
- Request body format:
```
{
    "content": <new showerthought content (string)>
}
```
- Returns a status message indicating the request was successful as well as the creator and new showerthought content.
```json
{
    "by": "johncena00034",
    "content": "Nighttime is the natural state of the universe and daytime is only caused by a nearby, radiating ball of flame.",
    "success": true
}
```

<br />

`POST '/users'`
#### Add a new user
- Permissions: ['add:user]
- Request body format:
```
{
    "name": <username (string)>
}
```
- Returns a status message indicating the request was successful as well as the user id and username. 
```json
{
    "message": "New user created",
    "status": 201,
    "success": true,
    "user_id": 6,
    "user_name": "youveHeardAboutMe"
}
```

<br />

`DELETE '/users/<user_id>'`
#### Delete a user
- Permissions: ['delete:user]
- Returns a status message, the deleted user's id and their username.
```json
{
    "message": "User account successfully deleted.",
    "status": 200,
    "user_id": 1,
    "user_name": "johncena00034"
}
```

`DELETE '/shower_thoughts/<shower_thought_id>'`
#### Delete a showerthought
- Permissions: ['delete:showerthought]
- Returns the deleted showerthought's id and a status message.
```json
{
    "id": 1,
    "message": "Showerthought successfully deleted."
}
```


## Authentication Details

__Live App URL__: https://udacity-fsnd-capstone-jt.herokuapp.com/

__The Auth0 URL__: https://dev-sw154ywt.us.auth0.com/authorize?audience=tub-api&response_type=token&client_id=nMocQbvsYw7bpOugCsUqkN0L3rlKmHQP&redirect_uri=https://127.0.0.1:8080/user/login

__Permissions__: 
- `add:user`: Add a user to the system
- `get:user`: Get a single user's or all users' details
- `edit:user`: Edit a user's details
- `delete:user`: Delete a user from the system
- `add:showerthought`: Add a showerthought to the system under a user's name
- `delete:showerthought`: Delete a showerthought from the system

__Roles__:
- __Admin__: Has higher but still limited control. Can delete users and showerthoughts and can get a particular user's details but cannot add or edit a user's data.
  - `delete:user`
  - `delete:showerthought`
  - `get:user`
- __Regular__: The regular user role. Can get user details, add a user, edit user details, add a showerthought and delete a showerthought. Cannot delete a user account.
  - `get:user`
  - `add:user`
  - `edit:user`
  - `add:showerthought`
  - `delete:showerthought`

## Testing endpoints
The easiest way to test endpoints is to use Postman. A Postman collection has been added to the repository to make this easy to work with. To use the Postman collection, import the Postman collection from the file `fsnd-capstone-test.postman_collection` which will create a collection called `fsnd-capstone-test` inside the Postman app.
To run the collection and all associated tests, click on the three dots on the `fsnd-capstone-test` tab and click `Run collection`. This will run all tests for the endpoints in the collection. The JWTs for both roles have been set up already in the collection but to be able to test otherwise, these are the tokens:

Admin role: 
```json
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2QmlWUXJXZ1RSWGFmcDNKZDQ5MyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zdzE1NHl3dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM1YmY3NDdhOTgxMjlkMWUxNzQ3Y2QwIiwiYXVkIjoidHViLWFwaSIsImlhdCI6MTY2OTQ3NTY2MSwiZXhwIjoxNjY5NTExNjYxLCJhenAiOiJuTW9jUWJ2c1l3N2JwT3VnQ3NVcWtOMEwzcmxLbUhRUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnNob3dlcnRob3VnaHQiLCJkZWxldGU6dXNlciIsImdldDp1c2VyIl19.mI533kON016SVy9qhKZHV67J_xJ_gsO_SKQK8nl_AFe5cIek4rlVOaTQ_723CmG-BXWPhXG_GOqScgbxEs5C_m5bXH9Iu6VZ7SRthumJrJCGm8liUCNCqe3UbvP6beMVrZl_FD6OZZ2amhSJJjtylEERPxn8g1CTHTbOc5iJsPKRl3Hw2RHNhC59rfG6WCGpOAzj2GxkGZ4cIl0_PqPFuDQKCcQgdfsE6lcNUZYMMumeXMwxihoVO5U70hJRLeho3PxkYtgKDHtDgtY7LChA6HJvns0nSPJpg2H7MTy_dDLCf3efCh1W6e1RY-lrpFaDCWn22BHckt02mHYMLBNWFA
```

Regular role:
```json
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2QmlWUXJXZ1RSWGFmcDNKZDQ5MyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zdzE1NHl3dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM2YTg4YTU1M2ZlYzI3MjVkYWE4MjMyIiwiYXVkIjoidHViLWFwaSIsImlhdCI6MTY2OTQ3NTc3OCwiZXhwIjoxNjY5NTExNzc4LCJhenAiOiJuTW9jUWJ2c1l3N2JwT3VnQ3NVcWtOMEwzcmxLbUhRUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOnNob3dlcnRob3VnaHQiLCJhZGQ6dXNlciIsImRlbGV0ZTpzaG93ZXJ0aG91Z2h0IiwiZWRpdDp1c2VyIiwiZ2V0OnVzZXIiXX0.DdehD19aV_11b-I4D55CoocEdCceHlc2--EdGb-yx6_BBF1ZzftSlvl2c6kdkGws7_6cyNq4CXoxDWByMI5VBAUw-M2qc7GnpOOJMru0EzSqhoNpt2hrF2IgGf6bM6Uak6vWarfO2iAXFz0-zSGu96IiUKMozZ5w1FFkL_DOhDN_8ZHwRptl6K2VjI1syiFwjx_o7ClhCNYpk3AoanTC4sfieDT2mSXj4dDdZ0KIQIXsUimN1PnMoePAu8s7zC5ahuH_WNboZvR1bSFsllWjEAEtYLJ2bO-9SDBBSpPRz_CWkefSOpC168YyudpeBTHQj8n94QTmfC3khMds8Ov-JA
```

> **Tip** - To reset the database, hit the `/db` endpoint with a DELETE request using admin credentials.
