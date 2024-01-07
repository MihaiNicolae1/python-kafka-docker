import logging
import json

from json import loads
from kafka import KafkaConsumer
from sqlalchemy.orm import Session

from app.my_enum import EnvironmentVariables as EnvVariables
from app.dependencies.db import get_db, SessionLocal
from app.core.models.product import Product
from app.core.gateways.kafka import Kafka


class StockError(Exception):
    """Custom exception for stock related errors."""
    pass


def decrease_stock(product_id: int, quantity: int, db: Session):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product and product.stock >= quantity:
        product.stock -= quantity
        return
    raise StockError(f"Product with ID {product_id} not found or insufficient stock")


async def send_to_fulfill(data: json, server: Kafka):
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
            topic=EnvVariables.KAFKA_FULFILL_TOPIC_NAME.get_env(),
            port=EnvVariables.KAFKA_PORT.get_env(),
            servers=EnvVariables.KAFKA_SERVER.get_env(),
        )
        await kafka_server.aioproducer.start()
        # To consume latest messages and auto-commit offsets
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_VALIDATE_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        for message in consumer:
            data = message.value
            items = data.get("items", [])
            with SessionLocal() as session:
                try:
                    for item in items:
                        decrease_stock(item.get("id"), item.get("quantity"), session)
                    session.commit()
                    await send_to_fulfill(data, kafka_server)
                    print("Successfully decreased stock")
                except Exception as e:
                    print(f"Error decreasing stock: {e}")
        await kafka_server.aioproducer.stop()
    except Exception as e:
        logging.info('Connection successful', e)
