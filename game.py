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
        contador = 0
        
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
                    if self.player.inventario:
                        for item in self.player.inventario:
                            if item.nombre == comando[1]:
                                self.player.descrip_objeto(item)
                                break
                        else:
                            print(f"No tienes {comando[1]} en tu inventario")
                    else:
                        print("No tienes nada en tu inventario")
                case "estadisticas":
                    self.player.estadisticas()
                case "salir":
                    break
                case _:
                    print("Comando no valido")
            
            # Incrementar el contador y limpiar la consola cada 3 iteraciones
            contador += 1
            if contador % 3 == 0:
                limpiar_consola()

if __name__ == "__main__":
    juego = game()
    juego.iniciar()

