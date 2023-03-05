import Backend.DbUtils as db
#import DbUtils as db
from PyQt5.QtCore import QObject, pyqtSignal, QTime, QDate
import sqlite3

class Logica(QObject):
    senal_enviar_asistencia = pyqtSignal(list)
    senal_enviar_chicas = pyqtSignal(list)
    senal_resultado_asistencia = pyqtSignal(str, str)
    senal_enviar_pagos = pyqtSignal(list)
    senal_enviar_pagos_semanal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.enviar_chicas()

    def get_bonus(self, fichas):
        return 5000 * (fichas // 50000)

    def enviar_chicas(self):
        chicas = db.SendQuery(f"""SELECT * FROM Chicas""")
        self.senal_enviar_chicas.emit(chicas)

    def actualizar_pagos(self,lista):
        cid = int(lista[0])
        fecha = lista[1]
        sueldo = int(lista[2])
        fichas = int(lista[4])
        bonus = self.get_bonus(fichas)
        extra = int(lista[5])
        #try:
        db.SendQuery(f"UPDATE Pagos SET sueldo = {sueldo}, bonus = {bonus}, fichas = {fichas}, extras = {extra} WHERE (cid = {cid} AND fecha = '{fecha}')")
        #except:
            #print("error")
    def is_saturday(self, fecha):
        fecha = fecha.split("-")
        dia = int(fecha[2])
        mes = int(fecha[1])
        año = int(fecha[0])
        dia = QDate(año, mes, dia).dayOfWeek()
        #print(dia)
        if dia == 6:
            #print("is Saturday", dia, mes, año) 
            return True
            

    def modificar_chicas(self, id, nombre):
        #print(str(id),nombre)
        try:
            db.SendQuery(F"UPDATE Chicas SET nombre= '{nombre}' WHERE cid = {id}")
        except:
            print("error al cambiar nombre")
        else:
            chicas = db.SendQuery(f"""SELECT * FROM Chicas""")
            self.senal_enviar_chicas.emit(chicas)

    def agregar_chicas(self, chicas):
        for chica in chicas:
            #print(chica)
            db.SendQuery(f"INSERT INTO Chicas (nombre) VALUES ('{chica}')")

    def agregar_chica(self):
        db.SendQuery(f"INSERT INTO Chicas (nombre) VALUES ('')")
        self.enviar_chicas()
        

    def stringify_values(self, chica):
        values = ""
        for valor in chica:
            values = values + f"'{valor}',"
        return values[:-1] # valores en string para la consulta

    def recibir_asistencia(self, asistencia):
        #print("recibiendo asistencia en la logica")
        check = self.revisar_asistencia(asistencia)
        if check: 
            self.enviar_asistencia(asistencia)
            
    def revisar_asistencia(self, chica): # revisa si la consulta no arrojara errores
        #print("revisando...")
        descripcion_error = ""
        cid = chica[0]
        fecha = chica[1]
        result = db.SendQuery(f"SELECT * FROM Asistencia WHERE cid = '{cid}' AND fecha = '{fecha}'") # Revisa si existe la fila
        if result != []:# Existe alguna
            descripcion_error = descripcion_error + f"Cid: {cid}, Fecha: {fecha}\n"
        if descripcion_error != "": #existen filas
            #print("Existe")
            self.senal_resultado_asistencia.emit("Already exists", descripcion_error)
            return False
        return True

    def enviar_asistencia(self, chica):
        #print(chica)
        values = self.stringify_values(chica)
        try :
            db.SendQuery(f"INSERT INTO Asistencia (cid, fecha, asistencia, hora) VALUES ({values})")
        except:
            print("Error extraño")
        else:
            self.senal_resultado_asistencia.emit("Succeded", "")
            sueldo = self.get_sueldo(chica[3])
            try:
                if db.SendQuery(f"SELECT * FROM Pagos WHERE cid = '{chica[0]}' AND fecha = '{chica[1]}'") == []: # Revisa si existe la fila 
                        db.SendQuery(f"INSERT INTO Pagos (cid, fecha,sueldo, bonus, fichas, extras, info) VALUES ('{chica[0]}','{chica[1]}' ,'{sueldo}' ,'0','0','0', '')")
                if chica[2] == "No" and self.is_saturday(chica[1]):
                    sabado = chica[1].split("-")
                    sabado = QDate(int(sabado[0]), int(sabado[1]), int(sabado[2]))
                    #print("sabado", sabado)
                    lunes = sabado.addDays(2)
                    lunes = lunes.toString("yyyy-MM-dd")
                    martes = sabado.addDays(3)
                    martes = martes.toString("yyyy-MM-dd")
                    #print(lunes, martes)
                    db.SendQuery(f"INSERT INTO Pagos (cid, fecha,sueldo, bonus, fichas, extras, info) VALUES ('{chica[0]}','{lunes}' ,'0' ,'0','0','0', 'Sin sueldo por inasistencia el dia {chica[1]}')")
                    db.SendQuery(f"INSERT INTO Pagos (cid, fecha,sueldo, bonus, fichas, extras, info) VALUES ('{chica[0]}','{martes}' ,'0' ,'0','0','0', 'Sin sueldo por inasistencia el dia {chica[1]}')")
            except: print("Error extraño al agregar el pago")

    def get_sueldo(self, hora_llegada):
        if hora_llegada == "": return "0"
        hora_entrada = QTime(20,30,0)
        hora_llegada = QTime.fromString(hora_llegada, "hh:mm")
        if hora_llegada >  hora_entrada: return "0"
        else: return "15000"

    def eliminar_chica(self, nombre):
        #print(nombre)
        db.SendQuery(f"DELETE FROM Chicas WHERE nombre = '{nombre}'")

    def insertar_columna(self, tabla, columna, type='text'):
        db.SendQuery(f"ALTER TABLE {tabla} ADD {columna} {type}")

    def eliminar_columna(self, tabla, columna):
        db.SendQuery(f"ALTER TABLE {tabla} DROP COLUMN {columna}")
    
    def agregar_pagos(self, cid, sueldo, fichas, extras, fecha= "strftime('%d/%m/%Y', date('now'))"):
        db.SendQuery(f"""INSERT INTO Pagos (cid, fecha, sueldo, fichas, extras) VALUES({cid},{fecha},{sueldo},{fichas},{extras})""")

    def solicitar_asistencia(self, fecha):
        chicas = db.SendQuery(f"""SELECT Asistencia.cid, Chicas.nombre, Asistencia.fecha, Asistencia.asistencia, Asistencia.hora FROM Chicas, Asistencia WHERE Chicas.cid = Asistencia.cid AND Asistencia.fecha = '{fecha}'""")
        self.senal_enviar_asistencia.emit(chicas)
    
    def solicitar_chicas(self):
        chicas = db.SendQuery(f"""SELECT * FROM Chicas""")
        self.senal_enviar_chicas.emit(chicas)

    def solicitar_pagos(self, fecha):
        pagos = db.SendQuery(f"""SELECT Pagos.cid, Chicas.nombre, Pagos.sueldo, Pagos.bonus, Pagos.fichas, Pagos.extras, Pagos.info FROM Pagos, Chicas WHERE Chicas.cid = Pagos.cid AND fecha = '{fecha}'""")
        self.senal_enviar_pagos.emit(pagos)

    def borrar_asistencia(self, asistencia):
        query =f"""DELETE FROM Asistencia WHERE cid = {asistencia[0]} AND fecha = '{asistencia[2]}'"""
        try:
            db.SendQuery(query)
        except: print("error")
        else:
            db.SendQuery(f"""DELETE FROM Pagos Where cid = {asistencia[0]} AND fecha = '{asistencia[2]}'""")


    def actualizar_asistencia(self,asistencia):
        #print(asistencia)
        db.SendQuery(f"UPDATE Asistencia SET asistencia= '{asistencia[2]}', hora='{asistencia[3]}' WHERE (cid = {asistencia[0]} AND fecha = '{asistencia[1]}')")
        
    def get_pago_semanal(self,fecha1,fecha2):
        query=f"""SELECT Pagos.cid, Chicas.nombre, Pagos.fecha, Pagos.sueldo, Pagos.bonus, Pagos.fichas, Pagos.extras FROM Pagos, Chicas WHERE (fecha BETWEEN '{fecha1}' AND '{fecha2}') AND Pagos.cid = Chicas.cid"""
        pagos_semanales = db.SendQuery(query)
        diccionario = {}
        for t in pagos_semanales:
            llave, *valores = t
            if llave in diccionario:
                diccionario[llave].extend([valores])
            else:
                 diccionario[llave] = list([valores])
        self.senal_enviar_pagos_semanal.emit(diccionario)

if __name__ == "__main__":

    logica_sistema = Logica()
    logica_sistema.get_pago_semanal()
    #logica_sistema.agregar_pagos(cid=2, sueldo=500000, fichas=40000, extras=3000)
    #logica_sistema.insertar_columna('Chicas', 'columnaprueba')
    #logica_sistema.eliminar_columna('Chicas','columnaprueba')
    #logica_sistema.agregar_chica("chicaprueba")
    #logica_sistema.eliminar_chica("chicaprueba")
