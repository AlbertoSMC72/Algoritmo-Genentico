import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import math
from PIL import Image, ImageTk, ImageDraw


class PatioDesigner:
    def __init__(self, master):
        self.master = master
        master.title("Diseñador de Patio")

        self.escala = 50  # 1 metro = 50 píxeles
        self.colmenas_pos = []
        self.elementos_images = {}
        self.plant_images = []

        # Solicitar tamaño del patio
        self.patio_width = simpledialog.askfloat("Tamaño del Patio", "Ancho del patio (m):", minvalue=1, maxvalue=100)
        self.patio_height = simpledialog.askfloat("Tamaño del Patio", "Largo del patio (m):", minvalue=1, maxvalue=100)

        if not self.patio_width or not self.patio_height:
            messagebox.showerror("Error", "Debe ingresar dimensiones válidas")
            self.master.quit()
            return

        self.setup_ui()

    def crear_icono_planta(self, tipo):
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        if tipo == 'arbol':
            draw.polygon([(50, 10), (20, 50), (50, 90), (80, 50)], fill='green')
            draw.rectangle([45, 70, 55, 100], fill='brown')
        elif tipo == 'arbusto':
            draw.ellipse([10, 50, 90, 90], fill='darkgreen')
        elif tipo == 'flor':
            img = Image.open("assets/flor.png").convert("RGBA")
            img = img.resize((img.width // 30, img.height // 30), Image.Resampling.LANCZOS)

        return img

    def crear_icono_elemento(self, tipo):
        img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        if tipo == 'colmena':
            img = Image.open("assets/panal.png").convert("RGBA")
            img = img.resize((img.width // 2, img.height // 2), Image.Resampling.LANCZOS)
        elif tipo == 'bote_agua':
            draw.rectangle([20, 40, 80, 90], fill='lightblue')
            draw.arc([30, 20, 70, 50], 0, 180, fill='blue', width=3)
        elif tipo == 'bote_azucar':
            draw.rectangle([20, 40, 80, 90], fill='lightblue')
            draw.arc([30, 20, 70, 50], 0, 180, fill='blue', width=3)
            draw.rectangle([45, 30, 55, 40], fill='white')

        return img

    def setup_ui(self):
        canvas_width = int(self.patio_width * self.escala)
        canvas_height = int(self.patio_height * self.escala)

        # Frame superior con botones
        top_frame = tk.Frame(self.master)
        top_frame.pack(side=tk.TOP, fill=tk.X)

        for tipo in ['arbol', 'arbusto', 'flor']:
            img_pillow = self.crear_icono_planta(tipo)
            img_tk = ImageTk.PhotoImage(img_pillow)
            self.plant_images.append((tipo, img_tk))
            btn = tk.Button(top_frame, text=f"Agregar {tipo}",
                            image=img_tk, compound=tk.TOP,
                            command=lambda t=tipo: self.add_plant(t))
            btn.image = img_tk
            btn.pack(side=tk.LEFT, padx=5)

        finalizar_btn = tk.Button(top_frame, text="Finalizar Diseño", command=self.solicitar_elementos)
        finalizar_btn.pack(side=tk.RIGHT, padx=10)

        # Frame para canvas con scroll
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

        # Área del patio
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
        while True:
            num_colmenas = simpledialog.askinteger("Colmenas", "Número de colmenas:", minvalue=0, maxvalue=10)
            if num_colmenas is not None:
                break
        num_botes_agua = simpledialog.askinteger("Botes de Agua", "Número de botes de agua:", minvalue=0, maxvalue=10)
        num_botes_azucar = simpledialog.askinteger("Botes de Agua con Azúcar", "Número de botes con azúcar:", minvalue=0, maxvalue=10)
        self.colocar_elementos(num_colmenas, num_botes_agua, num_botes_azucar)

    def colocar_elementos(self, num_colmenas, num_botes_agua, num_botes_azucar):
        self.canvas.delete('colmena', 'bote_agua', 'bote_azucar', 'zona_segura')
        self.colmenas_pos.clear()

        tipos = [('colmena', num_colmenas), ('bote_agua', num_botes_agua), ('bote_azucar', num_botes_azucar)]

        for tipo, cantidad in tipos:
            img_pillow = self.crear_icono_elemento(tipo)
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
                                                    fill='lightgreen', outline='green',
                                                    width=2, tags='zona_segura')
                            self.canvas.create_image(x, y, image=img_tk, tags='colmena')
                            break
                    else:
                        self.canvas.create_image(x, y, image=img_tk, tags=tipo)
                        break


def main():
    root = tk.Tk()
    app = PatioDesigner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
