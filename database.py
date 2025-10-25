from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#db_url = "mssql+pyodbc://SUKANT\\SQLEXPRESS/flask_auth?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes"

db_url = "postgresql://postgres:Sukant%4009@localhost:5432/Sukant"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush=False, bind = engine)