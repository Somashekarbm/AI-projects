import psycopg2

conn = psycopg2.connect("dbname=mockrecruiter user=admin password=securepass")
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS interviews (
        id SERIAL PRIMARY KEY,
        user_id TEXT,
        question TEXT,
        answer TEXT,
        feedback TEXT,
        score INT
    )
""")
conn.commit()
