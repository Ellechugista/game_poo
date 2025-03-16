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
                    limpiar_consola()
                    self.player.mover_a(comando[1])
                    limpiar_consola()
                case "tomar":
                    limpiar_consola()
                    self.player.tomar_objeto(comando[1])
                    print(" ")
                case "abrir":
                    if len(comando) > 1:
                        if lugar_actual.objetos:
                            for item in lugar_actual.objetos:
                                if item.nombre.lower() == comando[1]:
                                    item.abrir(self.player)
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No hay ningun {comando[1]} para abrir")
                                print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes espesificar que quieres abrir")
                        print(" ")
                case "hablar":
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if p.nombre.lower() == comando[1]:
                                    limpiar_consola()
                                    p.hablar()
                                    print(" ")
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No hay nadie llamado {comando[1]}")
                                print(" ")
                        else:
                            limpiar_consola()
                            print("⌘No hay nadie con quien hablar")
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar con quien quieres hablar")
                        print(" ")
                case "inventario":
                    limpiar_consola()
                    self.player.mostrar_inventario()
                    print(" ")
                case "informacion":
                    limpiar_consola()
                    if len(comando) > 1:
                        if self.player.inventario:
                            for item in self.player.inventario:
                                print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    self.player.descrip_objeto(item)
                                    print(" ")
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No tienes {comando[1]} en tu inventario")
                                print(" ")
                        else:
                            limpiar_consola()
                            print("⌘No tienes nada en tu inventario")  
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar el objeto del que quieres informacion")  
                        print(" ")
                case "estadisticas":
                    limpiar_consola()
                    self.player.estadisticas()
                    print(" ")
                case "atacar":
                    #aqui se maneja la batalla
                    pass
                case "salir":
                    break
                case _:
                    limpiar_consola()
                    print("⌘Comando no valido")
                    print(" ")

if __name__ == "__main__":
    juego = game()
    juego.iniciar()

