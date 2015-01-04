import mongoengine
from config.config import DB_HOST, DB_PORT, DB_NAME
db = mongoengine.connect(DB_NAME, host=DB_HOST, port=DB_PORT)
db.drop_database(DB_NAME)

