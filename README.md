<div align="center">
  <h3 align="center">Python Flask RESTful API</h3>
  <p align="center">
    volleyball-meetup-chicago-backend
    <br />
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## About The Project

RESTful APIs built with a micro framework Flask

<p align="right">(<a href="#top">back to top</a>)</p>

### Built With

* [Python](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/en/2.0.x/)
* [PostgreSQL](https://www.postgresql.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.

### Prerequisites

1. [Python 3.10.1](https://docs.python.org/3/tutorial/)
1. [PostgreSQL](https://www.postgresql.org/download/)
1. [Heroku CLI](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)

### Deployment

1. FIRST TIME LOCAL - Run PostgreSQL server and make sure to create a db for development. Run PostgreSQL commands to create a db:
   ```sh
   psql --version
   # psql (PostgreSQL) 14.x
   createdb python_getting_started
   python manage.py db init
   ```
1. For DB updates:
   ```sh
   # Update DB locally
   python manage.py db migrate
   python manage.py db upgrade
   # Update DB via Heroku CLI
   heroku config --app backend-volleyball-chicago
   heroku pg:psql --app backend-volleyball-chicago
   > select * from events;
   > exit
   heroku run python3 manage.py db upgrade --app backend-volleyball-chicago
   ```
1. Test the app from curl or browser:
   ```sh
    curl https://backend-volleyball-chicago.herokuapp.com/
   ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Aleksandandar-Nedelkovski/volleyball-meetup-chicago-backend.git
   ```

2. CD into the ptoject folder
   ```sh
   cd volleyball-meetup-chicago-backend
   ```
3. Create a Virtual Environment
   ```sh
   python3 -m venv venv
   ```
4. Activate the Virtual Environment
   ```sh
   source ./venv/bin/activate
   ```
5. Install Project Requirements
   ```sh
   pip install -r requirements.txt
   ```
6. Run the App
   ```sh
   python main.py
   ```

7. Test the app from curl or browser:
   ```sh
    curl http://127.0.0.1:5000/
   ```

<p align="right">(<a href="#top">back to top</a>)</p>