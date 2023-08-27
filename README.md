# TicTacToe

This code implements the BackEnd of a Tic-Tac-Toe application mainly using the Django rest framework
with a SQLite database.

## Contents

- [Set up](#set-up-the-environment)
- [Testing](#run-tests)
- [API](#api-specification)

## Set up the environment

The application has been built using [Docker](https://www.docker.com/) to ensure that it can be run
homogeneously in any machine. You will need to install Docker in your machine in order to run the 
project.

1. Clone the repository.
- `git clone https://github.com/ikerRAD/TicTacToe.git`
2. In the root repository of the project run the project using Docker. If it is
the first time running it add the `--build` flag to the command.
- `docker compose up [--build]`
3. Apply all the migrations to ensure that the application works properly.
- `docker compose exec web python manage.py makemigrations`
4. In case anything goes wrong set the environment down and up again.
- `docker compose down`
- `docker compose up [--build]`

The project should be running now in localhost. If you want to see the database you can use any
program to see what is inside the `db.sqlite3` file that has been generated.

## Run tests

If you want to run the tests of the project, execute the following command:

`docker compose exec web python manage.py test`

## API specification

Once the project is run, you can find a detailed API spec in the [following link](http://localhost:8000/)

### Request templates

#### Create user endpoint
- cURL: 
```
curl --location 'http://localhost:8000/users/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx' \
--data '{
    "username":<username>,
    "password":<password>
}'
```
- URL:
`http://localhost:8000/users/`

#### Login endpoint
- cURL: 
```
curl --location 'http://localhost:8000/login/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx' \
--data '{
  "username": <username>,
  "password": <password>
}'
```
- URL:
`http://localhost:8000/login/`

#### Refresh login endpoint
- cURL: 
```
curl --location 'http://localhost:8000/login/refresh/' \
--header 'Content-Type: application/json' \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx' \
--data '{
    "refresh_token":<refresh_token>
}'
```
- URL:
`http://localhost:8000/login/refresh/`

#### Create match endpoint
- cURL: 
```
curl --location --request POST 'http://localhost:8000/matches/' \
--header 'Authorization: Bearer <access_token> \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx'
```
- URL:
`http://localhost:8000/matches/`

#### Get all your matches endpoint
- cURL: 
```
curl --location 'http://localhost:8000/matches/all/' \
--header 'Authorization: Bearer <access_token> \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx'
```
- URL:
`http://localhost:8000/matches/all/`

#### Get match endpoint
- cURL: 
```
curl --location 'http://localhost:8000/matches/<match_id>/' \
--header 'Authorization: Bearer <access_token> \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx'
```
- URL:
`http://localhost:8000/matches/<match_id>/`

#### Join match endpoint
- cURL: 
```
curl --location --request POST 'http://localhost:8000/matches/<match_id>/join/' \
--header 'Authorization: Bearer <access_token> \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx'
```
- URL:
`http://localhost:8000/matches/<match_id>/join/`

#### Make a movement endpoint
- cURL: 
```
curl --location --request POST 'http://localhost:8000/matches/<match_id>/movements/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <access_token> \
--header 'Cookie: csrftoken=quxjPpTmoLAX702sRZ5eGHdQ2nvAVrOx' \
--data '{
    "x":<x_position>,
    "y":<y_position>
}'
```
- URL:
`http://localhost:8000/matches/<match_id>/movements/`
