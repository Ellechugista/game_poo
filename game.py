# archivo principal
#esta es una prueba
from lugares import casa 
from personajes import entidad, dialogos_ejemplos
from player import player
import random
import os
def limpiar_consola():
    # Para Windows
    if os.name == 'nt':
        os.system('cls')

# clase de batallas
class batalla:

    def __init__(self, jugador, contrincante):
        self.jugador = jugador
        self.contrincante = contrincante
        self.turno = 0

    def validar_ganador(self):
        """esta funcion imprime si hay o no ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y none"""
        if self.contrincante.vida <= 0:
            print(f"{self.contrincante.nombre} ha muerto")
            return True
        elif self.jugador.vida <= 0:
            print(f"{self.jugador.nombre} ha muerto")
            return False
        else:
            return "ninguno"

    def actualizar_vista(self):
        """esta funcion imprime la vista del combate"""
        print(" ")
        print("⊢---------------------------------------------⊣")
        print(f"tu vida {self.jugador.nombre}: {self.jugador.vida}")
        print(f"vida de {self.contrincante.nombre}: {self.contrincante.vida}")
        print("⊢---------------------------------------------⊣")
        print(" ")
        
    def mostrar_estadisticas(self):
        """esta funcion imprime las estadisticas del contrincante"""
        print(" ")
        print("⍚Estadisticas del contrincante")
        print("Nombre: ", self.contrincante.nombre)
        print("Vida: ", self.contrincante.vida)
        print(f"Habilidades:  Ataque: {self.contrincante.habilidades['atacar']} Defenza: {self.contrincante.habilidades['defender']}")
        print("Nivel de combate: ", self.contrincante.nivel_combate)

    def iniciar(self):
        """esta funcion controla todo el flujo de una batalla incluyendo turnos y acciones"""
        batalla_acabada = self.validar_ganador()
        limpiar_consola()
        # cuando validar ganador sea "ninguno"
        while batalla_acabada == "ninguno":
            print("-------------------BATALLA-------------------")
            self.actualizar_vista()
            print("⍟Tu turno")
            print(" ")
            print("⌘¿Que deseas hacer?")
            respuesta = str(input("> ")).lower().split()

            if respuesta[0] == "atacar":
                self.jugador.atacar(self.contrincante)
                batalla_acabada = self.validar_ganador()
            elif respuesta[0] == "defender":
                self.jugador.defender()
                batalla_acabada = self.validar_ganador()
            elif respuesta[0] == "estadistica":
                self.mostrar_estadisticas()
                continue
            else:
                print("⌘escribe una accion valida")
                print(" ")
                continue
            # aqui va el movimiento enemigo
            eleccion = random.choice(["atacar", "defender"])
            print(" ")
            print("⍾Turno del enemigo")

            if eleccion == "atacar":
                self.contrincante.atacar(self.jugador)
            else:
                self.contrincante.defender()
            self.validar_ganador()
            self.turno += 1
            self.jugador.defensa_activa = False
            self.contrincante.defensa_activa = False
        # cuando batalla_acabada sea True osea gano el jugador
        if batalla_acabada:
            print("⌘Has ganado la batalla")
            puntos = (self.turno + self.jugador.vida) * 0.2
            self.jugador.nivel_combate += puntos
            print(" ")
            print(f"⌘Has ganado {puntos} puntos de experiencia")
        # cuando validar_ganador sea false osea perdio el jugador
        elif not batalla_acabada:
            print("⌘Has perdido la batalla")
            self.jugador.game_over()

# test
if __name__ == "__main__":
    lechuga = player("El Lechugista", casa,habilidades={"atacar": 10, "defender": 5},nivel_combate=10, vida=10)
    pablo = entidad("pablo", dialogos_ejemplos, vida=10, nivel_combate=10)
    print(" ")
    batalla_1 = batalla(lechuga, pablo)
    batalla_1.iniciar()