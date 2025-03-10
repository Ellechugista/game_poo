# archivo principal
#esta es una prueba
from lugares import casa 
from personajes import *
from player import *
from batallas import *
from utils import *
import random
import os

class game:
    def __init__(self):
        self.player = player("Mariano", casa)
        self.enemigos_derrotados = 0

    def limpiar_consola(self):
        """Limpia la consola"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def iniciar(self):
        #aqui se maneja el input del jugador prara ver que  accion quiere hacer dentro de cada escenario y se le muestra la informacion en desarrollo
        while True:
            lugar_actual = self.player.lugar_actual
            lugar_actual.presentar_lugar()
            comando = str(input("> ")).lower().split()
            match comando[0]:
                case "ir":
                    self.player.mover_a(comando[1])
                case "tomar":
                    self.player.tomar_objeto(comando[1])
                case "hablar":
                    if lugar_actual.presentes:
                        for p in lugar_actual.presentes:
                            if p.nombre == comando[1]:
                                p.hablar()
                                break
                        else:
                            print(f"No hay nadie llamado {comando[1]}")
                    else:
                        print("No hay nadie con quien hablar")
                case "inventario":
                    self.player.mostrar_inventario()
                case "informacion":
                    if len(comando) > 1:
                        if self.player.inventario:
                            for item in self.player.inventario:
                                print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    self.player.descrip_objeto(item)
                                    break
                            else:
                                limpiar_consola()
                                print(f"No tienes {comando[1]} en tu inventario")
                        else:
                            limpiar_consola()
                            print("No tienes nada en tu inventario")  
                    else:
                        limpiar_consola()
                        print("Debes especificar el objeto del que quieres informacion")  
                    
                case "estadisticas":
                    self.player.estadisticas()
                case "salir":
                    break
                case _:
                    limpiar_consola()
                    print("Comando no valido")

if __name__ == "__main__":
    juego = game()
    juego.iniciar()

