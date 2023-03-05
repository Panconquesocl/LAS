import os

RUTA_UI_INICIO = os.path.join("Frontend","Ui","Inicio2.ui")
RUTA_UI_PAGO_DIARIO = os.path.join("Frontend","Ui","PagoDiario.ui")
RUTA_UI_PAGO_SEMANAL = os.path.join("Frontend","Ui","PagoSemanal.ui")
RUTA_UI_BALANCE = os.path.join("Frontend","Ui","Balance.ui")
RUTA_UI_ASISTENCIA = os.path.join("Frontend","Ui","Asistencia.ui")
RUTA_UI_CHICAS = os.path.join("Frontend","Ui","Chicas.ui")
RUTA_UI_POPUP_CHICAS = os.path.join("Frontend","Ui","PopUpChicas.ui")
RUTA_UI_POPUP_ASISTENCIA = os.path.join("Frontend","Ui","PopUpAsistencia.ui")
ALREADY_EXIST = """ERROR: Ya existen registros de algunas filas, Intente de nuevo\n Filas con error:\n """
SUCCEDED = """Se ha guardado la asistencia exitosamente, ya puedes cerrar la ventana"""
TEXTO_ERRORES = {"Already exists": ALREADY_EXIST, "Succeded": SUCCEDED}
RUTA_ICONO_VERDE = os.path.join("Frontend","ui","img", "succes.png" )