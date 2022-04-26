import databases
import sqlalchemy

from config import CONNECTION_STRING

database = databases.Database(CONNECTION_STRING)
metadata = sqlalchemy.MetaData()
