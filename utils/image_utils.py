from PIL import Image, ImageDraw

def crear_icono_planta(tipo):
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

def crear_icono_elemento(tipo):
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
