from sqlalchemy import Column, Text, String, Boolean, Float, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Domain(Base):
    __tablename__ = 'domain'

    domain_name = Column(Text, primary_key=True, nullable=False)
    query = Column(Text, nullable=False)
    tld = Column(String(16), nullable=False)
    purchasable = Column(Boolean, nullable=False)
    premium = Column(Boolean)
    purchase_price = Column(Float)
    purchase_type = Column(String(64))
    renewal_price = Column(Float)
    created_at = Column(DateTime, default=func.now(), onupdate=func.now())
