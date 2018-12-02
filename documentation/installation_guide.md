# Installing the application locally

*The user is expected to be familiar with the command line. This guide is for unix systems using bash.*

## Prerequisites

Software that should be installed on the system:

- python3, which includes *venv* and *pip*
- sqlite3

## Installation

1. Clone the project into a directory of your choosing

```
$ git clone git@github.com:stadibo/friseurManager.git
```

The project can also be downloaded as a .ZIP-file from https://github.com/stadibo/friseurManager and extracted into a directory

2. Create a virtual environment and activate it with the following commands
```
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install dependencies defined in requirements.txt file

```
$ pip install -r requirements.txt
```

4. You can now run the application with the command
```
$ python3 run.py
```

5. Navigate to the address http://localhost:5000/ in a browser of your choosing

6. The application can now be used in the local environment