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
        elif msg == "BARRERA LEVANTADA" or (msg == "AUTO DETECTADO" and est == "baja"):
            est = "levantada"
            actualizar_interfaz()
            registrar_movimiento("Barrera levantada")
        elif msg == "BARRERA BAJA" or (msg == "AUTO DETECTADO" and est == "levantada"):
            est = "baja"
            actualizar_interfaz()
            registrar_movimiento("Barrera bajada")

    ventana.after(100, recibir_datos)

def cambiar_estado_boton():
    send_command("BOTON")

def actualizar_interfaz():
    lbl_estado.config(
        text="ALTA" if est == "levantada" else "BAJA",
        fg="#4ADE80" if est == "levantada" else "#F87171"
    )
    if est == "baja":
        boton_bajar_levantar.config(
            text="Levantar Barrera",
            bg="#3B82F6",
            activebackground="#2563EB"
        )
    else:
        boton_bajar_levantar.config(
            text="Bajar Barrera",
            bg="#EF4444",
            activebackground="#DC2626"
        )

ventana = tk.Tk()
ventana.title("Parking System")
ventana.geometry("680x560")
ventana.configure(bg="#1E1E2E")
ventana.resizable(False, False)

cant = 0
est = "baja"

tk.Label(ventana, text="CONTROL DE PARKING", font=("Segoe UI", 18, "bold"), fg="#FFF", bg="#1E1E2E").pack(pady=15)

f = tk.Frame(ventana, bg="#1E1E2E")
f.pack(pady=5)

c1 = tk.Frame(f, bg="#27293D", padx=25, pady=15)
c1.pack(side="left", padx=10)
tk.Label(c1, text="AUTOS", font=("Segoe UI", 10, "bold"), fg="#9CA3AF", bg="#27293D").pack()
lbl_cantidad = tk.Label(c1, text=str(cant), font=("Segoe UI", 36, "bold"), fg="#60A5FA", bg="#27293D")
lbl_cantidad.pack()

c2 = tk.Frame(f, bg="#27293D", padx=25, pady=15)
c2.pack(side="left", padx=10)
tk.Label(c2, text="BARRERA", font=("Segoe UI", 10, "bold"), fg="#9CA3AF", bg="#27293D").pack()
lbl_estado = tk.Label(c2, text="BAJA", font=("Segoe UI", 36, "bold"), fg="#F87171", bg="#27293D")
lbl_estado.pack()

boton_bajar_levantar = tk.Button(
    ventana, text="Levantar Barrera", command=cambiar_estado_boton, 
    font=("Segoe UI", 11, "bold"), fg="#FFF", bg="#3B82F6", 
    activeforeground="#FFF", activebackground="#2563EB", 
    relief="flat", bd=0, padx=20, pady=10, cursor="hand2"
)
boton_bajar_levantar.pack(pady=15)

tk.Label(ventana, text="Historial de Movimientos", font=("Segoe UI", 12, "bold"), fg="#FFF", bg="#1E1E2E").pack(anchor="w", padx=30)

frame_historial = tk.Frame(ventana, bg="#1E1E2E")
frame_historial.pack(pady=5, padx=30, fill="x")

scrollbar = tk.Scrollbar(frame_historial)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_movimientos = tk.Listbox(
    frame_historial, yscrollcommand=scrollbar.set, 
    font=("Consolas", 10), bg="#27293D", fg="#FFF", 
    selectbackground="#3B82F6", relief="flat", bd=0, height=6
)
lista_movimientos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=lista_movimientos.yview)
ventana.after(100, recibir_datos)

ventana.mainloop()