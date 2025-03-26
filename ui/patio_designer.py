import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import math
from PIL import ImageTk
from utils.image_utils import crear_icono_planta, crear_icono_elemento

class PatioDesigner:
    def __init__(self, master):
        self.master = master
        master.title("Diseñador de Patio")

        self.escala = 50
        self.colmenas_pos = []
        self.elementos_images = {}
        self.plant_images = []

        self.solicitar_tamano_patio()

    def solicitar_tamano_patio(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Dimensiones del Patio")
        ventana.geometry("300x150")
        ventana.grab_set()

        tk.Label(ventana, text="Ancho del patio (m):").pack(pady=5)
        ancho_entry = tk.Entry(ventana)
        ancho_entry.pack()

        tk.Label(ventana, text="Largo del patio (m):").pack(pady=5)
        largo_entry = tk.Entry(ventana)
        largo_entry.pack()

        def confirmar():
            try:
                ancho = float(ancho_entry.get())
                largo = float(largo_entry.get())
                if ancho < 1 or largo < 1:
                    raise ValueError
                self.patio_width = ancho
                self.patio_height = largo
                ventana.destroy()
                self.setup_ui()
            except ValueError:
                messagebox.showerror("Error", "Ingresa valores válidos entre 1 y 100")

        tk.Button(ventana, text="Aceptar", command=confirmar).pack(pady=10)

    def setup_ui(self):
        canvas_width = int(self.patio_width * self.escala)
        canvas_height = int(self.patio_height * self.escala)

        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        for tipo in ['arbol', 'arbusto', 'flor']:
            img_pillow = crear_icono_planta(tipo)
            img_tk = ImageTk.PhotoImage(img_pillow)
            self.plant_images.append((tipo, img_tk))
            btn = tk.Button(top_frame, text=f"Agregar {tipo}",
                            image=img_tk, compound=tk.TOP,
                            command=lambda t=tipo: self.add_plant(t))
            btn.image = img_tk
            btn.pack(side=tk.LEFT, padx=5)

        finalizar_btn = tk.Button(top_frame, text="Finalizar Diseño", command=self.solicitar_elementos)
        finalizar_btn.pack(side=tk.RIGHT, padx=10)

        canvas_frame = tk.Frame(self.master)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='white',
                                scrollregion=(0, 0, canvas_width + 50, canvas_height + 50))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        x_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        self.canvas.create_rectangle(30, 30, 30 + canvas_width, 30 + canvas_height,
                                     fill='lightgreen', outline='black', width=2)

        for metro in range(int(self.patio_width) + 1):
            x = 30 + metro * self.escala
            self.canvas.create_line(x, 25, x, 30, fill='black')
            self.canvas.create_text(x, 15, text=f"{metro}m", font=('Arial', 8))

        for metro in range(int(self.patio_height) + 1):
            y = 30 + metro * self.escala
            self.canvas.create_line(25, y, 30, y, fill='black')
            self.canvas.create_text(10, y, text=f"{metro}m", font=('Arial', 8), anchor="w")

    def add_plant(self, tipo):
        for t, image in self.plant_images:
            if t == tipo:
                canvas_width = int(self.patio_width * self.escala)
                canvas_height = int(self.patio_height * self.escala)
                x = random.randint(30 + 50, 30 + canvas_width - 50)
                y = random.randint(30 + 50, 30 + canvas_height - 50)
                item = self.canvas.create_image(x, y, image=image, tags=('planta', tipo))
                self.canvas.tag_bind(item, '<ButtonPress-1>', self.start_drag)
                self.canvas.tag_bind(item, '<B1-Motion>', self.drag)

    def start_drag(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        self._drag_data = {"x": canvas_x, "y": canvas_y, "item": self.canvas.find_closest(canvas_x, canvas_y)[0]}

    def drag(self, event):
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        dx = canvas_x - self._drag_data["x"]
        dy = canvas_y - self._drag_data["y"]
        self.canvas.move(self._drag_data["item"], dx, dy)
        self._drag_data["x"] = canvas_x
        self._drag_data["y"] = canvas_y

    def solicitar_elementos(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Elementos del Patio")
        ventana.geometry("300x250")
        ventana.grab_set()

        def crear_campo(label_text):
            tk.Label(ventana, text=label_text).pack(pady=5)
            entrada = tk.Entry(ventana)
            entrada.pack()
            return entrada

        colmenas_entry = crear_campo("Número de colmenas:")
        agua_entry = crear_campo("Número de botes de agua:")
        azucar_entry = crear_campo("Número de botes con azúcar:")

        def confirmar():
            try:
                colmenas = int(colmenas_entry.get())
                agua = int(agua_entry.get())
                azucar = int(azucar_entry.get())
                if not (0 <= colmenas <= 10 and 0 <= agua <= 10 and 0 <= azucar <= 10):
                    raise ValueError
                ventana.destroy()
                self.colocar_elementos(colmenas, agua, azucar)
            except ValueError:
                messagebox.showerror("Error", "Ingresa valores válidos entre 0 y 10")

        tk.Button(ventana, text="Aceptar", command=confirmar).pack(pady=10)

    def colocar_elementos(self, num_colmenas, num_botes_agua, num_botes_azucar):
        self.canvas.delete('colmena', 'bote_agua', 'bote_azucar', 'zona_segura')
        self.colmenas_pos.clear()

        tipos = [('colmena', num_colmenas), ('bote_agua', num_botes_agua), ('bote_azucar', num_botes_azucar)]

        for tipo, cantidad in tipos:
            img_pillow = crear_icono_elemento(tipo)
            img_tk = ImageTk.PhotoImage(img_pillow)
            self.elementos_images[tipo] = img_tk

            for _ in range(cantidad):
                for _ in range(100):
                    x = random.randint(30 + 50, 30 + int(self.patio_width * self.escala) - 50)
                    y = random.randint(30 + 50, 30 + int(self.patio_height * self.escala) - 50)
                    if tipo == 'colmena':
                        if all(math.hypot(x - cx, y - cy) >= 100 for cx, cy in self.colmenas_pos):
                            self.colmenas_pos.append((x, y))
                            self.canvas.create_oval(x - 100, y - 100, x + 100, y + 100,
                                                    outline='green', width=2, tags='zona_segura')
                            self.canvas.create_image(x, y, image=img_tk, tags='colmena')
                            break
                    else:
                        self.canvas.create_image(x, y, image=img_tk, tags=tipo)
                        break