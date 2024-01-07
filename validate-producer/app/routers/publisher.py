import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.gateways.kafka import Kafka
from app.core.models.message import Message
from app.core.models.product import Product
from app.dependencies.db import get_db
from app.dependencies.kafka import get_kafka_instance

router = APIRouter()

@router.post("")
async def send(data: Message, server: Kafka = Depends(get_kafka_instance), db: Session = Depends(get_db)):
    try:
        for item in data.items:
            product = db.query(Product).filter(Product.id == item.id).first()
            if not product or product.stock < item.quantity:
                return JSONResponse(
                    content={"detail": "Product not found or insufficient stock", "item": item.id},
                    status_code=status.HTTP_400_BAD_REQUEST
                )

        # If all products are available and have sufficient stock
        topic_name = server._topic
        await server.aioproducer.send_and_wait(topic_name, json.dumps(data.dict()).encode("ascii"))
    except HTTPException as http_exception:
        return JSONResponse(content={"detail": http_exception.detail}, status_code=http_exception.status_code)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        await server.aioproducer.stop()
        raise HTTPException(status_code=500, detail="Internal Server Error")

    return JSONResponse(content={"detail": "Order sent successfully"}, status_code=status.HTTP_200_OK)
