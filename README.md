# time-tracker-be

## Development

### Project Requirements

* Python 3.11+
* Virtualenv 20.24+
* Docker Engine 20.10+
* Docker Compose 1.29+

### IDE

We recommend you use Visual Studio Code and set it up using the ff. extensions and settings below.

##### Extensions

Install these extensions in VS Code:

* Python
* Django
* Pylint
* Flake8
* MyPy Type Checker

##### Settings
VSCode workspace settings are already included in the project (*.vscode/settings.json*)

##### Run the Project Locally Without Docker
1. Clone the project.
2. In the project directory create a virtualenv by running the command "python -m venv venv".
3. Activate the virtualenv.
4. Install the dependencies.
5. Run migrations using "python manage.py migrate".
5. Create a superuser using the command "python manage.py createsuperuser".
7. Run the localhost server using "python manage.py runserver".

##### Run the Project Locally Without Docker
1. Clone the project.
2. Run "docker compose up --build to build the images.
3. Apply migrations using the command "docker exec -it time-tracker-be python manage.py migrate".
4. Create a superuser using the command "docker exec -it time-tracker-be python manage.py createsuperuser".
5. The app can now be accessed in your localhost port 8000.
