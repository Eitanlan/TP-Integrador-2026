import tkinter as tk

ventana = tk.Tk()
ventana.title("Parking System")
ventana.geometry("600x380")
ventana.configure(bg="#1E1E2E")
ventana.resizable(False, False)

cant, barrera_alta = 0, False

def alternar():
    global cant, barrera_alta
    barrera_alta = not barrera_alta
    cant += 1 if barrera_alta else 0
    lbl_cant.config(text=str(cant))
    lbl_est.config(text="ALTA" if barrera_alta else "BAJA", fg="#4ADE80" if barrera_alta else "#F87171")
    btn.config(text="Bajar Barrera" if barrera_alta else "Levantar Barrera", bg="#EF4444" if barrera_alta else "#3B82F6")


tk.Label(ventana, text="CONTROL DE PARKING", font=("Segoe UI", 18, "bold"), fg="#FFF", bg="#1E1E2E").pack(pady=15)


f = tk.Frame(ventana, bg="#1E1E2E")
f.pack(pady=10)

c1 = tk.Frame(f, bg="#27293D", padx=25, pady=15); c1.pack(side="left", padx=10)
tk.Label(c1, text="AUTOS", font=("Segoe UI", 10, "bold"), fg="#9CA3AF", bg="#27293D").pack()
lbl_cant = tk.Label(c1, text="0", font=("Segoe UI", 36, "bold"), fg="#60A5FA", bg="#27293D")
lbl_cant.pack()

c2 = tk.Frame(f, bg="#27293D", padx=25, pady=15); c2.pack(side="left", padx=10)
tk.Label(c2, text="BARRERA", font=("Segoe UI", 10, "bold"), fg="#9CA3AF", bg="#27293D").pack()
lbl_est = tk.Label(c2, text="BAJA", font=("Segoe UI", 36, "bold"), fg="#F87171", bg="#27293D")
lbl_est.pack()


btn = tk.Button(ventana, text="Levantar Barrera", command=alternar, font=("Segoe UI", 11, "bold"), 
                fg="#FFF", bg="#3B82F6", activeforeground="#FFF", activebackground="#2563EB", relief="flat", bd=0, padx=20, pady=10, cursor="hand2")
btn.pack(pady=20)

ventana.mainloop()