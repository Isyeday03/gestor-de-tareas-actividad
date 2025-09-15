"""
Lista de Tareas Simple - GUI con Tkinter
Aplicación básica para gestionar tareas con persistencia local.
"""

import tkinter as tk
from tkinter import messagebox
import os

ARCHIVO_TAREAS = "tareas.txt"
COLOR_AGREGAR = '#4CAF50'
COLOR_LIMPIAR = '#f44336'
COLOR_LIMPIAR_TODO = '#ff9800'
FUENTE_TITULO = ('Arial', 14, 'bold')
FUENTE_NORMAL = ('Arial', 11)

class GestorTareas:
    """Gestor de la lista de tareas (lógica, sin GUI)"""
    def __init__(self):
        self.tareas = []

    def agregar(self, tarea):
        if tarea and tarea not in self.tareas:
            self.tareas.append(tarea)
            return True
        return False

    def eliminar(self, indice):
        if 0 <= indice < len(self.tareas):
            del self.tareas[indice]
            return True
        return False

    def limpiar_todo(self):
        self.tareas.clear()

    def cargar(self, archivo=ARCHIVO_TAREAS):
        if os.path.exists(archivo):
            with open(archivo, "r", encoding="utf-8") as f:
                self.tareas = [linea.strip() for linea in f if linea.strip()]

    def guardar(self, archivo=ARCHIVO_TAREAS):
        with open(archivo, "w", encoding="utf-8") as f:
            for tarea in self.tareas:
                f.write(tarea + "\n")

class ListaTareasApp:
    """Aplicación GUI para gestionar tareas"""
    def __init__(self):
        self.gestor = GestorTareas()
        self.gestor.cargar()
        self.ventana = tk.Tk()
        self.ventana.title("Lista de Tareas Simple")
        self.ventana.geometry("400x370")
        self.crear_interfaz()
        self.actualizar_lista()

    def crear_interfaz(self):
        tk.Label(self.ventana, text="LISTA DE TAREAS", font=FUENTE_TITULO).pack(pady=10)
        tk.Label(self.ventana, text="Escribe una nueva tarea:").pack(pady=(0, 5))
        self.entrada_tarea = tk.Entry(self.ventana, width=40, font=FUENTE_NORMAL)
        self.entrada_tarea.pack(pady=5)
        self.entrada_tarea.bind('<Return>', lambda event: self.agregar_tarea())

        tk.Button(self.ventana, text="Agregar", command=self.agregar_tarea,
                  bg=COLOR_AGREGAR, fg='white', font=('Arial', 10)).pack(pady=5)

        tk.Label(self.ventana, text="Tareas:").pack(pady=(10, 5))
        self.lista = tk.Listbox(self.ventana, width=50, height=10)
        self.lista.pack(pady=5, padx=20, fill='both', expand=True)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)
        tk.Button(frame_botones, text="Limpiar Seleccionada", command=self.limpiar_seleccionada,
                  bg=COLOR_LIMPIAR, fg='white').pack(side='left', padx=5)
        tk.Button(frame_botones, text="Limpiar Todo", command=self.limpiar_todo,
                  bg=COLOR_LIMPIAR_TODO, fg='white').pack(side='left', padx=5)

    def agregar_tarea(self):
        tarea = self.entrada_tarea.get().strip()
        if not tarea:
            messagebox.showwarning("Advertencia", "Por favor escribe una tarea")
            return
        if self.gestor.agregar(tarea):
            self.actualizar_lista()
            self.gestor.guardar()
        else:
            messagebox.showinfo("Info", "La tarea ya existe o es inválida")
        self.entrada_tarea.delete(0, tk.END)
        self.entrada_tarea.focus()

    def limpiar_seleccionada(self):
        seleccion = self.lista.curselection()
        if not seleccion:
            messagebox.showinfo("Info", "Selecciona una tarea para eliminar")
            return
        indice = seleccion[0]
        if self.gestor.eliminar(indice):
            self.actualizar_lista()
            self.gestor.guardar()

    def limpiar_todo(self):
        if not self.gestor.tareas:
            messagebox.showinfo("Info", "No hay tareas para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Eliminar todas las tareas?"):
            self.gestor.limpiar_todo()
            self.actualizar_lista()
            self.gestor.guardar()

    def actualizar_lista(self):
        self.lista.delete(0, tk.END)
        for tarea in self.gestor.tareas:
            self.lista.insert(tk.END, tarea)

    def ejecutar(self):
        self.entrada_tarea.focus()
        self.ventana.mainloop()

if __name__ == "__main__":
    app = ListaTareasApp()
    app.ejecutar()