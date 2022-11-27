# Tub API

Tub is a platform where users can share their shower thoughts with one another because **Knowledge is Power**. This is the backend web API for this platform, and it's built with [Python](https://www.python.org) using [Flask](https://flask.palletsprojects.com).

**🌐 Live Link**: https://udacity-fsnd-capstone-jt.herokuapp.com

Database is hosted on Heroku Postgres.

## Motivation

The motivation for the project is based on the r/showerthoughts subreddit, where users share their pseudo-Eureka moments. Tub is meant to be a full platform that attempts to do the same. The API provides access to the database and allows to edit user details, add new showerthoughts, edit showerthoughts, add new users to the system as well as delete both user accounts and showerthoughts created. There is also a simple follower system available.

## Getting Started

### Set up your environment

#### Install Python

Follow the instructions to install the latest version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Enable a Virtual Environment

Working within a virtual environment enables a consistent dependency environment for Python projects. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### Install Dependencies

Once you have your virtual environment set up and running, install dependencies by running:

##### Key Dependencies

- **Flask**: Flask is a Python microframework that allows us to make HTTP requests and responses, and it provides the base layer for the API.
- **SQLAlchemy**: An ORM for interacting with the database using the class-based model pattern, eliminating much of the need for manual SQL queries.
- **Jose**: JOSE stands for JavaScript Object Signing and Encryption and there are various Python implementations. The one used in this project is [python-jose](https://pypi.org/project/python-jose/)

```bash
pip install -r requirements.txt
```

This will install all the required packages in the `requirements.txt` file.

#### Environment variables

Run `setup.sh` to export important environment variables to the terminal.

```bash
source setup.sh
```

> **Note** - It is recommended to have Postgres installed for local development especially for tests. You can however use the Heroku database if you wish. To do so, add its URI to your `setup.sh` file.

#### Run the server

To run the server, use the `python` utility to run `app.py`.

```bash
python app.py
```

> **Tip** - **Unable to run on port 3001?** You can tweak the value of `PORT` in `setup.sh` to an available port of your choice.

#### Run tests

Although you can also run tests using the Postman collection, unit testing is available via the `unittest` library. To run the tests, ensure you have exported the environment variables to the terminal and then run the `tests.py` file.

- Export variables

```bash
source setup.sh
```

- Run tests

```bash
python tests.py
```

## Authentication Details

**Live App URL**: https://udacity-fsnd-capstone-jt.herokuapp.com/

**The Auth0 Login URL**: https://dev-sw154ywt.us.auth0.com/authorize?audience=tub-api&response_type=token&client_id=nMocQbvsYw7bpOugCsUqkN0L3rlKmHQP&redirect_uri=https://127.0.0.1:8080/user/login

**Permissions**:

- `add:user`: Add a user to the system
- `get:user`: Get a single user's or all users' details
- `edit:user`: Edit a user's details
- `delete:user`: Delete a user from the system
- `add:showerthought`: Add a showerthought to the system under a user's name
- `delete:showerthought`: Delete a showerthought from the system

**Roles**:

- **Admin**: Has higher but still limited control. Can delete users and showerthoughts and can get a particular user's details but cannot add or edit a user's data.
  - `delete:user`
  - `delete:showerthought`
  - `get:user`
- **Regular**: The regular user role. Can get user details, add a user, edit user details, add a showerthought and delete a showerthought. Cannot delete a user account.
  - `get:user`
  - `add:user`
  - `edit:user`
  - `add:showerthought`
  - `delete:showerthought`

## Testing endpoints with Postman

The easiest way to test endpoints is to use Postman. A Postman collection has been added to the repository to make this easy to work with. To use the Postman collection, import the Postman collection from the file `fsnd-capstone-test.postman_collection` which will create a collection called `fsnd-capstone-test` inside the Postman app.
To run the collection and all associated tests, click on the three dots on the `fsnd-capstone-test` tab and click `Run collection`. This will run all tests for the endpoints in the collection.

> **Tip** - To reset the database, hit the `/db` endpoint with a DELETE request using admin credentials.

To test the endpoints yourself, sign in using the Auth0 Login URL provided above. Two accounts representing the available roles have been pre-created to make this easier.

### Admin: <br/>

**Email**: ufcadmin@hotmail.red <br/>
**Password**: Admin@123
**Sample Token**:

```json
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2QmlWUXJXZ1RSWGFmcDNKZDQ5MyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zdzE1NHl3dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM1YmY3NDdhOTgxMjlkMWUxNzQ3Y2QwIiwiYXVkIjoidHViLWFwaSIsImlhdCI6MTY2OTU4NTM3OCwiZXhwIjoxNjY5NjIxMzc4LCJhenAiOiJuTW9jUWJ2c1l3N2JwT3VnQ3NVcWtOMEwzcmxLbUhRUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnNob3dlcnRob3VnaHQiLCJkZWxldGU6dXNlciIsImdldDp1c2VyIl19.YwXAy-q4bbD99vLEquUyuedD3_UEiuJ97XZ7z0teomhP8BlXJkVm9d-v334kt0HO1rsQapnQve-KJhKSufENxyllmJWoIpQggyJKURqsqAXZO2bMH0DRG77XsrxGQXDBLsYN6VFlXhCamUNtN2VP5lBefomL4VCBHRIFQFLxkswLOEsibQ2VQV5Iu9LO7sExAZTiPmRgbN5Un-DB6kbLHgMcSmYlh2ila-ddE2N4HClG9WxaKzbWhYU_IbFbq-d2Go2g0Hst03mpPlwNf-BZRaaiCkdTyYUqAldmW0LsDTH7dOlUiEZYrFZ--oBsEm57-vq6Ck6HQ4WxwcLJhBb2_g
```

### Regular <br/>

**Email**: ufcregular@test130.com <br/>
**Password**: Regular@123

```json
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkR2QmlWUXJXZ1RSWGFmcDNKZDQ5MyJ9.eyJpc3MiOiJodHRwczovL2Rldi1zdzE1NHl3dC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjM2YTg4YTU1M2ZlYzI3MjVkYWE4MjMyIiwiYXVkIjoidHViLWFwaSIsImlhdCI6MTY2OTU4NTQ3MywiZXhwIjoxNjY5NjIxNDczLCJhenAiOiJuTW9jUWJ2c1l3N2JwT3VnQ3NVcWtOMEwzcmxLbUhRUCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOnNob3dlcnRob3VnaHQiLCJhZGQ6dXNlciIsImRlbGV0ZTpzaG93ZXJ0aG91Z2h0IiwiZWRpdDpzaG93ZXJ0aG91Z2h0IiwiZ2V0OnVzZXIiXX0.n7oD12Sfu-XUa7aZcxMB1LcQpWxvFE6cStpEG1-erRMBvQnMy7Ly1tI5Bwi1PbDDrP0hzhovLlK5J0BvO_4Z6DLRLYj_HIqPZAGznZh5eg_mMKFPsRrfGvl8Zchsu52plzJNvsz4aWFJ0HG5mt40RMl-fnYDvpeOLL05f2WAY-ryl5_psYyAU1n1m6awp8gPn9PzAqCHY77j5BNnE6TaflHkPAZzIHqPi2vjiloMkQORMtlAHH-ySvORNdkvUR59SopVm5n0A2xQQ3B2mV7Y-E65A2CQGknekPCx7NPKP1SgE7q9tpuDa7wUjCT6txsXb_HL7NgtYtNqBklETAMYLg
```

## Deploying to Heroku

### Requirements

- An Heroku account. Create one [here](https://signup.heroku.com/) if you don't have one.
- The [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli).

### Steps

- Create a new Heroku app and give it a name.

```bash
heroku create [my-app-name] --buildpack heroku/python
```

- Add a Heroku remote repo

```bash
git remote add heroku [heroku_remote_git_url]
```

- Add a Heroku Postgres addon

```bash
heroku addons:create heroku-postgresql:hobby-dev --app [my-app-name]
```

- Configure the app and copy the generated environment variables. Add the generated environment variables to your local environment. You will likely get a DATABASE_URL. Replace the one in your `setup.sh` with that one.

```bash
heroku config --app [my-app-name]
```

- When you make a new commit, push it to the remote Heroku repo.

```bash
git push heroku master
```

Alternatively, you can set up a GitHub pipeline from inside `Deploy > Deployment` from the app's dashboard.

## Endpoint Reference

`GET '/all'`

#### Fetches all showerthoughts

- **Returns**: An array of objects with each object representing a showerthought with its content, id and the user name of its creator.
- Permissions: None

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
      "followers": ["johncena00034", "messi_10"],
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
  "followers": ["johncena00034", "messi_10"],
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
