from sqlalchemy import (Column, Date, Float, Integer, String, Boolean, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy import func

Base = declarative_base()


class Apartment(Base):
    __tablename__ = "apartments"

    id = Column(Integer, primary_key=True)
    city = Column(String)
    district = Column(String)
    property_type = Column(String)
    address = Column(String)
    link = Column(String, primary_key=True)
    description = Column(String)
    price = Column(Float(decimal_return_scale=2))
    rooms = Column(Integer)
    floor = Column(Integer)
    squares = Column(Integer)
    price_per_square = Column(Float(decimal_return_scale=2))
    directly = Column(Boolean)


conn_string = r"sqlite:///adresowo.db"
echo = False
engine = create_engine(conn_string, echo=echo)
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
