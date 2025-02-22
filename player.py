import random
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
        "necesitara un parametro la cual es la direccion"
        if direccion:
            if direccion in self.lugar_actual.conexiones:
                nuevo_lugar = self.lugar_actual.conexiones[direccion]
                self.lugar_actual = nuevo_lugar
                self.lugar_actual.presentar_lugar()
            else:
                print("No puedes ir en esa direccion")
        else:
            print("El jugador no esta en ningun lugar")
         
    def agregar_inventario(self, objeto):
        for item in self.inventario:
            if item.nombre == objeto.nombre:
                item.cantidad += objeto.cantidad
                break
        else:
            self.inventario.append(objeto)
        print(f"has tomado el {objeto.nombre} (Cantidad: {objeto.cantidad})")
       
    def quitar_inventario(self, objeto):
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
        if self.inventario:
            print("Tienes:")
            for item in self.inventario:
                if item.cantidad == 0:
                    print(f"- {item.nombre}")
                else:
                    print(f"- {item.nombre} > {item.cantidad}")
        else:
            print("no tienes nada en tu inventario")
            
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
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if ventaja == True:
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                defenza_contrincante = contrincante.habilidades["defender"]*0.7
            else:
                defenza_contrincante = 0
            #sacamos la diferencia de nivel entre rivales y generamos ventaja
            diferencial_nivel = self.nivel_combate - contrincante.nivel_combate
            daño_base = self.habilidades["atacar"] * diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = random.randint(daño_minimo, daño_base) - defenza_contrincante
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
            diferencial_nivel = self.nivel_combate - contrincante.nivel_combate
            daño_base = self.habilidades["atacar"] - diferencial_nivel
            daño_minimo = daño_base // 2
            daño_final = (random.randint(daño_minimo, daño_base)-defenza_contrincante)
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
        print(" ")



