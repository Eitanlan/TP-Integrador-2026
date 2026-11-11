import tkinter as tk
import serial
import time
from datetime import datetime

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
time.sleep(2)  

def send_command(cmd):
    arduino.write((cmd + '\n').encode())

def registrar_movimiento(texto):
    hora_actual = datetime.now().strftime("%H:%M:%S")
    mensaje_completo = f"[{hora_actual}] {texto}"
    lista_movimientos.insert(0, mensaje_completo)

def recibir_datos():
    global cant, est
    if arduino.in_waiting > 0:
        msg = arduino.readline().decode('utf-8').strip()
        
        if msg == "ENTRA":
            cant += 1
            lbl_cantidad.config(text=str(cant))
            registrar_movimiento("Auto entró al parking")
        elif msg == "SALE":
            cant -= 1
            lbl_cantidad.config(text=str(cant))
            registrar_movimiento("Auto salió del parking")
        elif msg == "BARRERA LEVANTADA" or msg == "AUTO DETECTADO" and est == "baja":
            est = "levantada"
            lbl_estado.config(text=est)
            actualizar_boton()
            registrar_movimiento("Barrera levantada")
        elif msg == "BARRERA BAJA" or msg == "AUTO DETECTADO" and est == "levantada":
            est = "baja"
            lbl_estado.config(text=est)
            actualizar_boton()
            registrar_movimiento("Barrera bajada")

    ventana.after(100, recibir_datos)

def cambiar_estado_boton():
    if est == "baja":
        send_command("SUBIR")
        registrar_movimiento("Comando enviado: SUBIR")
    else:
        send_command("BAJAR")
        registrar_movimiento("Comando enviado: BAJAR")

def actualizar_boton():
    if est == "baja":
        boton_bajar_levantar.config(text="SUBIR BARRERA")
    else:
        boton_bajar_levantar.config(text="BAJAR BARRERA")

ventana = tk.Tk()
ventana.title("Contador de autos con barrera")
ventana.geometry("800x600")

titulo = tk.Label(ventana, text="PARKING", font=("Times New Roman", 20, "bold"))
titulo.place(x=300, y=20)

cant = 0
est = "baja"

tk.Label(ventana, text="Cantidad de autos", font=("Times New Roman", 15, "bold")).place(x=20, y=150)
lbl_cantidad = tk.Label(ventana, text=str(cant), font=("Times New Roman", 50, "bold"))
lbl_cantidad.place(x=70, y=190)

tk.Label(ventana, text="Estado de la barrera", font=("Times New Roman", 15, "bold")).place(x=450, y=150)
lbl_estado = tk.Label(ventana, text=est, font=("Times New Roman", 47, "bold"))
lbl_estado.place(x=450, y=190)

boton_bajar_levantar = tk.Button(ventana, text="SUBIR BARRERA", command=cambiar_estado_boton)
boton_bajar_levantar.place(y=300, x=260)

tk.Label(ventana, text="Historial de Movimientos", font=("Times New Roman", 15, "bold")).place(x=20, y=360)
frame_historial = tk.Frame(ventana)
frame_historial.place(x=20, y=400, width=760, height=170)

scrollbar = tk.Scrollbar(frame_historial)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_movimientos = tk.Listbox(frame_historial, yscrollcommand=scrollbar.set, font=("Consolas", 10))
lista_movimientos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=lista_movimientos.yview)
ventana.after(100, recibir_datos)

ventana.mainloop()