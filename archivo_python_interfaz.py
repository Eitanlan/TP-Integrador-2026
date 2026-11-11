import tkinter as tk
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=0.1)
time.sleep(2)  

def send_command(cmd):
    arduino.write((cmd + '\n').encode())

def recibir_datos():
    global cant, est
    if arduino.in_waiting > 0:
        msg = arduino.readline().decode('utf-8').strip()
        
        if msg == "ENTRA":
            cant += 1
            lbl_cantidad.config(text=str(cant))
        elif msg == "SALE":
            cant -= 1
            lbl_cantidad.config(text=str(cant))
        elif msg == "AUTO DETECTADO":
            if est == "baja":
                est = "levantada"
            else:
                est = "baja"
            lbl_estado.config(text=est)
            actualizar_boton()

    ventana.after(100, recibir_datos)

def mandar_msg_subir():
    send_command("SUBIR")

def mandar_msg_bajar():
    send_command("BAJAR")

def cambiar_estado_boton():
    global est
    if est == "baja":
        mandar_msg_subir()
        est = "levantada"
    else:
        mandar_msg_bajar()
        est = "baja"
    lbl_estado.config(text=est)
    actualizar_boton()

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

ventana.after(100, recibir_datos)

ventana.mainloop()