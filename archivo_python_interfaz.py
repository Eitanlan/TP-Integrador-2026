import tkinter as tk
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
time.sleep(2)  

def send_command(cmd):
    arduino.write((cmd + '\n').encode())
    return arduino.readline().decode().strip()

def receive_command():
    return arduino.readline().decode('utf-8').strip()

def mandar_msg_subir():
    send_command("SUBIR")

def mandar_msg_bajar():
    send_command("BAJAR")

ventana = tk.Tk()
ventana.title("Contador de autos con barrera")
ventana.geometry("800x600")

titulo=tk.Label(ventana, text="PARKING", font=("Times New Roman", 20, "bold"))
titulo.place(x="300", y="20")

cant=0




texto_cantidad = tk.Label(ventana, text="Cantidad de autos", font=("Times New Roman", 15, "bold")).place(x="20", y="150")
cantidad = tk.Label(ventana, text=cant, font=("Times New Roman", 50, "bold" )).place(x="70", y="190")

est="baja"




boton_bajar_levantar = tk.Button(ventana)
boton_bajar_levantar.place(y="300", x="260")

texto_estado=tk.Label(ventana, text="Estado de la barrera"  , font=("Times New Roman", 15, "bold")).place(x="450", y="150")
estado = tk.Label(ventana, text=est,  font=("Times New Roman", 47, "bold")).place(x="450", y="190")

ventana.mainloop()
while True:
    if est=="baja":
        boton_bajar_levantar.config(text="SUBIR BARRERA")
        boton_bajar_levantar.config(command=mandar_msg_subir)
    elif est=="levantada":
        boton_bajar_levantar.config(text="BAJAR BARRERA")
        boton_bajar_levantar.config(command=mandar_msg_bajar)
    if receive_command == "ENTRA":
        cant+=1
    elif receive_command == "SALE":
        cant-=1

    if receive_command == "AUTO DETECTADO" and est=="baja":   
        est="levantada"
    elif receive_command == "AUTO DETECTADO" and est=="levantada":
        est="baja"
