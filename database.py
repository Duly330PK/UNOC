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
# Das Debug-Print kann für die Produktion entfernt werden
# print(f"DEBUG: Geladene DATABASE_URL: '{DATABASE_URL}'")
if not DATABASE_URL:
    raise ValueError("Keine DATABASE_URL in der .env-Datei gefunden!")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Assoziationstabelle für die Many-to-Many-Beziehung zwischen Ring und Device
ring_device_association = Table('ring_device_association', Base.metadata,
    Column('ring_id', Integer, ForeignKey('rings.id'), primary_key=True),
    Column('device_id', Integer, ForeignKey('devices.id'), primary_key=True)
)

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    device_id_str = Column(String, unique=True, index=True, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, default="online")
    properties = Column(JSON, default={})
    coordinates = Column(JSON)

    # KORREKTUR: back_populates hinzugefügt, um die Beziehung explizit zu machen
    links_as_source = relationship("Link", foreign_keys="[Link.source_id]", back_populates="source")
    links_as_target = relationship("Link", foreign_keys="[Link.target_id]", back_populates="target")

    # KORREKTUR: back_populates auch für die Many-to-Many-Beziehung hinzugefügt
    rings = relationship("Ring", secondary=ring_device_association, back_populates="nodes")

class Link(Base):
    __tablename__ = "links"
    id = Column(Integer, primary_key=True, index=True)
    link_id_str = Column(String, unique=True, index=True, nullable=False)
    source_id = Column(Integer, ForeignKey("devices.id"))
    target_id = Column(Integer, ForeignKey("devices.id"))
    status = Column(String, default="up")
    properties = Column(JSON, default={})

    # KORREKTUR: back_populates hinzugefügt, um die Beziehung explizit zu machen
    source = relationship("Device", foreign_keys=[source_id], back_populates="links_as_source")
    target = relationship("Device", foreign_keys=[target_id], back_populates="links_as_target")

class Ring(Base):
    __tablename__ = "rings"
    id = Column(Integer, primary_key=True, index=True)
    ring_id_str = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    rpl_link_id_str = Column(String, nullable=False)
    
    # KORREKTUR: back_populates auch für die Many-to-Many-Beziehung hinzugefügt
    nodes = relationship("Device", secondary=ring_device_association, back_populates="rings")

class Alarm(Base):
    __tablename__ = "alarms"
    id = Column(Integer, primary_key=True, index=True)
    severity = Column(String, nullable=False)  # CRITICAL, MAJOR, MINOR, WARNING
    status = Column(String, nullable=False)    # ACTIVE, ACKNOWLEDGED, CLEARED
    timestamp_raised = Column(String, nullable=False)
    timestamp_cleared = Column(String)
    affected_object_type = Column(String)  # 'device' oder 'link'
    affected_object_id = Column(String)
    description = Column(String)

def init_db():
    """Erstellt alle Tabellen in der Datenbank."""
    Base.metadata.create_all(bind=engine)