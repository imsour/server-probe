# Server Probe Concept
This projects demonstrates an API response time monitoring service, using FastAPI, RabbitMQ, ReactJS and Celery.

## Docker-Compose Run (Production) example
### Requirements

- Docker
  - [docker-compose](https://docs.docker.com/compose/install/)

### Run Services
1. Run command ```docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up``` to start up our RabbitMQ image, ReactJS Application API Server and Celery Worker instances.
2. Navigate to [http://localhost:3000/](http://localhost:3000/) to view the probe results and start/stop the tests.
3. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) and execute API calls, for example, add a **Server** to test.
4. You can monitor the execution of the celery tasks in the console logs or navigate to the RabbitMQ monitoring app: [http://localhost:15672](http://localhost:15672) (username: admin, password: password123).
5. Use the ```scale``` options to specify the amount of worker containers that are to be created. for example: ```docker-compose -f docker-compose.yaml -f docker-compose.prod.yaml up --scale worker=3``` to scale the application with more worker instances.

## Local Development Run example

### FastAPI and Celery worker
#### Requirements

- Python >= 3.9
  - [pip](https://pip.pypa.io/en/stable/installation/)
- RabbitMQ instance
  - ```docker-compose up rabbitmq```
- Local env values
  - ```cp sample/sample.env server-probe/.env```

#### Install dependencies
```pip install server-probe/requirements.txt```

#### Run the services

1. **Optional:** use the prepopulated DB with test servers: ```cp sample/probe.db server-probe/.```
2. ```cd server-probe/```
3. Start the FastAPI web server with ```uvicorn main:app --reload```.
4. Start the Celery worker with ```celery -A celery_worker worker -l info```.
5. Navigate to [http://localhost:8000/docs](http://localhost:8000/docs) and execute test API calls. You can monitor the execution of the celery tasks in the console logs or navigate to the RabbitMQ monitoring app: [http://localhost:15672](http://localhost:15672) (username: admin, password: password123).

### ReactJS web interface 
#### Requirements

- Node >= 16
  - [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

#### Install dependencies
```yarn --cwd probe-ui install```

#### Run the app
1. ```cd probe-ui/```
2. Start the ReactJS application with ```npm start```.
3. Navigate to [http://localhost:3000/](http://localhost:3000/) to view the probe results and start/stop the tests.
