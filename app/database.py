from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

load_dotenv()

# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('DB_USER')}:"
#     f"{os.getenv('DB_PASSWORD')}@"
#     f"{os.getenv('DB_HOST')}/"
#     f"{os.getenv('DB_NAME')}"
# )

DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL)
    

def get_session():
    with Session(engine) as session:
        yield session
    
