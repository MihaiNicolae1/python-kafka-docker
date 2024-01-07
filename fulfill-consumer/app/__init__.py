import logging
import json

from json import loads
from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from app.my_enum import EnvironmentVariables as EnvVariables
from app.dependencies.db import get_db, SessionLocal
from app.core.models.order import Order
from app.core.gateways.kafka import Kafka


def save_new_order(data: json, db: Session):
    print(data)
    order = Order(address='test', email='test', items='test')
    db.add(order)
    db.commit()
    return


async def send_to_shipping(data: json, server: Kafka):
    try:
        topic_name = server._topic
        await server.aioproducer.send_and_wait(topic_name, json.dumps(data).encode("ascii"))
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        await server.aioproducer.stop()
    return


async def main():
    try:
        kafka_server = Kafka(
            topic=EnvVariables.KAFKA_SHIPPING_TOPIC_NAME.get_env(),
            port=EnvVariables.KAFKA_PORT.get_env(),
            servers=EnvVariables.KAFKA_SERVER.get_env(),
        )
        await kafka_server.aioproducer.start()
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_FULFILL_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        for message in consumer:
            data = message.value
            with SessionLocal() as session:
                try:
                    save_new_order(data, session)
                    session.commit()
                    await send_to_shipping(data, kafka_server)
                    print("Successfully saved order")
                except Exception as e:
                    print(f"Error decreasing stock: {e}")
        await kafka_server.aioproducer.stop()
    except Exception as e:
        logging.info('Connection successful', e)