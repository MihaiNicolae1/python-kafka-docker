#!/bin/bash

# Run the seeder
python -m app.seeder

# Start the main application
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
