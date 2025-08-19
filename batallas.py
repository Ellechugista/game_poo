from lugares import casa 
from personajes import *
from player import player
from utils import *
import random
# clase de batallas
class batalla:

    def __init__(self, jugador, contrincante):
        self.jugador = jugador
        self.contrincante = contrincante
        self.ganador = None
        self.vivo = None
        self.batalla_injusta = None
        self.turno = 0
        self.xp = None
        
    def informe_batalla(self):
        """esta funcion imprime el informe de la batalla, luego de que ya se ha terminado"""
        if not self.batalla_injusta:
            print("⊢---------------------Informes----------------------⊣")
            print(f"⌘Batalla entre {self.jugador.nombre} y {self.contrincante.nombre}")
            print(f"⌘Turnos: {self.turno}")
            print(f"⌘Ganador: {self.ganador}")
            print(f"⌘Puntos de experiencia ganados: {self.xp}")
            if self.vivo:
                print("⌘El contrincante ha sido dejado vivo")
            elif not self.vivo:
                print("⌘El contrincante ha sido destruido")
            else:
                print("⌘Indeterminado")
            print("⊢---------------------------------------------------⊣")
            print(" ")
        else:
            print("⊢---------------------Informes----------------------⊣")
            print(f"⌘Batalla entre {self.jugador.nombre} y {self.contrincante.nombre}")
            print(f"⌘Turnos: {self.turno}")
            print(f"⌘Batalla Injusta: {self.batalla_injusta}")
            print("⊢---------------------------------------------------⊣")
            print(" ")

    def validar_ganador(self):
        """esta funcion imprime si hay o no ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y none"""
        if self.contrincante.vida == 0:
            print(f"{self.contrincante.nombre} ha muerto")
            return True
        elif self.jugador.vida == 0:
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
        #aqui tenemos que cambiar el animo del personaje con quien peliemos a enojado
        self.contrincante.animo -= 35
        self.contrincante.calcular_animo()
        batalla_acabada = self.validar_ganador()
        limpiar_consola()
        if self.contrincante.vida <= 0:
            self.batalla_injusta = True
            print(f"{self.contrincante.nombre} esta incapacitado para el combate.")
            print(" ")
            return
        
        # cuando validar ganador sea "ninguno"
        while batalla_acabada == "ninguno":
            print("-------------------BATALLA-------------------")
            self.actualizar_vista()
            print("⍟Tu turno")
            print(" ")
            print("⌘¿Que deseas hacer?")
            respuesta = str(input("> ")).lower().split()
            limpiar_consola()
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
            batalla_acabada = self.validar_ganador()
            self.turno += 1
            self.jugador.defensa_activa = False
            self.contrincante.defensa_activa = False
        
        # cuando batalla_acabada sea True osea gano el jugador
        if batalla_acabada:
            self.ganador = self.jugador.nombre
            limpiar_consola()
            print("⌘Has ganado la batalla")
            print(" ")
            
            #bucle de respuesta
            while True:
                print("⌘¿Deseas dejar vivo al contrincante? si/no")
                respuesta = str(input("> ")).lower().split()
                if respuesta[0] == "no":
                    lugar_actual = self.jugador.lugar_actual
                    if self.contrincante in lugar_actual.presentes:
                        lugar_actual.quitar_entidad(self.contrincante)
                        self.vivo = False
                        limpiar_consola()
                        print("⌘Culminas el sufrimiento de tu contrincante, deseandole una mejor vida en el mas alla")
                        print(" ")
                    else:
                        limpiar_consola()
                        print("El contrincante ya no se encuntra en el lugar.")
                        self.vivo = 0
                    
                    #ahora como el sujeto murio debe dropearnos su pequeño inventario
                    self.contrincante.luteador(self.jugador)
                    break
                                        
                elif respuesta[0] == "si":
                    self.vivo = True
                    
                    #aqui si hay una probabilidad de que el contrincante suelte un item de su inventario
                    recompensas = self.contrincante.soltar_azar()
                    if recompensas or not recompensas == None:
                        for item in recompensas:
                            print(f"⌘{self.contrincante.nombre} ha dejado caer {item.nombre}.")
                            print("")
                        
                        self.jugador.lugar_actual.agregar_objeto(recompensas) 
                    
                    print("⌘El contrincante se aleja gravemente herido")
                    break
                else:
                    limpiar_consola()
                    print("⌘Digita una opcion vlida")
                    print("")
                    continue
                
            puntos = ((self.turno*0.25) + (self.jugador.vida)*0.50) * 0.20
            puntos = round(puntos, 2)
            self.jugador.nivel_combate += puntos
            self.xp = puntos
            print(" ")
            print(f"⌘Has ganado {puntos} puntos de experiencia")
        # cuando validar_ganador sea false osea perdio el jugador
        elif not batalla_acabada:
            self.ganador = self.contrincante.nombre
            limpiar_consola()
            print("⌘Has perdido la batalla")
            #debemos actualizar el animo del personaje con quien peliemos a feliz porque gano
            self.contrincante.animo += 50
            self.jugador.game_over()

# test
if __name__ == "__main__":
    lechuga = player("El Lechugista", casa,habilidades={"atacar": 10, "defender": 10},nivel_combate=18, vida=100)
    pablo = humano("pablo", dialogos_ejemplos, vida=100, nivel_combate=20, habilidades={"atacar": 10, "defender": 10})
    print(" ")
    batalla_1 = batalla(lechuga, pablo)
    batalla_1.iniciar()