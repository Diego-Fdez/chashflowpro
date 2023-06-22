from app.database.database import Base
from sqlalchemy import Column, String, Boolean, CHAR, Integer, DOUBLE_PRECISION, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import uuid

# create a class for the user schema
class User_Schema(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    sub = Column(String(250), nullable=False)
    email = Column(String(85), nullable=False, unique=True)
    username = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now(), server_default=text('now()'))
    phone_number = Column(String(15), nullable=True)
    is_active = Column(Boolean, server_default='TRUE')
    is_admin = Column(Boolean, server_default='TRUE')
    is_superuser = Column(Boolean, server_default='FALSE')
    user_type = Column(CHAR, server_default='A')
    is_pro = Column(Boolean, server_default='FALSE')


# create a class for the clients schema
class Client_Schema(Base):
    __tablename__ = "clients"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    client_name = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    phone_number = Column(String(15), nullable=True)
    address = Column(String(250), nullable=True)
    email = Column(String(85), nullable=True)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    status = Column(CHAR, server_default='P')


# create a class for the categories schema
class Category_Schema(Base):
    __tablename__ = "categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    category_name = Column(String(120), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())


# create a class for the products schema
class Product_Schema(Base):
    __tablename__ = "products"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    product_name = Column(String(170), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    price = Column(DOUBLE_PRECISION, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String(250), nullable=True)
    category_id = Column(UUID, ForeignKey("categories.id", ondelete='CASCADE'), nullable=False)
    category = relationship('Category_Schema')


# create a class for the orders schema
class Order_Schema(Base):
    __tablename__ = "orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    total_amount = Column(DOUBLE_PRECISION, nullable=False)
    status = Column(CHAR, server_default='P')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    client_id = Column(UUID, ForeignKey("clients.id", ondelete='CASCADE'), nullable=False)
    client = relationship('Client_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    product_id = Column(UUID, ForeignKey("products.id", ondelete='CASCADE'), nullable=False)
    product = relationship('Product_Schema')


# create a class for the payments schema
class Payment_Schema(Base):
    __tablename__ = "payments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    amount = Column(DOUBLE_PRECISION, nullable=False)
    status = Column(CHAR, server_default='P')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    order_id = Column(UUID, ForeignKey("orders.id", ondelete='CASCADE'), nullable=False)
    order = relationship('Order_Schema')


# create a class for the collections agreements
class CollectionAgreement_Schema(Base):
    __tablename__ = "collection_agreements"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    agreed_date = Column(Integer, nullable=False)
    temporary_date = Column(Date, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, onupdate=func.now())
    status = Column(CHAR, server_default='P')
    client_id = Column(UUID, ForeignKey("clients.id", ondelete='CASCADE'), nullable=False)
    client = relationship('Client_Schema')
    user_id = Column(UUID, ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    user = relationship('User_Schema')
    order_id = Column(UUID, ForeignKey("orders.id", ondelete='CASCADE'), nullable=False)
    order = relationship('Order_Schema')