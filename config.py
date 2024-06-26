import psycopg2

connection = psycopg2.connect(
    host="127.0.0.1",
    user="postgres_username",
    password="postgres_password",
    dbname="converter",
)