import tkinter as tk
import serial
ventana = tk.Tk()
ventana.title("Contador de autos con barrera")
ventana.geometry("800x600")

titulo=tk.Label(ventana, text="PARKING", font=("Times New Roman", 20, "bold"))
titulo.pack(pady=20)

ventana.mainloop()