import random
from objects import consumible, vestimenta
from utils import *
class player:   
    def __init__(self, nombre:str, lugar_actual, vida:float=100, habilidades:dict = {"atacar": 5, "defender": 5}, nivel_combate = 10, control_juego= None):
        self.nombre = nombre
        self.vida = round(vida, 1)
        self.inventario = []
        self.vestimentas = []
        self.peso_inventario = 0
        self.limite_inventario = 20
        self.habilidades = habilidades
        self.lugar_actual = lugar_actual 
        self.nivel_combate = round(nivel_combate, 2)
        self.defensa_activa = False
        self.control_juego = control_juego
        
        #seccion de misiones
        self.registro_misiones = []


    #misiones
    def agregar_mision(self, mision):
        """esta funcion agrega una mision al jugador como activa"""
        self.registro_misiones.append(mision)
        
    def mostrar_misiones(self):
        limpiar_consola()
        if self.registro_misiones:
            print("="*20)
            for mision in self.registro_misiones:
                if mision.estado == "activo":
                    print(f"#{mision.id} - {mision.nombre} [Mision activa]")
                else:
                    print(f"#{mision.id} - {mision.nombre} [Mision pasada]")
        else:
            print("⌘No tienes misiones activas")
        
    def estadisticas(self):
        print(f"{"-"*10}ESTADISTICAS{"-"*10}")
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
        peso = objeto.peso + self.peso_inventario
        if  peso > self.limite_inventario:
            print("⌘No puedes llevar mas objetos en tu inventario sobrepeso")
            print(" ")
            return False
        else:
            for item in self.inventario:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.inventario.append(objeto)
                
            self.peso_inventario += objeto.peso * objeto.cantidad
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
                    self.peso_inventario -= objeto.peso * objeto.cantidad

                elif item.cantidad == objeto.cantidad:
                    self.inventario.remove(item)
                    self.peso_inventario -= objeto.peso * objeto.cantidad

                elif item.cantidad < objeto.cantidad:
                    self.inventario.remove(item)
                    self.peso_inventario -= objeto.peso * objeto.cantidad
                    
                break
        else:
            print(f"No tienes {objeto.nombre} en tu inventario")
         
    def mostrar_inventario(self):
        """esta funcion muestra el inventario del jugador y permite hacer mucho mass"""
        limpiar_consola()
        while True:
            if self.inventario or self.vestimentas:
                print("Tienes:")
                for item in self.inventario:
                    if item.cantidad == 1:
                        print(f"ⵚ {item.nombre}")
                    else:
                        print(f"ⵚ {item.nombre} x{item.cantidad}")
                print(f"----------------------------------{self.peso_inventario}/{self.limite_inventario}")
                
                if self.vestimentas:
                    print(" ")
                    print("Tienes equipado:")
                    for item in self.vestimentas:
                        if item.tipo == "casco":
                            print(f"⛑ {item.nombre}")
                        elif item.tipo == "coraza":
                            print(f"🧥 {item.nombre}")
                        elif item.tipo == "guantes":
                            print(f"🧤 {item.nombre}")
                        elif item.tipo == "botas":
                            print(f"🥾 {item.nombre}")
                        elif item.tipo == "pantalones":
                            print(f"👖 {item.nombre}")
                        elif item.tipo == "mochila":
                            print(f"🎒 {item.nombre}")
                        elif item.tipo == "arma":
                            print(f"🗡 {item.nombre}")
                        elif item.tipo == "escudo":
                            print(f"🛡 {item.nombre}")
                        else:
                            print(f"🥼 {item.nombre}")
                else:
                    print(" ")
                    print("⌘no tienes nada equipado")
            else:
                print("⌘no tienes nada en tu inventario")
                break
            
            
            comando = str(input("> ")).lower().split()
            match comando[0]:
                case "equipar":
                    limpiar_consola()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                if isinstance(item, vestimenta):
                                    item.vestir(self)
                                    break
                        else:
                            print(f"⌘No tienes {objeto} en tu inventario")
                            print(" ")  
                    else:
                        print("⌘No has especificado el objeto a equipar")
                        print(" ")
                
                case "desequipar":
                    limpiar_consola()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        for item in self.vestimentas:
                            if item.nombre.lower() == objeto:
                                item.desequipar(self)
                                break
                        else:
                            print(f"⌘No tienes {objeto} en tu inventario")
                            print(" ")  
                    else:
                        print("⌘No has especificado el objeto a equipar")
                        print(" ")
                
                case "usar":
                    limpiar_consola()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        print (objeto)
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                if isinstance(item, consumible):
                                    item.usar(self)
                                    break
                                else:
                                    print(f"⌘No puedes usar {objeto}, no es un consumible")
                                    print(" ")
                                    break       
                        else:
                            print(f"⌘No tienes {objeto} en tu inventario")
                            print(" ")  
                    else:
                        print("⌘No has especificado el objeto a usar")
                        print(" ")
                case "informacion":
                    limpiar_consola()
                    if len(comando) > 1:
                        if self.inventario:
                            for item in self.inventario:
                                #print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    self.descrip_objeto(item)
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
                case "tirar":
                    limpiar_consola()
                    if len(comando) > 1:
                        objeto = comando[1].lower()
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                self.extraer_inventario(item)
                                self.lugar_actual.agregar_objeto(item)
                                print(f"⌘Has tirado {objeto}")
                                print(" ")
                                break
                        else:
                            print(f"⌘No tienes {objeto} en tu inventario")
                            print(" ")
                    else:
                        print("⌘No has especificado el objeto a tirar")
                        print(" ")
                case "salir":
                    limpiar_consola()
                    break
                case _:
                    limpiar_consola()
                    print("⌘Comando no valido")
                    print(" ")

    def agregar_vestimenta(self, objeto):
        """esta funcion agrega un objeto al inventario del jugador sin aplicar sus efectos"""
        limpiar_consola()
        for item in self.vestimentas:
            if item.tipo == objeto.tipo:
                print("⌘No puedes llevar dos veces la misma vestimenta")
                print(" ")
                return False  
        else:
            #aqui funciona todo correctamente y se agrega el objeto al inventario
            self.vestimentas.append(objeto)
            self.peso_inventario += objeto.peso * objeto.cantidad
            return True
            #no se actualiza el peso porque ya esta actualizado en la funcion de agregar_inventario pero cmomo se estrae del inventario se resta el peso 

    def extraer_vestimenta(self, objeto):
        """esta funcion elimina un objeto del inventario del jugador"""
        limpiar_consola()
        for item in self.vestimentas:
            if item.nombre == objeto.nombre:
                self.vestimentas.remove(objeto)
                self.peso_inventario -= objeto.peso * objeto.cantidad
                return True
        else:
            #aqui funciona todo correctamente y se agrega el objeto al inventario
            print("⌘No tienes esa vestimenta equipada")
            print(" ")
            return False  
            
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
                    chek= self.agregar_inventario(item)
                    if chek:
                        self.lugar_actual.quitar_objeto(item)
                        return
                    else:
                        return
        else:
            print(f"⌘No hay {objeto} aqui.")
            print("")
        
        
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
                #defenza total
                defenza_contrincante = contrincante.habilidades["defender"] * 1.5
            else:
                #la mitad de la defenza si no se cubre
                defenza_contrincante = contrincante.habilidades["defender"]
                
            #probabilidad de ataque en bace a nivel y deefensa
            probabilidad_ataque = diferencial_nivel - defenza_contrincante
            #aqui comprobamos que la probabilidad no sea negativa
            if probabilidad_ataque < 30:
                probabilidad_ataque = 0.30
            else:
                probabilidad_ataque = probabilidad_ataque/100
                
            probabilidad_ataque = probabilidad_ataque * 1.25
            
            #validamos si ataca o no probabilidad de ataque
            ataca = self.ataque_probabilidad(probabilidad_ataque)
            if ataca == False:
                print(f"⌘{self.nombre} ha fallado el ataque")
                return

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
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
                #defenza total
                defenza_contrincante = contrincante.habilidades["defender"] * 1.5
            else:
                #la mitad de la defenza si no se cubre
                defenza_contrincante = contrincante.habilidades["defender"]
                
            #probabilidad de ataque en base a nivel de de ataque y deefensa
            probabilidad_ataque = diferencial_nivel - defenza_contrincante
            #aqui comprobamos que la probabilidad no sea negativa
            if probabilidad_ataque < 25:
                probabilidad_ataque = 0.25
            else:
                probabilidad_ataque = probabilidad_ataque/100
            
            #validamos si ataca o no probabilidad de ataque
            ataca = self.ataque_probabilidad(probabilidad_ataque)
            if ataca == False:
                print(f"⌘{self.nombre} ha fallado el ataque")
                return

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘Has causado {daño_final} de daño a {contrincante.nombre}")

        #cuando los niveles son iguales
        elif ventaja == "iguales":
            #validamos si el contrincante se esta defendiendo
            if contrincante.defensa_activa:
                #defenza total
                defenza_contrincante = contrincante.habilidades["defender"] * 1.5
            else:
                #la mitad de la defenza si no se cubre
                defenza_contrincante = contrincante.habilidades["defender"]
                
            #probabilidad de ataque en base a nivel de de ataque y deefensa
            probabilidad_ataque = self.habilidades["atacar"] - defenza_contrincante
            #aqui comprobamos que la probabilidad no sea negativa
            if probabilidad_ataque < 30:
                probabilidad_ataque = 0.30
            else:
                probabilidad_ataque = probabilidad_ataque/100
            
            #validamos si ataca o no probabilidad de ataque
            ataca = self.ataque_probabilidad(probabilidad_ataque)
            if ataca == False:
                print(f"⌘{self.nombre} ha fallado el ataque")
                return

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            print(f"⌘Has causado {daño_final} de daño a {contrincante.nombre}")

    @classmethod
    def ataque_probabilidad(self, probabilidad:float):
        """esta funcion calcula la probabilidad de ataque y devuelve True o False"""
        return random.random() < probabilidad

    def defender(self):
        """esta funcion hace que el jugador se defienda cambie el booleano de defensa_activa a True pero al final de su turno se debe desactivar desde afuera"""
        self.defensa_activa = True
        print(f"{self.nombre} se defiende")
    
    def game_over(self):
        """esta funcion hace que el jugador muera"""
        print(r"""
▓█████▄ ▓█████ ▄▄▄      ▓█████▄ 
▒██▀ ██▌▓█   ▀▒████▄    ▒██▀ ██▌
░██   █▌▒███  ▒██  ▀█▄  ░██   █▌
░▓█▄   ▌▒▓█  ▄░██▄▄▄▄██ ░▓█▄   ▌
░▒████▓ ░▒████▒▓█   ▓██▒░▒████▓ 
 ▒▒▓  ▒ ░░ ▒░ ░▒▒   ▓▒█░ ▒▒▓  ▒ 
 ░ ▒  ▒  ░ ░  ░ ▒   ▒▒ ░ ░ ▒  ▒ 
 ░ ░  ░    ░    ░   ▒    ░ ░  ░ 
   ░       ░  ░     ░  ░   ░    
 ░                       ░      
""")
        print(" ")
        print("⌘Game Over")
        input("_")
        self.control_juego.game_over()





