import random
import math

class GeneticBeeOptimizer:
    def __init__(self, patio_width, patio_height, escala, plantas, num_colmenas, num_agua, num_azucar):
        self.patio_width = patio_width * escala
        self.patio_height = patio_height * escala
        self.escala = escala
        self.plantas = plantas
        self.num_colmenas = num_colmenas
        self.num_agua = num_agua
        self.num_azucar = num_azucar

        self.validar_capacidad_colmenas()

    def validar_capacidad_colmenas(self):
        area_total = (self.patio_width - 60) * (self.patio_height - 60)  # se deja margen
        area_por_colmena = math.pi * (100 ** 2)  # círculo de 2m (radio 100px)
        max_colmenas = int(area_total / area_por_colmena * 0.6)  # 60% eficiencia
        if self.num_colmenas > max_colmenas:
            print(f"El área del patio es insuficiente para {self.num_colmenas} colmenas. Máximo permitido: {max_colmenas}")
            raise ValueError(f"El área del patio es insuficiente para {self.num_colmenas} colmenas. Máximo permitido: {max_colmenas}")

    def generar_individuo(self):
        for _ in range(100):
            individuo = {"colmenas": [], "agua": [], "azucar": []}
            intentos = 0
            while len(individuo["colmenas"]) < self.num_colmenas and intentos < 1000:
                x, y = self.random_posicion()
                if self.validar_colmena(x, y, individuo["colmenas"]):
                    individuo["colmenas"].append({"x": x, "y": y})
                intentos += 1
            if len(individuo["colmenas"]) != self.num_colmenas:
                continue
            for key, cantidad in [("agua", self.num_agua), ("azucar", self.num_azucar)]:
                for _ in range(cantidad):
                    x, y = self.random_posicion()
                    individuo[key].append({"x": x, "y": y})
            return individuo
        raise Exception("No se pudo generar un individuo válido con todas las colmenas")

    def random_posicion(self):
        x = random.randint(30 + 50, int(self.patio_width - 50))
        y = random.randint(30 + 50, int(self.patio_height - 50))
        return x, y

    def validar_colmena(self, x, y, colmenas):
        for px, py, _ in self.plantas:
            if math.hypot(x - px, y - py) < 50:
                return False
        for c in colmenas:
            if math.hypot(x - c["x"], y - c["y"]) < 100:
                return False
        return True

    def calcular_aptitud(self, individuo):
        score = 0
        for colmena in individuo["colmenas"]:
            for px, py, _ in self.plantas:
                distancia = math.hypot(colmena["x"] - px, colmena["y"] - py)
                if distancia < 50:
                    score -= 50
                elif distancia < 200:
                    score += 5
        for i in range(len(individuo["colmenas"])):
            for j in range(i + 1, len(individuo["colmenas"])):
                if math.hypot(
                    individuo["colmenas"][i]["x"] - individuo["colmenas"][j]["x"],
                    individuo["colmenas"][i]["y"] - individuo["colmenas"][j]["y"]
                ) < 100:
                    score -= 100
        for colmena in individuo["colmenas"]:
            for recipiente in individuo["agua"] + individuo["azucar"]:
                if math.hypot(colmena["x"] - recipiente["x"], colmena["y"] - recipiente["y"]) < 150:
                    score += 10
        return score

    def cruzar(self, padre, madre):
        for _ in range(100):
            hijo = {"colmenas": [], "agua": [], "azucar": []}
            for key in hijo:
                lista1 = padre[key]
                lista2 = madre[key]
                mitad = len(lista1) // 2
                hijo[key] = lista1[:mitad] + lista2[mitad:]
            hijo_validado = {"colmenas": [], "agua": hijo["agua"], "azucar": hijo["azucar"]}
            intentos = 0
            for colmena in hijo["colmenas"]:
                if self.validar_colmena(colmena["x"], colmena["y"], hijo_validado["colmenas"]):
                    hijo_validado["colmenas"].append(colmena)
                intentos += 1
            if len(hijo_validado["colmenas"]) == self.num_colmenas:
                return hijo_validado
        return padre

    def mutar(self, individuo, prob):
        for intento in range(100):
            nuevas_colmenas = []
            for colmena in individuo["colmenas"]:
                if random.random() < prob:
                    for _ in range(20):
                        x, y = self.random_posicion()
                        if self.validar_colmena(x, y, nuevas_colmenas):
                            nuevas_colmenas.append({"x": x, "y": y})
                            break
                    else:
                        break
                else:
                    nuevas_colmenas.append(colmena)
            if len(nuevas_colmenas) == self.num_colmenas:
                individuo["colmenas"] = nuevas_colmenas
                break
        for key in ["agua", "azucar"]:
            for elemento in individuo[key]:
                if random.random() < prob:
                    elemento["x"], elemento["y"] = self.random_posicion()

    def evolucionar(self, poblacion, generaciones, prob_mutacion):
        for generacion in range(generaciones):
            print(f"Generación {generacion + 1}/{generaciones}")
            poblacion.sort(key=self.calcular_aptitud, reverse=True)
            nueva_generacion = []
            mitad = len(poblacion) // 2
            mejores = poblacion[:mitad]
            peores = poblacion[mitad:]
            while len(nueva_generacion) < mitad:
                padre = random.choice(mejores)
                madre = random.choice(mejores)
                hijo = self.cruzar(padre, madre)
                self.mutar(hijo, prob_mutacion)
                nueva_generacion.append(hijo)
            while len(nueva_generacion) < len(poblacion):
                padre = random.choice(peores)
                madre = random.choice(peores)
                hijo = self.cruzar(padre, madre)
                self.mutar(hijo, prob_mutacion)
                nueva_generacion.append(hijo)
            poblacion = nueva_generacion
        return sorted(poblacion, key=self.calcular_aptitud, reverse=True)[:5]
