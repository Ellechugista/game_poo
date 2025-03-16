from objects import *
from personajes import *
class lugar:  
    def __init__(self, nombre:str, descripcion:str):
        self.nombre = nombre
        self.descripcion = descripcion
        self.presentes = []
        self.objetos = []
        self.conexiones = {}

    def presentar_conexiones(self):
        """esto es para mostrar las conexiones disponibles del lugar"""
        print("Puedes ir a:")
        for direccion, lugar in self.conexiones.items():
            print(f" ⵥ {direccion}: {lugar.nombre}")

    # objetos en el lugar
    def agregar_objeto(self, objeto):
        """esta funcion sirve para agregar un objeto al lugar, solo uno a la vez"""
        for item in self.objetos:
            if item.nombre == objeto.nombre:
                item.cantidad += objeto.cantidad
                return True
        else:
            self.objetos.append(objeto)
            return True

    def quitar_objeto(self, objeto):
        if objeto in self.objetos:
            self.objetos.remove(objeto)
            return True
        else:
            return False

    def presentar_lugar(self):
        """esto es para mostrar la info del lugar"""
        # informacion del lugar
        print(f"》Te encuentras en {self.nombre}")
        print(" ")
        print(self.descripcion)
        print(" ")
        # objetos presentes
        if self.objetos:
            print("Aqui hay:")
            for item in self.objetos:
                if item.cantidad == 1:
                    print(f"ⵚ {item.nombre}")
                else:
                    print(f"ⵚ {item.nombre} (x{item.cantidad})")
        else:
            print("⌘No hay items en este lugar")
        print(" ")
        # presentar los presentes
        if self.presentes:
            print("Puedes ver:")
            for p in self.presentes:
                print(f" ¤ {p.nombre}")
        else:
            print("⌘Aqui no hay nadie")
        print(" ")
        self.presentar_conexiones()
        print(" ")

    # agregar un personaje a un lugar, es decir, agregar un presente
    def agregar_entidad(self, personaje):  
        self.presentes.append(personaje)

    def quitar_entidad(self, personaje):
        self.presentes.remove(personaje)

    def conectar_lugar(self, direccion:str, lugar_destino):
        """esto añade al diccionario direcciones la direccion correspondiente y el objeto lugar para conectarlos"""
        self.conexiones[direccion] = lugar_destino

#valle lidien
casa = lugar("Tu casa", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
cumbre_rocosa = lugar("Cumbre rocosa", "Una sobra se alza en el horizonte, es la cumbre de una seca e infertil montalla, donde el viento sopla con fuerza gritando los nombres de los perdidos")
valle_lidien = lugar("Valle de Lidien", "Un valle amarillo y seco, refleja un deterioro con el tiempo como si la estacion del lugar fuera siempre la nostalgia de un crudo otoño, su poblacion tambien se ve disminuida mostrando solo unas cuantas casas de madera secas y desgastadas")
#conectando lugares
casa.conectar_lugar("oeste", cumbre_rocosa)
casa.conectar_lugar("este", valle_lidien)
cumbre_rocosa.conectar_lugar("este", casa)
valle_lidien.conectar_lugar("oeste", casa)
#agregrando objetos a los lugares
cofre_normal = cofre()
cofre_normal.agregar([monedax10.clonar(), guantes_cuero.clonar()])
casa.agregar_objeto(cofre_normal)
casa.agregar_objeto(botas_cuero.clonar())
#agregamos a los personajes
casa.agregar_entidad(laura)



if __name__ == "__main__":
    patio = lugar("Patio trasero", "un enorme porton abre un inmenso bosque verde con arboles")

    casa = lugar("Casa Mariano eximilianl Urrutia", "Esta es tu casa aqui vas a lograr ver tus lugros y dormir para reponerte de tu aventura")
    casa.conectar_lugar("este", patio)
    patio.conectar_lugar("oeste", casa)

    casa.presentar_lugar()
