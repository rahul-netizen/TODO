## A simple flask application hosted on heroku

To use install the dependecies in an venv using
* `pip install requirements.txt`

After that serve the application on WSGI like gunicorn, waitress

* `waitress-serve --listen=127.0.0.1:5000 app:app`, where app before colon is the name of the python file & after it the method
