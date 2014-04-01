from sqlalchemy import Boolean, Column, Integer, ForeignKey, String, Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


Base = declarative_base()


techs = Table('companies_techs', Base.metadata,
    Column('company_id', Integer, ForeignKey('companies.id')),
    Column('tech_id', Integer, ForeignKey('techs.id'))
)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    website = Column(String)
    description = Column(String(140))
    size = Column(String)
    remote = Column(Boolean)

    location = relationship('Location', uselist=False, backref="company")
    techs = relationship('Tech', secondary=techs)



class Tech(Base):
    __tablename__ = 'techs'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))


class Location(Base):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    country = Column(String(2))
    postcode = Column(String)
    company_id = Column(Integer, ForeignKey('companies.id'))


def _reset_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def _get_engine(url):
    return create_engine(url)


def setup_db(url):
    """
    Get the db engine and resets the database.
    Returns a session for that database for us to insert the list of companies
    """
    engine = _get_engine(url)
    _reset_database(engine)

    return sessionmaker(bind=engine)()
