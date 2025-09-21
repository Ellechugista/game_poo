import random
from objects import consumible, vestimenta
from utils import *
#GUI de consola
from rich.panel import Panel
from rich.text import Text

class player:   
    def __init__(self, nombre:str, lugar_actual, vida:float=100, habilidades:dict = {"atacar": 5, "defender": 5}, nivel_combate = 5, control_juego= None):
        self.nombre = nombre
        self.vida = round(vida, 1)
        self.vida_limite = round(vida, 1)
        self.inventario = []
        self.vestimentas = []
        self.peso_inventario = 0
        self.limite_inventario = 30
        self.habilidades = habilidades
        self.lugar_actual = lugar_actual 
        self.nivel_combate = round(nivel_combate, 2)
        self.defensa_activa = False
        self.control_juego = control_juego
        
        #seccion de misiones
        self.registro_misiones = []
        
        #diseños
        self.diseño= diagramas


    #misiones
    def agregar_mision(self, mision):
        """esta funcion agrega una mision al jugador como activa"""
        self.registro_misiones.append(mision)
        
    def mostrar_misiones(self):
        consola.clear()
        text = ""
        if self.registro_misiones:
            for mision in self.registro_misiones[-5:]:
                if mision.estado == "activo":
                    text += f"[bright_cyan]⌭ {mision.id}[/] - {mision.nombre} [green][Mision activa][/]\n"
                else:
                    text += f"[bright_cyan]⌭ {mision.id}[/] - {mision.nombre} [bright_black][Mision pasada][/]\n"
        else:
            text += "[bright_black]⌬ No tienes misiones activas[/]"
        
        
        return Panel(Text.from_markup(text, style="white"), title="Misiones", style="dark_green",)
             
    def estadisticas(self):
        text = Text.from_markup(f"[yellow1]♦[/] Nombre: {self.nombre}\n[red]♥[/] Vida: {self.vida}/{self.vida_limite}\n[cyan1]♣[/] Nivel de combate: {self.nivel_combate}\n[chartreuse4]♠[/] Habilidades: Ataque:{self.habilidades['atacar']} Defensa:{self.habilidades['defender']} \n[orange4]〄[/] Inventario: {self.peso_inventario}g/{self.limite_inventario}g")
        
        return Panel(text, title="Estadisticas Player", style="white")
     
    def mover_a(self, direccion):
        consola.clear()
        """necesitara un parametro la cual es la direccion"""
        if direccion:
            if direccion in self.lugar_actual.conexiones:
                if self.lugar_actual.conexiones[direccion].bloqueado:
                    if self.lugar_actual.conexiones[direccion].razon:
                        return Panel(f"⊠ No puedes ir a este lugar porque: {self.lugar_actual.conexiones[direccion].razon}", style="coin")
                    else:
                        return Panel("⊠ No puedes ir a este lugar", style="coin")
                else:        
                    nuevo_lugar = self.lugar_actual.conexiones[direccion]
                    self.lugar_actual = nuevo_lugar
            else:
                return Panel("⌬ No puedes ir en esa direccion", style="info")
        else:
            print("⌬ El jugador no esta en ningun lugar")
            print(" ")
         
    def agregar_inventario(self, objeto):
        """esta funcion agrega un objeto al inventario del jugador"""
        consola.clear()
        peso = (objeto.peso*objeto.cantidad) + self.peso_inventario
        if  peso > self.limite_inventario:
            return Panel("⌬ No puedes llevar mas objetos en tu inventario sobrepeso", style="alert")
        else:
            for item in self.inventario:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.inventario.append(objeto)
                
            self.peso_inventario += objeto.peso * objeto.cantidad
            return True
       
    def extraer_inventario(self, objeto, cantidad:int = None):
        """esta funcion elimina un objeto del inventario del jugador"""
        consola.clear()
        for item in self.inventario:
            if item.nombre == objeto.nombre:
                if item.cantidad > (objeto.cantidad if not cantidad else cantidad):
                    item.cantidad -= objeto.cantidad if not cantidad else cantidad
                    self.peso_inventario -= objeto.peso * (objeto.cantidad if not cantidad else cantidad)

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
        consola.clear()
        #GUI structure
        view = Layout()
        
        #altura
        view.split_column(
            Layout(name="response", size=3, visible=False),
            Layout(name="centrado", size=28)
        )
        
        #secciones
        view["centrado"].split_row(
            Layout(name="inventario"),
            Layout(name="equipados")
        )
        
        view["centrado"]["equipados"].split_column(
            Layout(name="objetos", size=11),
            Layout(name="estadisticas", size=17)
        )
        
        view["centrado"]["equipados"]["estadisticas"].split_row(
            Layout(name="diagrama"),
            Layout(name="estadistica", ratio=2)
        )
        
        while True:
            if self.inventario or self.vestimentas:
                text_inventario=f"[b]Tienes:[/]\n"
                for item in self.inventario:
                    if item.cantidad == 1:
                        text_inventario += f"[green4]ⵚ[/] [white]{item.nombre}[/]\n"
                    else:
                        text_inventario += f"[green4]ⵚ[/] [white]{item.nombre} x({item.cantidad})[/]\n"

                text_equipados = f"Tienes equipado:\n"
                if self.vestimentas:
                    for item in self.vestimentas:
                        if item.tipo == "casco":
                            text_equipados += f"⛑ {item.nombre}\n"
                        elif item.tipo == "coraza":
                            text_equipados += f"🧥 {item.nombre}\n"
                        elif item.tipo == "guantes":
                            text_equipados += f"🧤 {item.nombre}\n"
                        elif item.tipo == "botas":
                            text_equipados += f"🥾 {item.nombre}\n"
                        elif item.tipo == "pantalones":
                            text_equipados += f"👖 {item.nombre}\n"
                        elif item.tipo == "mochila":
                            text_equipados += f"🎒 {item.nombre}\n"
                        elif item.tipo == "arma":
                            text_equipados += f"🗡 {item.nombre}\n"
                        elif item.tipo == "escudo":
                            text_equipados += f"🛡 {item.nombre}\n"
                        else:
                            text_equipados += f"🥼 {item.nombre}\n"
                else:
                    text_equipados = "[bright_black]⌬ No tienes nada equipado[/]"
                
                #actualizamos la seccion de inventario
                view["centrado"]["inventario"].update(Panel(Text.from_markup(text_inventario), title="Inventario", style="dark_cyan", subtitle=f"Peso: {self.peso_inventario}k/{self.limite_inventario}k", subtitle_align="right"))
                
                #actualizamos la seccion de inventario equipados
                view["centrado"]["equipados"]["objetos"].update(Panel(Text.from_markup(text_equipados), title="Equipados", style="dark_orange3"))
                
                #actualizamos estadistica del personaje
                view["centrado"]["equipados"]["estadistica"].update(self.estadisticas())
                
                #actualizar diagrama
                view["centrado"]["equipados"]["diagrama"].update(Panel(self.diseño["normal"] if self.vida > (self.vida*0.8) else self.diseño["herido"], title="Estado",style=f"{"green4" if self.vida > (self.vida*0.8) else "red"}"))
                
                #imprimimos GUI con centra
                centra = Layout(Panel(view, style="bright_black"))
                consola.print(centra)
            else:
                return Panel("⌬ No tienes nada en tu inventario", style="info")
            
            comando = str(input("➥ ")).lower().split()
            
            #reiniciamos la vista de la seccion de response
            view["response"].visible = False
            
            #validamos que no este vacio
            if not comando:
                view["response"].update(Panel("Selecciona una opcion Valida", style="alert"))
                view["response"].visible = True
                continue
            
            match comando[0]:
                case "equipar":
                    consola.clear()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                if isinstance(item, vestimenta):
                                    #actualisamos seccion de respuesta para que si o si mustre un mensaje
                                    view["response"].update(item.vestir(self))
                                    view["response"].visible = True
                                    break
                        else:
                            view["response"].update(Panel(f"⌬ No tienes {objeto} en tu inventario",style="info"))
                            view["response"].visible = True  
                    else:
                        view["response"].update(Panel("⌬ No has especificado el objeto a equipar",style="info"))
                        view["response"].visible = True 
                
                case "desequipar":
                    consola.clear()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        for item in self.vestimentas:
                            if item.nombre.lower() == objeto:
                                item.desequipar(self)
                                break
                        else:
                            print(f"⌬ No tienes {objeto} en tu inventario")
                            print(" ")  
                    else:
                        print("⌬ No has especificado el objeto a equipar")
                        print(" ")
                
                case "usar":
                    consola.clear()
                    if len(comando) > 1:
                        objeto = comando[1].lower().strip()
                        #print (objeto)
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                if isinstance(item, consumible):
                                    respuesta = item.usar(self)
                                    if isinstance(respuesta, Panel):
                                        view["response"].update(respuesta)
                                        view["response"].visible = True
                                    break
                                else:
                                    view["response"].update(Panel(f"⌬ No puedes usar {objeto}, no es un consumible", style="info"))
                                    view["response"].visible = True
                                    break       
                        else:
                            view["response"].update(Panel(f"⌬ No tienes {objeto} en tu inventario", style="info"))
                            view["response"].visible = True
                    else:
                        view["response"].update(Panel(f"⌬ No has especificado el objeto a usar", style="info"))
                        view["response"].visible = True
                case "informacion":
                    consola.clear()
                    if len(comando) > 1:
                        if self.inventario or self.vestimentas:
                            all_vestiman= self.inventario + self.vestimentas
                            for item in all_vestiman:
                                #print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    item.describir()
                                    break
                            else:
                                view["response"].update(Panel(f"⌬ No tienes {comando[1]} en tu inventario", style="info"))
                                view["response"].visible = True
                        else:
                            view["response"].update(Panel("⌬ No tienes nada en tu inventario",style="info" ))
                            view["response"].visible = True
                    else:
                        consola.clear()
                        view["response"].update(Panel("⌬ Debes especificar el objeto del que quieres informacion", style="info"))  
                        view["response"].visible = True
                case "tirar":
                    consola.clear()
                    if len(comando) > 1:
                        objeto = comando[1].lower()
                        for item in self.inventario:
                            if item.nombre.lower() == objeto:
                                self.extraer_inventario(item)
                                self.lugar_actual.agregar_objeto(item)
                                view["response"].update(Panel(f"⌬ Has tirado {objeto}", style="info"))
                                view["response"].visible = True
                                break
                        else:
                            view["response"].update(Panel(f"⌬ No tienes {objeto} en tu inventario", style="info"))
                            view["response"].visible = True
                    else:
                        view["response"].update(Panel("⌬ No has especificado el objeto a tirar", style="info"))
                        view["response"].visible = True
                case "salir":
                    consola.clear()
                    break
                case _:
                    consola.clear()
                    view["response"].update(Panel("⌬ Comando no valido", style="info"))
                    view["response"].visible = True

    def agregar_vestimenta(self, objeto):
        """esta funcion agrega un objeto al inventario del jugador sin aplicar sus efectos"""
        consola.clear()
        for item in self.vestimentas:
            if item.tipo == objeto.tipo:
                return Panel("⌬ No puedes llevar dos veces la misma vestimenta", style="alert") 
        else:
            #aqui funciona todo correctamente y se agrega el objeto al inventario
            self.vestimentas.append(objeto)
            self.peso_inventario += objeto.peso * objeto.cantidad
            return True
            #no se actualiza el peso porque ya esta actualizado en la funcion de agregar_inventario pero cmomo se estrae del inventario se resta el peso 

    def extraer_vestimenta(self, objeto):
        """esta funcion elimina un objeto del inventario del jugador"""
        consola.clear()
        for item in self.vestimentas:
            if item.nombre == objeto.nombre:
                self.vestimentas.remove(objeto)
                self.peso_inventario -= objeto.peso * objeto.cantidad
                return True
        else:
            #aqui funciona todo correctamente y se agrega el objeto al inventario
            print("⌬ No tienes esa vestimenta equipada")
            print(" ")
            return False  
        
    def tomar_objeto(self, objeto):
        consola.clear()
        for item in self.lugar_actual.objetos:
            if objeto == "cofre":
                return Panel("⌬ No puedes tomar un cofre", style="info")
            elif item.nombre.lower() == objeto:
                    respuesta= self.agregar_inventario(item)
                    if respuesta == True:
                        self.lugar_actual.quitar_objeto(item)
                        return Panel(f"⌬ has tomado {item.nombre} (Cantidad: {item.cantidad})", style="info")
                    else:
                        return respuesta
        else:
            return Panel(f"⌬ No hay {objeto} aqui.", style="info")
        
    def calcular_ventaja(self, contrincante):
        """esta funcion devuelve si hay ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y iguales si son iguales"""
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if self.nivel_combate > contrincante.nivel_combate:
            print(f"⌬ ¡Tienes ventaja sobre {contrincante.nombre}!")
            print(" ")
            return True
        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif self.nivel_combate < contrincante.nivel_combate:
            print(f"⌬ ¡{contrincante.nombre} tiene ventaja sobre ti!")
            print(" ")
            return False
        #cuando los niveles son iguales
        elif self.nivel_combate == contrincante.nivel_combate:
            print("⌬ Niveles iguales - combate justo")
            print(" ")
            return "iguales"

    def atacar(self, contrincante):
        """Ataca a un contrincante basado en el nivel de combate"""
        #validamos si el contrincante ya está muerto si ya lo esta que retorne
        if contrincante.vida <= 0:
            return Panel(f"{contrincante.nombre} ya está muerto")
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
                return f"⌬ [white]{self.nombre} ha fallado el ataque[/]\n"
                

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌬ Has causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

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
                return f"⌬ [white]{self.nombre} ha fallado el ataque [/]\n"

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌬ Has causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

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
                return f"⌬ [white]{self.nombre} ha fallado el ataque[/]\n"

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌬ Has causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

    @classmethod
    def ataque_probabilidad(self, probabilidad:float):
        """esta funcion calcula la probabilidad de ataque y devuelve True o False"""
        return random.random() < probabilidad

    def defender(self):
        """esta funcion hace que el jugador se defienda cambie el booleano de defensa_activa a True pero al final de su turno se debe desactivar desde afuera"""
        self.defensa_activa = True
        return f"⌘ [green]{self.nombre} se defiende[/]\n"
    
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
        print("⌬ Game Over")
        input("_")
        self.control_juego.game_over()


#clases imagenes asciii

diagramas = {
    "normal":Text(f"""                    
       :#@@#:       
       @@@@@@       
       =@@@@=       
       .-++-.       
    .+@@@@@@@@+.    
    :@%@@@@@@%@-    
    :@=@@@@@@=@-    
    :@=@@@@@@=@-    
    .#=@@@@@@=#:    
      :@@++@@:      
      :@@++@@:      
      :@@++@@:      
      :@@++@@:      
      .@@-:@@.      
                    """, style="white"),
    "herido":Text(f"""                                
        ::               
        **               
        =-               
        -=               
    .-.#@@#.-.           
       .##.              
        %%               
        @@               
        @@               
        @%               
        %#               
        #*               
        ++               
        .:               
                                """),
    "muerto":Text(f"""                                  
    :@@@@@@@@:            
  .@@@@@@@@@@@@.          
  @@@@@@@@@@@@@@          
  @@@+*@@@@*=%@@          
  %@   :@@-   @@          
   @@%@@##@@%@@           
    .@@@@@@@@.            
      %*%%*@              
      % %% #                      """)
} 









