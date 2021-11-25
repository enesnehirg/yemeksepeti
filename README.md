# Yemeksepeti

### Run in a Docker container

If you have already installed Docker on your local computer, just run the bash script in terminal.

`$ bash script.sh`

This command will pull Redis, PostgreSQL and this web API's image and start the development server on localhost:8000.
Once you have started, API is going to listen pub/sub topic 'orders'. If an order gets created, then its data will be 
published to that topic. Just after that, API automatically sends a `PATCH` request to `api/v1/complete-order/<:id>/` 
which makes the order's status "Completed". This sounds weird but that is the only way to subscribe a topic from an 
endpoint.

It also loads some initial Food, Restaurant and Category data while it's starting.

You can also run it without docker.

### Run in your local computer

Make sure to your Redis client is up and running.

Set environment variables:
```
DJANGO_SETTINGS_MODULE=api.settings.base
DB_NAME=<your_db_name>
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=localhost
REDIS_HOST=localhost
```

Create virtual environment:
`$ python3 -m venv venv`

Activate venv:
`$ source venv/bin/activate`

Install requirements:
`$ pip install -r requirements.txt`

Run tests:
`$ python manage.py test`

Start development server:
`$ python manage.py runserver`

Listen `orders` topic:
`$ python manage.py subscribe`
