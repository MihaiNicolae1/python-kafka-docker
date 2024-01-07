from app.dependencies.db import SessionLocal, engine, Base

# Create tables
Base.metadata.create_all(bind=engine)