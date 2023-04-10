import psycopg2

#Information about the MAU database
hostname = 'pgserver.mau.se'
database_name = 'hairfind_db'
usernames = 'al0791'
password = 'aks4rzug'
port_id = 5432


conn = psycopg2.connect(
    database=database_name,
    user=usernames,
    password=password,
    host=hostname,
    port=port_id
)
print("Successfully connected to the database.")

conn.close()
