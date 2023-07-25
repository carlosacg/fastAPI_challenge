import psycopg2
from conf.envs import HOST_DB, DB_NAME, USER_DB, PASSWORD_DB

# Define the database connection
conn = psycopg2.connect(
    host=HOST_DB,
    dbname=DB_NAME,
    user=USER_DB,
    password=PASSWORD_DB
)