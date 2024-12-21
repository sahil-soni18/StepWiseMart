from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgres://postgres:myPostgres@localhost:5432/StepWiseMart"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=True, autoflush=True, bind=engine)

Base = declarative_base()



