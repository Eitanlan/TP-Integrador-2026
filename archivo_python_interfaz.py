import tkinter as tk
import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
time.sleep(2)  

def send_command(cmd):
    arduino.write((cmd + '\n').encode())
    return arduino.readline().decode().strip()

def receive_command():
    arduino.readline().decode().strip()



ventana = tk.Tk()
ventana.title("Contador de autos con barrera")
ventana.geometry("800x600")

titulo=tk.Label(ventana, text="PARKING", font=("Times New Roman", 20, "bold"))
titulo.place(x="300", y="20")

cant=0
if receive_command == "ENTRA":
    cant+=1
elif receive_command == "SALE":
    cant-=1



texto_cantidad = tk.Label(ventana, text="Cantidad de autos", font=("Times New Roman", 15, "bold")).place(x="20", y="150")
cantidad = tk.Label(ventana, text=cant, font=("Times New Roman", 50, "bold" )).place(x="70", y="190")

est="levantada"
texto_estado=tk.Label(ventana, text="Estado de la barrera"  , font=("Times New Roman", 15, "bold")).place(x="450", y="150")
estado = tk.Label(ventana, text=est,  font=("Times New Roman", 47, "bold")).place(x="450", y="190")
ventana.mainloop()