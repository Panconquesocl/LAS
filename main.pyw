from Frontend.Inicio import VentanaInicio
from Frontend.PagoDiario import VentanaPagoDiario
from Frontend.PagoSemanal import VentanaPagoSemanal
from PyQt5.QtWidgets import  QApplication
from Frontend.Balance import VentanaBalance
from Frontend.Asistencia import VentanaAsistencia
from Backend.Logica import Logica
import sys

if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)

    sys.__excepthook__ = hook
    app = QApplication([])

    
    

    VentanaInicio = VentanaInicio()
    
    VentanaPagoDiario = VentanaPagoDiario()
    VentanaPagoSemanal = VentanaPagoSemanal()
    #VentanaBalance = VentanaBalance()
    VentanaAsistencia = VentanaAsistencia()
    Logica = Logica()
    VentanaInicio.stack.addWidget(VentanaAsistencia)
    VentanaInicio.stack.addWidget(VentanaPagoDiario)
    VentanaInicio.stack.addWidget(VentanaPagoSemanal)
    #VentanaInicio.stack.setCurrentWidget(VentanaAsistencia)

    VentanaInicio.senal_abrir_pago_semanal.connect(lambda: VentanaInicio.change_widget(VentanaPagoSemanal))
    VentanaInicio.senal_abrir_pago_diario.connect(lambda: VentanaInicio.change_widget(VentanaPagoDiario))
    #VentanaInicio.senal_abrir_balance.connect(lambda: VentanaInicio.change_widget(VentanaBalance))
    VentanaInicio.senal_abrir_asistencia.connect(lambda: VentanaInicio.change_widget(VentanaAsistencia))
    VentanaPagoDiario.senal_volver.connect(VentanaInicio.mostrar)
    VentanaPagoSemanal.senal_volver.connect(VentanaInicio.mostrar)
    #VentanaBalance.senal_volver.connect(VentanaInicio.mostrar)
    VentanaAsistencia.senal_volver.connect(VentanaInicio.mostrar)
    VentanaAsistencia.senal_buscar.connect(Logica.solicitar_asistencia)
    Logica.senal_enviar_asistencia.connect(VentanaAsistencia.cargar_datos)
    Logica.senal_enviar_chicas.connect(VentanaAsistencia.set_chicas)
    #Logica.senal_enviar_chicas.connect(VentanaPagoDiario.set_chicas)
    Logica.senal_resultado_asistencia.connect(VentanaAsistencia.pop_result)
    VentanaAsistencia.senal_pedir_chicas.connect(Logica.solicitar_chicas)
    VentanaAsistencia.senal_enviar_asistencia.connect(Logica.recibir_asistencia)
    VentanaAsistencia.senal_borrar_asistencia.connect(Logica.borrar_asistencia)
    VentanaPagoDiario.senal_pedir_pagos.connect(Logica.solicitar_pagos)
    Logica.senal_enviar_pagos.connect(VentanaPagoDiario.cargar_datos)
    Logica.senal_enviar_pagos_semanal.connect(VentanaPagoSemanal.cargar_datos)
    VentanaAsistencia.senal_actualizar.connect(Logica.actualizar_asistencia)
    VentanaAsistencia.senal_agregar_chica.connect(Logica.agregar_chica)
    VentanaAsistencia.senal_cambiar_nombre_chica.connect(Logica.modificar_chicas)
    VentanaPagoDiario.senal_actualizar_pago.connect(Logica.actualizar_pagos)
    VentanaPagoSemanal.senal_pedir_pagos.connect(Logica.get_pago_semanal)

    VentanaInicio.show()
    app.exec()