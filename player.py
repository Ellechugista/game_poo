import random
from utils import *
class player:   
    def __init__(self, nombre:str, lugar_actual, vida:float=10, habilidades:dict = {"atacar": 5, "defender": 5}, nivel_combate = 10):
        self.nombre = nombre
        self.vida = vida
        self.inventario = []
        self.habilidades = habilidades
        self.lugar_actual = lugar_actual 
        self.nivel_combate = nivel_combate
        self.defensa_activa = False

        
    def estadisticas(self):
        print(f"☺ Nombre: {self.nombre}")
        print(f"🎔 Vida: {self.vida}")
        print(f"⍚ Nivel de combate: {self.nivel_combate}")
        print(f"❖ Habilidades: Ataque:{self.habilidades['atacar']} Defensa:{self.habilidades['defender']}")
     
    def mover_a(self, direccion):
        limpiar_consola()
        """necesitara un parametro la cual es la direccion"""
        if direccion:
            if direccion in self.lugar_actual.conexiones:
                if self.lugar_actual.conexiones[direccion].bloqueado:
                    if self.lugar_actual.conexiones[direccion].razon:
                        limpiar_consola()
                        print(f"⌘No puedes ir a este lugar porque: {self.lugar_actual.conexiones[direccion].razon}")
                        print(" ")
                    else:
                        limpiar_consola()
                        print("⌘No puedes ir a este lugar")
                        print(" ")
                else:        
                    nuevo_lugar = self.lugar_actual.conexiones[direccion]
                    self.lugar_actual = nuevo_lugar
            else:
                limpiar_consola()
                print("No puedes ir en esa direccion")
                print(" ")
        else:
            print("El jugador no esta en ningun lugar")
            print(" ")
         
    def agregar_inventario(self, objeto):
        """esta funcion agrega un objeto al inventario del jugador"""
        limpiar_consola()
        for item in self.inventario:
            if item.nombre == objeto.nombre:
                item.cantidad += objeto.cantidad
                break
        else:
            self.inventario.append(objeto)
        print(f"⌘has tomado {objeto.nombre} (Cantidad: {objeto.cantidad})")
        print(" ")
        return True
       
    def extraer_inventario(self, objeto):
        """esta funcion elimina un objeto del inventario del jugador"""
        limpiar_consola()
        for item in self.inventario:
            if item.nombre == objeto.nombre:
                if item.cantidad > objeto.cantidad:
                    item.cantidad -= objeto.cantidad
                elif item.cantidad == objeto.cantidad:
                    self.inventario.remove(item)
                else:
                    print(f"No tienes suficiente cantidad de {objeto.nombre} en tu inventario")
                break
        else:
            print(f"No tienes {objeto.nombre} en tu inventario")
         
    def mostrar_inventario(self):
        """esta funcion muestra el inventario del jugador"""
        limpiar_consola()
        if self.inventario:
            print("Tienes:")
            for item in self.inventario:
                if item.cantidad == 1:
                    print(f"ⵚ {item.nombre}")
                else:
                    print(f"ⵚ {item.nombre} x{item.cantidad}")
        else:
            print("⌘no tienes nada en tu inventario")
            
    def descrip_objeto(self, objeto):
        limpiar_consola()
        objeto.describir()
        
    def tomar_objeto(self, objeto):
        limpiar_consola()
        for item in self.lugar_actual.objetos:
            if objeto == "cofre":
                print("⌘No puedes tomar un cofre")
                return False
            elif item.nombre.lower() == objeto:
                self.agregar_inventario(item)
                self.lugar_actual.quitar_objeto(item)
                break
        else:
            print(f"⌘No hay {objeto} en este lugar")
            
    def calcular_ventaja(self, contrincante):
        """esta funcion devuelve si hay ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y iguales si son iguales"""
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if self.nivel_combate > contrincante.nivel_combate:
            print(f"⌘¡Tienes ventaja sobre {contrincante.nombre}!")
            print(" ")
            return True
        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif self.nivel_combate < contrincante.nivel_combate:
            print(f"⌘¡{contrincante.nombre} tiene ventaja sobre ti!")
            print(" ")
            return False
        #cuando los niveles son iguales
        elif self.nivel_combate == contrincante.nivel_combate:
            print("⌘Niveles iguales - combate justo")
            print(" ")
            return "iguales"

    def atacar(self, contrincante):
        """Ataca a un contrincante basado en el nivel de combate"""
        #validamos si el contrincante ya está muerto si ya lo esta que retorne
        if contrincante.vida <= 0:
            print(f"{contrincante.nombre} ya está muerto")
            return
        # Validamos la ventaja según nivel de combate
        ventaja = self.calcular_ventaja(contrincante)
        #calculamos la diferencia de nivel entre rivales
        diferencial_nivel = (self.nivel_combate - contrincante.nivel_combate)
        if diferencial_nivel < 0:
            diferencial_nivel = diferencial_nivel * -1
            
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if ventaja == True:
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            #sacamos la diferencia de nivel entre rivales y generamos ventaja
            daño_base = self.habilidades["atacar"] * diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base)) - defenza_contrincante
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘Has causado {daño_final} de daño a {contrincante.nombre}")

        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif ventaja == False:
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            #sacamos la diferencia de nivel entre rivales y generamos desventaja
            daño_base = self.habilidades["atacar"] - diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))-defenza_contrincante
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘Has causado {daño_final} de daño a {contrincante.nombre} (reducido por defenza enemiga)")

        #cuando los niveles son iguales
        elif ventaja == "iguales":
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            daño_minimo = self.habilidades["atacar"] // 2
            daño_final = random.randint(daño_minimo, self.habilidades["atacar"]) - defenza_contrincante
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘Has causado {daño_final} de daño a {contrincante.nombre}")


    def defender(self):
        """esta funcion hace que el jugador se defienda cambie el booleano de defensa_activa a True pero al final de su turno se debe desactivar desde afuera"""
        self.defensa_activa = True
        print(f"{self.nombre} se defiende")
    
    def game_over(self):
        """esta funcion hace que el jugador muera"""
        print("⌘Has muerto")
        print(" ")
        print("⌘Game Over")
        return False





