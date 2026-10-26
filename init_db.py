
from app.database.session import Base, engine
from app.model import model  # Registers all three models

Base.metadata.create_all(bind=engine)

print("Database tables created successfully.")
