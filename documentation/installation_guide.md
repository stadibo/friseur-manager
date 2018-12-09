# Installing the application locally

*The user is expected to be familiar with the command line. This guide is for unix systems using bash.*

## Prerequisites

Software that should be installed on the system:

- python3, which includes *venv* and *pip*
- sqlite3

## Installation locally

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

6. Click on the register button in the top right corner. The first user to be created is assigned to the __admin__ role.

7. The application can now be used in the local environment

# Intallation onto heroku.com

*When cloning the project from github the requirements.txt file and definitions in the source code should be up to date. If dependencies are added using pip one must remember to run the following command in the root folder for the application before continuing:*
```
$ pip freeze | grep -v pkg-resources > requirements.txt
```
**Step 1:** Clone and install the project locally using the above instructions

**Step 2: ** Install the Heroku command line interface (Heroku CLI)

Linux:

```
$ sudo snap install heroku --classic
```

MacOS:

```
$ brew install heroku/brew/heroku
```

Or using other instructions at https://devcenter.heroku.com/articles/heroku-cli

**Step 3:** Login to heroku (Create an account if you do not have one)

```
$ heroku login
```

**Step 4:** Navigate to the directory in which you installed the project
*Replace directoryName with the path to your directory*
```
$ cd ~/directoryName
```

**Step 5:** Create a heroku project
*Replace appName with a name by which the project shall be created*
```
$ heroku create appName
```

**Step 6:** Add information about Heroku to local version control and push the project to Heroku
```
$ git remote add heroku
$ git add .
$ git commit -m "init heroku"
$ git push heroku master
```
The project should now be running on Heroku

**Step 7:** Configure a PostgreSQL database on Heroku for persistant storage
```
$ heroku config:set HEROKU=1
$ heroku addons:add heroku-postgresql:hobby-dev
```
There is now a working database for the application. It can be accessed from the Heroku CLI with command:
```
$ heroku pg:psql
```
