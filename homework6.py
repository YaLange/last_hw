from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float, Date
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import func

class Base(DeclarativeBase): pass

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    books = relationship("Book")

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    stocks = relationship("Stock", back_populates="shop")


class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, index=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    book = relationship("Book", back_populates="stocks")
    id_shop = Column(Integer, ForeignKey('shop.id'))
    shop = relationship("Shop", back_populates="stocks")
    count = Column(Integer)
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True, index=True)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    stock = relationship("Stock", back_populates="sales")
    count = Column(Integer)
    price = Column(Float)
    date_sale = Column(Date)


database_name = "test1"
user = "postgres"
password = "123"
host = "localhost"
port = 5432
engine_url = f"postgresql://{user}:{password}@{host}:{port}/{database_name}"

engine = create_engine(engine_url)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def get_shops(publisher_id_or_name):   
    query = session.query(
        Book, Shop, Publisher, Sale
    ).join(Book).join(Stock).join(Sale).join(Shop)

    if publisher_id_or_name.isdigit():
        query = query.filter(Publisher.id == int(publisher_id_or_name))
    else:
        query = query.filter(func.lower(Publisher.name).contains(publisher_id_or_name.lower()))
    
    records = query.all() 
    for book, shop, publisher, sale in records:
        print(f"{book.title: <40} | {shop.name: <10} | {sale.price: <8} | {sale.date_sale.strftime('%d-%m-%Y')}")

if __name__ == '__main__':
    publisher_id_or_name = input("Введите имя или идентификатор издателя: ")
    get_shops(publisher_id_or_name)