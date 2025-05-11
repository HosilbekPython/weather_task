import psycopg2

try:
    connection = psycopg2.connect(
        dbname="weather_db",
        user="postgres",
        password="1903",
        host="localhost",
        port="5433"
    )
    print("Ulanish muvaffaqiyatli!")
    connection.close()
except Exception as e:
    print(f"Xato: {e}")