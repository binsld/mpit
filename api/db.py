from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, SmallInteger, CHAR, DateTime, Boolean, BigInteger
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_URL

engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    telegram_username = Column(String(32), nullable=True)
    fio = Column(String(64), nullable=True)
    phone = Column(BigInteger(), nullable=True)
    coins = Column(SmallInteger, default=0)
    type = Column(CHAR) # BOUMA классификация (B-anned O-utsider U-ser M-oderator A-dministration)
    state = Column(SmallInteger) # 1 - ожидание фио    2 - ожидание телефона    3 - данные подтверждены

    def __repr__(self):
       return "<User(telegram_id='%s', telegram_username='%s', fio='%s', phone='%s', coins='%s', type='%s')>" % (
                            self.telegram_id, self.telegram_username, self.fio, self.phone, self.coins, self.type)

class Event(Base):
    __tablename__ = 'events'
    id = Column(SmallInteger, autoincrement=True, primary_key=True)
    name = Column(String(48))
    date = Column(DateTime)
    description = Column(String(400))
    image_url = Column(String(30))
    location = Column(String(60))
    bank = Column(SmallInteger) # Сколько монет можно будет раздать, -1 для неограниченного числа
    def __repr__(self):
       return "<Event(name='%s', date='%s', description='%s', location='%s', bank='%s')>" % (
                                self.name, self.date, self.description, self.location, self.bank)

class Registered(Base):
    __tablename__ = 'registered'
    id = Column(SmallInteger, autoincrement=True, primary_key=True)
    user_id = ForeignKey(User.telegram_id)
    event_id = ForeignKey(Event.id)
    marked = Column(Boolean, default=False)
    tag = Column(String(60))

    def __repr__(self):
       return "<Registered(user_id='%s', event_id='%s', marked='%s', tag='%s')>" % (
                            self.user_id, self.event_id, self.marked, self.tag)

class Merch(Base):
    __tablename__ = 'merchs'
    id = Column(SmallInteger, autoincrement=True, primary_key=True)
    name = Column(String(40))
    description = Column(String(200))
    image_url = Column(String(30))


class Authtoken(Base):
    __tablename__ = "authtokens"
    id = Column(SmallInteger, autoincrement=True, primary_key=True)
    user_id = ForeignKey(User.telegram_id)
    token = Column(String(40))
    created = Column(DateTime)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()
