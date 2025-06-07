import tkinter as tk
from tkinter import messagebox
import threading
import asyncio
from logic import registrar_uso, obtener_mensaje_reactivo, inicializar_bd

def iniciar_interfaz():
    inicializar_bd()
    ventana = tk.Tk()
    ventana.title("Desconéctate")
    ventana.geometry("400x300")

    tk.Label(ventana, text="Minutos usados hoy en redes sociales:").pack(pady=10)
    entrada_minutos = tk.Entry(ventana)
    entrada_minutos.pack(pady=5)

    def guardar():
        try:
            minutos = int(entrada_minutos.get())

            def tarea():
                registrar_uso(minutos)
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                mensaje = loop.run_until_complete(obtener_mensaje_reactivo(minutos))
                loop.close()
                ventana.after(0, lambda: messagebox.showinfo("Aviso", mensaje))

            threading.Thread(target=tarea).start()
            messagebox.showinfo("Guardado", "Uso registrado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa un número entero válido.")
        except Exception as e:
            messagebox.showerror("Error inesperado", str(e))

    tk.Button(ventana, text="Guardar uso", command=guardar).pack(pady=20)
    ventana.mainloop()
