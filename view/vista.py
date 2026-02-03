import tkinter as tk
from tkinter import ttk
import threading
import time
import platform
import os
import pywhatkit
import datetime

def emitir_sonido():
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 500)
    else:
        os.system('play -nq -t alsa synth 0.5 sine 1000')

class Vista:
    def iniciar_verificacion_periodica(self, objetivo, tope, telefono):
        def tarea():
            while True:
                try:
                    print("[INFO] Realizando solicitud a https://dolarboliviahoy.com/...")
                    precio = float(self.controller.get_precio_compra("https://dolarboliviahoy.com/"))
                    print(f"[INFO] Precio actual: {precio} BOB (objetivo: {objetivo} / tope: {tope})")

                    if precio <= objetivo or precio >= tope:
                        now = datetime.datetime.now()
                        hora_envio = now.hour
                        minuto_envio = now.minute + 1
                        if minuto_envio == 60:
                            minuto_envio = 0
                            hora_envio = (hora_envio + 1) % 24

                        mensaje = f"El precio del dólar es de {precio} BOB"
                        pywhatkit.sendwhatmsg(telefono, mensaje, hora_envio, minuto_envio)

                        if precio <= objetivo:
                            print("[ALERTA] ¡Precio igual o menor al objetivo! Emitiendo sonido.")
                            self.result_label.config(text=f"¡Alerta por BAJO! Precio = {precio} BOB")
                        else:
                            print("[ALERTA] ¡Precio igual o mayor al tope! Emitiendo sonido.")
                            self.result_label.config(text=f"¡Alerta por ALTO! Precio = {precio} BOB")

                        emitir_sonido()
                        break
                    else:
                        self.result_label.config(text=f"Precio actual: {precio} BOB (esperando...)")

                except Exception as e:
                    print(f"[ERROR] Falló al obtener el precio: {e}")
                    self.result_label.config(text=f"Error: {e}")

                time.sleep(150)

        threading.Thread(target=tarea, daemon=True).start()

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title("Scraper de Precio Paralelo")
        self.root.geometry("500x300")

        ttk.Label(self.root, text="Los precios se obtienen de: https://dolarboliviahoy.com/").pack(pady=(20, 5))

        # Campo para el número de teléfono
        ttk.Label(self.root, text="Número de WhatsApp (con código, e.g. +5917...):").pack()
        self.telefono_entry = ttk.Entry(self.root, width=25)
        self.telefono_entry.pack(pady=(0,10))

        # Entrada de precio objetivo
        ttk.Label(self.root, text="Precio objetivo (alerta si es menor o igual):").pack()
        self.precio_objetivo_entry = ttk.Entry(self.root, width=20)
        self.precio_objetivo_entry.pack(pady=(0,10))

        # Entrada de precio tope
        ttk.Label(self.root, text="Precio tope (alerta si es mayor o igual):").pack()
        self.precio_tope_entry = ttk.Entry(self.root, width=20)
        self.precio_tope_entry.pack(pady=(0,10))

        # Botón
        ttk.Button(
            self.root,
            text="Iniciar monitoreo",
            command=self.obtener_parametros
        ).pack(pady=10)

        # Resultado
        self.result_label = ttk.Label(self.root, text="", font=("Arial", 12))
        self.result_label.pack(pady=5)

    def obtener_parametros(self):
        try:
            telefono = self.telefono_entry.get().strip()
            if not telefono.startswith("+"):
                self.result_label.config(text="El número debe incluir el código de país, e.g. +5917...")
                return

            objetivo = float(self.precio_objetivo_entry.get().replace(',', '.'))
            tope    = float(self.precio_tope_entry.get().replace(',', '.'))

            if objetivo >= tope:
                self.result_label.config(text="El objetivo debe ser menor que el tope.")
                return

            self.result_label.config(text="Esperando que el precio esté fuera del rango...")
            self.iniciar_verificacion_periodica(objetivo, tope, telefono)

        except ValueError:
            self.result_label.config(text="Ingresa los precios y el número correctamente.")

    def iniciar(self):
        self.root.mainloop()

