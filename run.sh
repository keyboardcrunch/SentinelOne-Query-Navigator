export FLASK_APP=app.py
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade
flask run
