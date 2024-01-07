import logging
import barcode
import time
import os

from barcode.writer import ImageWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from json import loads
from kafka import KafkaConsumer

from app.my_enum import EnvironmentVariables as EnvVariables


def main():
    try:
        consumer = KafkaConsumer(
            EnvVariables.KAFKA_SHIPPING_TOPIC_NAME.get_env(),
            bootstrap_servers=f'{EnvVariables.KAFKA_SERVER.get_env()}:{EnvVariables.KAFKA_PORT.get_env()}',
            value_deserializer=lambda x: loads(x.decode('utf-8')),
            auto_offset_reset='earliest',
            enable_auto_commit=True,
        )
        for message in consumer:
            data = message.value

            # Generate a barcode
            timestamp = time.time()
            name = str(timestamp)
            barcode_file = create_barcode(name, name)
            # Specify the path and name of the PDF file
            pdf_path = name + "_shipping_label.pdf"
            create_shipping_label(data.get("address"), data.get("email"), barcode_file, pdf_path)
            # Cleanup the barcode image file
            os.remove(barcode_file)

    except Exception as e:
        print("Exception occurred", e)


# Function to create barcode
def create_barcode(code, filename):
    CODE128 = barcode.get_barcode_class('code128')
    barcode_instance = CODE128(code, writer=ImageWriter())
    return barcode_instance.save(filename)


# Function to create PDF for shipping label
def create_shipping_label(address, email, barcode_file, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter

    # Add barcode
    c.drawImage(barcode_file, x=50, y=height - 150, width=400, height=100)

    # Add Name, Address, and Email
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 200, f"Email: {email}")
    c.drawString(50, height - 220, f"Address: {address}")

    c.save()
