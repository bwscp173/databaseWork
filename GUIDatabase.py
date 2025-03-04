import psycopg2

conn = psycopg2.connect(user = "esa21gpu", # not my real data
                        password = "SUPERSECRET",
                        host = "cmpstudb-01.cmp.uea.ac.uk",
                        port = "5432",
                        database = "esa21gpu")

cur = conn.cursor()
cur.execute('SET search_path TO Demo,public;')
cur.execute('SELECT * FROM emp')
rows = cur.fetchall()
for row in rows:
    print(row[0], row[1], row[3])
conn.close()