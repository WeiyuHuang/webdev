import psycopg2

conn = psycopg2.connect('dbname=example')
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS table2;")

cursor.execute("""
  CREATE TABLE table2 (
    id INTEGER PRIMARY KEY,
    description BOOLEAN NOT NULL DEFAULT False 
  );
""")

SQL = 'INSERT INTO table2 (id, description) VALUES (%(id)s, %(description)s);'
cursor.execute(SQL, {'id': 1, 'description': True})
cursor.execute(SQL, {'id': 2, 'description': False})
cursor.execute(SQL, {'id': 3, 'description': True})
cursor.execute(SQL, {'id': 4, 'description': False})

cursor.execute('select * from table2;')
result = cursor.fetchall()
print(result)

# commit, so it does the executions on the db and persists in the db
conn.commit()

cursor.close()
conn.close()