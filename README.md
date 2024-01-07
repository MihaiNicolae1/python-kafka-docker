# python-kafka-docker
The application validates orders

## Stack

- aiokafka
- Docker
- FastAPI
- Kafka-python
- Python 3.8

## How to use

### Using Docker Compose 
You will need Docker installed to follow the next steps. To create and run the image use the following command:

```bash
> docker-compose up --build
```


The Publisher container will create a simple RESTful API application that sends orders to Kafka. It will take a few seconds to come up, then will be accessible at `http://localhost:8000`.

The Consumer container is a script that aims to wait and receive messages from Kafka.

And the kafdrop container will provide acess to  web UI for viewing Kafka topics and browsing consumer groups that can be accessed at `http://localhost:19000`.


### API

- Send order
  
Send message to Kafka, below is an example request:
```json
POST http://localhost:8000/orders
Accept: application/json
Content-Type: application/json
Body:
{
    "email": "test@gmail.com",
    "address" : "Timisoara, RO",
    "items": [
      {"id" : 1, "quantity" : 10},
      {"id" : 10, "quantity" : 1}
    ],
}
```


- Health check
  
Checks if the app is available.
```json
GET http://localhost:8000/
Accept: application/json
Content-Type: application/json
```

### Swagger

The swagger, an automatic interactive API documentation, will be accessible at `http://localhost:8000/docs`
## Environment Variables
Listed below are the environment variables needed to run the application. They can be included in docker-compose or to run locally, it's necessary to create an `.env` file in the root of the Publisher and Consumer service folders.

- Publisher:
```bash
KAFKA_TOPIC_NAME=
KAFKA_SERVER=
KAFKA_PORT=
```

- Consumer:
```bash
KAFKA_TOPIC_NAME=
KAFKA_SERVER=
KAFKA_PORT=
```