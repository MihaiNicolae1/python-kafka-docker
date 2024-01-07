from app.dependencies.db import SessionLocal, engine, Base
from app.core.models.product import Product

# Create tables
Base.metadata.create_all(bind=engine)


# Seed data
def seed_data():
    db = SessionLocal()
    try:
        products = [
            Product(id=1, stock=10, title='Product 1', name='Prod1', description='Description 1'),
            Product(id=2, stock=0, title='Product 2', name='Prod2', description='Description 2'),
            Product(id=3, stock=50, title='Product 3', name='Prod3', description='Description 3'),
            Product(id=4, stock=100, title='Product 4', name='Prod4', description='Description 4'),
            Product(id=5, stock=3, title='Product 5', name='Prod5', description='Description 5'),
            Product(id=6, stock=5, title='Product 6', name='Prod6', description='Description 6'),
        ]
        db.add_all(products)
        db.commit()
    finally:
        db.close()


seed_data()
