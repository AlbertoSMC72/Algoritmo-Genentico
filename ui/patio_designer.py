import tkinter as tk
from tkinter import messagebox
import random
import math
from PIL import ImageTk
from utils.image_utils import crear_icono_planta, crear_icono_elemento
from logic.genetic_algorithm import GeneticBeeOptimizer

class PatioDesigner:
    def __init__(self, master):
        self.master = master
        master.title("Diseñador de Patio")
        self.escala = 50
        self.colmenas_pos = []
        self.elementos_images = {}
        self.plant_images = []
        self.elementos_plantas = []
        self.individuos_resultado = []
        self.indice_actual = 0
        self.solicitar_tamano_patio()

    def solicitar_tamano_patio(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Dimensiones del Patio")
        ventana.geometry("300x250")
        ventana.grab_set()

        tk.Label(ventana, text="Ancho del patio (m):").pack(pady=5)
        ancho_entry = tk.Entry(ventana)
        ancho_entry.pack()

        tk.Label(ventana, text="Largo del patio (m):").pack(pady=5)
        largo_entry = tk.Entry(ventana)
        largo_entry.pack()

        max_label = tk.Label(ventana, text="Máximo estimado: -")
        max_label.pack(pady=5)

        def actualizar_max_colmenas(*args):
            try:
                ancho = float(ancho_entry.get())
                largo = float(largo_entry.get())
                escala = 50
                patio_width_px = ancho * escala
                patio_height_px = largo * escala
                area_total = (patio_width_px - 60) * (patio_height_px - 60)
                area_por_colmena = math.pi * (100 ** 2)
                max_colmenas = int(area_total / area_por_colmena * 0.6)
                max_label.config(text=f"Máximo estimado: {max_colmenas} colmenas")
            except:
                max_label.config(text="Máximo estimado: -")

        ancho_entry.bind("<KeyRelease>", actualizar_max_colmenas)
        largo_entry.bind("<KeyRelease>", actualizar_max_colmenas)

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
                messagebox.showerror("Error", "Ingresa valores válidos para dimensiones y colmenas")

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
            btn = tk.Button(top_frame, text=f"Agregar {tipo}", image=img_tk, compound=tk.TOP, command=lambda t=tipo: self.add_plant(t))
            btn.image = img_tk
            btn.pack(side=tk.LEFT, padx=5)

        finalizar_btn = tk.Button(top_frame, text="Finalizar Diseño", command=self.solicitar_elementos)
        finalizar_btn.pack(side=tk.RIGHT, padx=10)

        canvas_frame = tk.Frame(self.master)
        canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(canvas_frame, bg='white', scrollregion=(0, 0, canvas_width + 50, canvas_height + 50))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        x_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL, command=self.canvas.xview)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        y_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL, command=self.canvas.yview)
        y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(xscrollcommand=x_scrollbar.set, yscrollcommand=y_scrollbar.set)

        self.canvas.create_rectangle(30, 30, 30 + canvas_width, 30 + canvas_height, fill='lightgreen', outline='black', width=2)

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
                x = random.randint(30 + 50, 30 + int(self.patio_width * self.escala) - 50)
                y = random.randint(30 + 50, 30 + int(self.patio_height * self.escala) - 50)
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
        ventana.geometry("300x300")
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
                self.colmenas = colmenas
                self.agua = agua
                self.azucar = azucar
                self.mostrar_boton_genetico()
            except ValueError:
                messagebox.showerror("Error", "Ingresa valores válidos entre 0 y 10")

        tk.Button(ventana, text="Aceptar", command=confirmar).pack(pady=10)

    def mostrar_boton_genetico(self):
        analizar_btn = tk.Button(self.master, text="Iniciar Análisis Genético", command=self.solicitar_parametros_geneticos)
        analizar_btn.pack(pady=10)

        siguiente_btn = tk.Button(self.master, text="Ver Siguiente Individuo", command=self.mostrar_siguiente_individuo)
        siguiente_btn.pack(pady=5)

    def solicitar_parametros_geneticos(self):
        ventana = tk.Toplevel(self.master)
        ventana.title("Parámetros Genéticos")
        ventana.geometry("300x250")
        ventana.grab_set()

        def crear_campo(label_text):
            tk.Label(ventana, text=label_text).pack(pady=5)
            entrada = tk.Entry(ventana)
            entrada.pack()
            return entrada

        poblacion_entry = crear_campo("Cantidad de individuos:")
        generaciones_entry = crear_campo("Cantidad de generaciones:")
        mutacion_entry = crear_campo("Porcentaje de mutación (0.1 = 10%):")

        def iniciar():
            try:
                poblacion = int(poblacion_entry.get())
                generaciones = int(generaciones_entry.get())
                mutacion = float(mutacion_entry.get())
                if poblacion < 1 or generaciones < 1 or not (0 <= mutacion <= 1):
                    raise ValueError
                ventana.destroy()
                self.iniciar_algoritmo_genetico(poblacion, generaciones, mutacion)
            except ValueError:
                messagebox.showerror("Error", "Valores no válidos")

        tk.Button(ventana, text="Ejecutar", command=iniciar).pack(pady=10)

    def obtener_plantas(self):
        plantas = []
        for item in self.canvas.find_withtag('planta'):
            tipo = self.canvas.gettags(item)[1]
            coords = self.canvas.coords(item)
            if coords:
                x, y = coords
                plantas.append((x, y, tipo))
        return plantas

    def iniciar_algoritmo_genetico(self, poblacion_n, generaciones, mutacion):
        self.canvas.delete('colmena', 'bote_agua', 'bote_azucar', 'zona_segura')
        plantas = self.obtener_plantas()
        optimizador = GeneticBeeOptimizer(
            patio_width=self.patio_width,
            patio_height=self.patio_height,
            escala=self.escala,
            plantas=plantas,
            num_colmenas=self.colmenas,
            num_agua=self.agua,
            num_azucar=self.azucar
        )

        poblacion = [optimizador.generar_individuo() for _ in range(poblacion_n)]
        mejores = optimizador.evolucionar(poblacion, generaciones, mutacion)
        self.individuos_resultado = mejores
        self.indice_actual = 0
        self.mostrar_siguiente_individuo()

    def mostrar_siguiente_individuo(self):
        if not self.individuos_resultado:
            return
        self.canvas.delete('colmena', 'bote_agua', 'bote_azucar', 'zona_segura')
        individuo = self.individuos_resultado[self.indice_actual]
        self.dibujar_individuo(individuo)
        self.indice_actual = (self.indice_actual + 1) % len(self.individuos_resultado)

    def dibujar_individuo(self, individuo):
        for tipo, items in individuo.items():
            tag = 'colmena' if tipo == 'colmenas' else f"bote_{tipo}" if tipo in ['agua', 'azucar'] else tipo
            if tag not in self.elementos_images:
                img_pillow = crear_icono_elemento(tag)
                self.elementos_images[tag] = ImageTk.PhotoImage(img_pillow)

            for elem in items:
                x, y = elem['x'], elem['y']
                if tag == 'colmena':
                    self.canvas.create_oval(x - 100, y - 100, x + 100, y + 100, outline='green', width=2, tags='zona_segura')
                self.canvas.create_image(x, y, image=self.elementos_images[tag], tags=tag)
