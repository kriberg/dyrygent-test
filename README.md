Start redis and rabbitmq

```
docker run --rm -it -p "6379:6379" redis:latest
docker run --rm -it -p "5672:5672" rabbitmq:latest
```

Fix virtualenv and start worker
```
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
celery -A test worker
```

Start the tasks
```
source .venv/bin/activate
python -m test.main
```

