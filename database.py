#
# UNOC - database.py
#
# Definiert das Datenbank-Schema mit SQLAlchemy ORM und die Session-Logik.
#

import os
from sqlalchemy import create_engine, Column, Integer, String, Float, JSON, ForeignKey, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"DEBUG: Geladene DATABASE_URL: '{DATABASE_URL}'")
if not DATABASE_URL:
    raise ValueError("Keine DATABASE_URL in der .env-Datei gefunden!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Assoziationstabelle für die Many-to-Many-Beziehung zwischen Ring und Device
ring_device_association = Table('ring_device_association', Base.metadata,
    Column('ring_id', Integer, ForeignKey('rings.id')),
    Column('device_id', Integer, ForeignKey('devices.id'))
)

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id_str = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="online")
    properties = Column(JSON, default={})
    coordinates = Column(JSON) # Speichert [lat, lon]

    links_as_source = relationship("Link", foreign_keys="[Link.source_id]")
    links_as_target = relationship("Link", foreign_keys="[Link.target_id]")

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    link_id_str = Column(String, unique=True, index=True, nullable=False)
    source_id = Column(Integer, ForeignKey("devices.id"))
    target_id = Column(Integer, ForeignKey("devices.id"))
    status = Column(String, default="up")
    properties = Column(JSON, default={})

    source = relationship("Device", foreign_keys=[source_id])
    target = relationship("Device", foreign_keys=[target_id])

class Ring(Base):
    __tablename__ = "rings"
    id = Column(Integer, primary_key=True, index=True)
    ring_id_str = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    rpl_link_id_str = Column(String, nullable=False)
    
    nodes = relationship("Device", secondary=ring_device_association)

def init_db():
    """Erstellt alle Tabellen in der Datenbank."""
    Base.metadata.create_all(bind=engine)