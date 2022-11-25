# Tub API
Tub is a platform where users can share their shower thoughts with one another because __Knowledge is Power__. This is the backend web API for this platform, and it's built with [Python](https://www.python.org) using [Flask](https://flask.palletsprojects.com).

__🌐 Live Link__: https://udacity-fsnd-capstone-jt.herokuapp.com

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

>__Unable to run on port 3001?__ You can tweak the value of `PORT` in `setup.sh` to an available port of your choice.


## Endpoint Reference
`GET '/users'`

- Fetches all users
- **Request Arguments**: None
- **Returns**: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
