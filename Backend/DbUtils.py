import sqlite3 as sql

def CreateDatabase():
    coneccion = sql.connect("./Database/datos.db")
    coneccion.commit()
    coneccion.close()
    CreateInitialTables()
    print("Se ha creado la base de datos")

def SendQuery(query):
    query = query
    coneccion = sql.connect("./Database/datos.db")
    cursor = coneccion.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    coneccion.commit()
    coneccion.close()
    return data

def CreateInitialTables():
    SendQuery("CREATE TABLE Chicas (cid integer primary key, nombre text not null)")
    SendQuery("CREATE TABLE Asistencia (cid integer, fecha text not null, asistencia text, hora text, PRIMARY KEY (cid, fecha))")
    SendQuery(" CREATE TABLE Pagos (cid integer, fecha text not null, sueldo integer,bonus integer, fichas integer, extras integer,info text,PRIMARY KEY (cid, fecha))")

def test_data():
    import random
    asistencia = ['si', 'no']
    for i in range(10):
        SendQuery(f"INSERT INTO Pagos (cid, fecha, sueldo, bonus,fichas, extras, info) VALUES ('{i+1}',date('now'),0, {random.randint(1000,99999)}, {random.randint(1000,99999)}, {random.randint(1000,99999)}, '')")
        SendQuery(f"INSERT INTO Chicas (nombre) VALUES ('chica{str(i + 10)}')")
        SendQuery(f"INSERT INTO Asistencia (cid, fecha, asistencia, hora) VALUES ('{i+1}',date('now'), '{random.choice(asistencia)}', '16:00')")

if __name__ == "__main__":
    CreateDatabase()
    test_data()
    #SendQuery("SELECT nombre, fecha, sueldo, fichas, extras FROM Pagos, Chicas WHERE Chicas.cid = Pagos.cid")