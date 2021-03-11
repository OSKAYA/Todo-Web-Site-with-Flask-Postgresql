import psycopg2

params = {
  'dbname': 'blog',
  'user': 'blog',
  'password': 'blog',
  'host': '192.168.1.72',
  'port': 5432
}

def insert_to_users(name,email,password,username):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query=" INSERT INTO users (nm, email, psswrd, username) VALUES (%s,%s,%s,%s);"
  cur.execute(query,(name,email,password,username))
  conn.commit()
  conn.close()

def check_user(username):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "SELECT * FROM  users WHERE username = %s;"
  cur.execute(query,(username,))
  data = cur.fetchone()
  if data == None:
    conn.close()
    return 
  
  else :
    conn.close()
    return (data)

def insert_to_todos(Author,ToDo,Due_Date):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query="INSERT INTO todos (author,todo,due_date) VALUES (%s,%s,%s);"
  cur.execute(query,(Author,ToDo,Due_Date))
  conn.commit()
  conn.close()

def get_from_todos_for_user(id):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "SELECT * FROM  users WHERE username = %s;"
  cur.execute(query,(username,))
  data = cur.fetchall()
  if data == None:
    conn.close()
    return 
  
  else :
    conn.close()
    return (data)

def query_from_todos():
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "SELECT * FROM  todos ORDER BY id;"
  cur.execute(query)
  data = cur.fetchall()
  if data == None:
    conn.close()
    return 
  
  else :
    conn.close()
    return (data)

def get_from_todos_for_id(id):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "SELECT  * FROM  todos WHERE id = %s;"
  cur.execute(query,(id,))
  data = cur.fetchone()
  if data == None:
    conn.close()
    return 
  
  else :
    conn.close()
    return (data)

def updateStatus(id):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "SELECT  completed FROM  todos WHERE id = %s;"
  cur.execute(query,(id,))
  data = cur.fetchone()
  newdata = not data[0]
  query= "UPDATE todos SET completed=%s WHERE id = %s;" 
  cur.execute(query,(newdata,id))
  conn.commit()
  conn.close()
  return 

def del_item_from_todos_for_id(id):
  conn = psycopg2.connect(**params)
  cur = conn.cursor()
  query= "DELETE FROM todos WHERE id = %s;" 
  cur.execute(query,(id,))
  conn.commit()
  conn.close()
  return 