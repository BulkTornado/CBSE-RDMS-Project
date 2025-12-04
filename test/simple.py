import mysql.connector as _mysql

try:
    db_object = _mysql.connect(host="localhost", user="root", passwd="")
    cursor_ob = db_object.cursor()
    cursor_ob.execute("USE CBSE_Database;")
    cursor_ob.execute("SELECT * FROM schools_data;")
    print(cursor_ob.fetchall())
    print(db_object.close())
except Exception as error:
    print(error)
    print(repr(error))
