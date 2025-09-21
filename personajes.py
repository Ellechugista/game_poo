import random
from utils import *
from objects import *
# entidad otros seres personajes y demás 
class entidad:
    def __init__(self, nombre: str, dialogos, vida:float,descripcion:str=None, rutinas=None, nivel_combate=4, habilidades:dict = {"atacar": 5, "defender": 5}, animo=50, diagrama:Text=Text("aqui imagen en ASCII")):
        self.nombre = nombre
        # los dialogos deben ser un diccionario como clave el tipo de diálogo y como valor un diccionario con las opciones de respuesta
        self.dialogos = dialogos
        self.vida = vida
        self.descripcion = descripcion
        self.animo = animo
        self.rutinas = rutinas
        self.habilidades = habilidades
        self.nivel_combate = nivel_combate
        self.defensa_activa = False
        self.diagrama = diagrama #diagrama de imagen en ASCII
        
        #estado para verificar si esta vivo o muerto (relacion con misiones)
        self.estado = "vivo"
        
        #seccion de misiones 
        self.misiones_objetivo = []
        self.misiones_a_dar = []
        
        #estos dialogos otra mision son dialogos dento de la miscion que dan info pero desde otros personaje sno solo el personaje que las da
        self.dialogos_otra_mision = []
        
        #inventario del personaje sin limites de peso
        self.inventario = []
        
        #registramos la entidad en el registro de entidades para acceder a ella desde el registro
        RegistroEntidades.registrar(self)
        
    def estadisticas(self, GUI:bool=None):
        if GUI == False:
            return Panel(Text.from_markup(f"[yellow]☺ Nombre:[/] [white]{self.nombre}[/]\n[red]🎔 Vida:[/] [white]{self.vida}[/]\n[orange3]✧ Animo:[/] [white]{self.calcular_animo()}[/]\n[blue]⍚ Nivel de combate:[/] [white]{self.nivel_combate}[/]\n[green]❖ Habilidades:[/] [white]Ataque:{self.habilidades['atacar']} Defensa:{self.habilidades['defender']}[/]\n"), title = "Estadisticcas contrincante", style="white")
        
        #GUI
        view= Layout()
        
        #seccion de informacion
        view.split_column(
            Layout(Panel(Text("INFORMACION DE ENTIDAD", justify="center"), style="info"), size=3),
            Layout(name="centra", size=28)
        )
        
        #secciones y layouts
        view["centra"].split_row(
            Layout(name="diagrama", size=45),
            Layout(name="info", ratio=2)
        )
        
        texto = Text.from_markup(f"[yellow]☺ Nombre:[/] [white]{self.nombre}[/]\n[red]🎔 Vida:[/] [white]{self.vida}[/]\n[orange3]✧ Animo:[/] [white]{self.calcular_animo()}[/]\n[blue]⍚ Nivel de combate:[/] [white]{self.nivel_combate}[/]\n[green]❖ Habilidades:[/] [white]Ataque:{self.habilidades['atacar']} Defensa:{self.habilidades['defender']}[/]\n\n")
        
        #añadimos texto de presentacion
        texto.append(self.presentacion())
        
        #actualizamos los paneles
        view["centra"]["info"].update(Panel(texto, style="white", title="Estadisticas"))
        
        view["centra"]["diagrama"].update(Panel(self.diagrama, title="Diagrama",style="orange3"))
        
        #baner centrador
        centra = Layout(Panel(view, style="bright_black"))
        
        #imprimimos el view
        consola.print(centra)
        consola.input("⌬ Presiona cualquier cosita para continuar")
        return

    def calcular_animo(self):
        """aqui calculamos el animo de la entidad, y lo devolvemos como un string para que el jugador sepa como se siente
        si el animo es mayor a 50 la entidad se siente normal, si es mayor a 70 feliz, si es menor a 50 triste, si es menor a 30 enojado y si es menor o igual a 0 el animo se pone en 0
        """
        
      #aqui tenemos que calcular el animo de la entidad
        clave = ""
        if self.animo >= 50:
            clave = "normal"
        elif self.animo >= 70:
            clave = "feliz"
        elif self.animo < 50:
            clave = "triste"
        elif self.animo < 30:
            clave = "enojado"
        elif self.animo <= 0:
            self.animo = 0
        return clave
    
    def hablar(self, jugador):
        """aqui el sujeto tendrá una lista de diccionarios qué tendrán textos que mostrará según el carácter de la entidad, y otro diccionario que tendrá las respuestas que el usuario puede darle"""
        #GUI
        view = Layout()
        
        view.split_column(
            Layout(name="response", size=3, visible=False),
            Layout(name="conten", size=28)
        )
        
        #dividimos el contenido
        view["conten"].split_row(
            Layout(name="dialogos", ratio=3),
            Layout(name="diagrama", size=45)
        )
        
        #dividimos segmento dialogos
        view["conten"]["dialogos"].split_column(
            Layout(name="dialogo", ratio=3),
            Layout(name="respuestas", ratio=1, minimum_size=8)
        )
        
        #si o si actializamos el diagrama
        view["conten"]["diagrama"].update(Panel(self.diagrama,style="dark_orange3", title="Diagrama"))
        
        #centrador
        centra = Layout(Panel(view, style="bright_black"))
        
        if self.misiones_a_dar:
            for m in self.misiones_a_dar:
                if m.estado == "inactivo":
                    m.dialogos_iniciar(jugador, view)
                    break
                elif m.estado == "activo":
                    resultado = m.validar_objeto_inventario(jugador)
                    #print(resultado)
                    #print(all(resultado))
                    #input("pausa")
                    if resultado == None or not all(resultado):
                        m.dialogos_proceso(view)
                        limpiar_consola()
                        break
                    elif resultado and all(resultado):
                        m.completar_mision(jugador, view,tipo="exito")
                        break
                elif m.estado == "completado" or m.estado == "fallido":
                    self.misiones_a_dar.remove(m)
            return        
                    
        #esto da los dialogos opcionales si la mision esta activa
        if self.dialogos_otra_mision:
            for m in self.dialogos_otra_mision:
                if m.estado == "activo":
                    dialogos_otros = m.dialogos["info"]
                    for d in dialogos_otros:
                        #print(d)
                        if self in d:
                            #print(d[self])
                            #inicia proceso de dialogo
                            for anunciado in d[self]:
                                for info, respuestas in anunciado.items():
                                    while True:
                                        view["conten"]["dialogos"]["dialogo"].update(Panel(f"[dark_orange3]{self.nombre}[/][bright_black]: {info}[/]", style="dodger_blue1", title="Dialogo de Entidad"))
                                        
                                        #respuestassssss
                                        text_respuestas=""
                                        text_respuestas += "Respuestas:\n"
                                        #añadimos las respuestas
                                        for i, r in enumerate(respuestas):
                                            text_respuestas += f"[green]{i+1}.[/][white] {r}[/]\n"
                                            
                                        #añadimos la info como panel al layout
                                        view["conten"]["dialogos"]["respuestas"].update(Panel(Text.from_markup(text_respuestas), style="dodger_blue2"))
                                        #actualizamos vista
                                        view["conten"]["dialogos"]["respuestas"].visible = True
                                        
                                        #centrador
                                        centra = Layout(Panel(view, style="bright_black"))
                                        
                                        #imprimimos layout 
                                        consola.print(centra)
                                        try:
                                            #esperar seleccion del jugador y reiniciamos response
                                            view["response"].visible = False
                                            seleccion = int(input("➥ ")) - 1
                                            if seleccion < 0 or seleccion >= len(respuestas):
                                                view["response"].update(Panel("⌘ Selección inválida. Intenta de nuevo.", style="alert"))
                                                #actualizamos response
                                                view["response"].visible = True
                                                continue
                                            elif seleccion == 0:
                                                return
                                            
                                            #añadimos lo que dijo el sujeto a los registros de la mision
                                            m.añadir_registro(f"{self.nombre}: {info}")
                                        except ValueError:
                                            view["response"].update(Panel("⌘ Entrada inválida. Por favor, ingresa un número.", style="alert"))
                                            #actualizamos response
                                            view["response"].visible = True
                                            continue
                                        break
                        #esto rompe el for del que itera por cada dialogo en los dialogos otros
                        #break

                elif m.estado == "completado" or m.estado == "fallido":
                    self.eliminar_dialogos_otra_mision(m)
            limpiar_consola()
        
        else:
            clave = self.calcular_animo()
            #aqui se elige la respuesta dependiendo del animo de la entidad
                
            match clave:
                case "normal":
                    respuesta = random.choice(self.dialogos["normal"])
                case "feliz":
                    respuesta = random.choice(self.dialogos["content"])
                case "triste":
                    respuesta = random.choice(self.dialogos["triste"])
                case "enojado":
                    respuesta = random.choice(self.dialogos["enojado"])
                case "repetido":
                    respuesta = random.choice(self.dialogos["repetido"])
            #actualizamos el contenido
            view["conten"]["dialogos"]["dialogo"].update(Panel(f"[dark_orange3]{self.nombre}[/][bright_black]: {respuesta}[/]", style="dodger_blue1", title="Dialogo de Entidad"))
            
            #debemos ocultar las respuestas ya no las usaremos aqui
            view["conten"]["dialogos"]["respuestas"].visible = False
            
            #imprimimos la info actualizada
            consola.print(centra)
            input("⌬ Oprime cualquier opcion para salir")
            return            
                    
    def agregar_dialogos_otra_mision(self, mision):
        self.dialogos_otra_mision.append(mision)
    
    def eliminar_dialogos_otra_mision(self, mision):
        self.dialogos_otra_mision.remove(mision)      
                    
    def luteador(self, jugador):
        """esta funcion genera un loop donde el jugador decide que tomar de los objetos que tenia el personaje en su inventarios"""
        
        #gui
        view=Layout()
        
        #seccionamos 
        view.split_column(
            Layout(name="response", size=3, visible=False),
            Layout(name="conten", size=28)
        )
        
        view["conten"].split_row(
            Layout(name="e-inven"),
            Layout(name="p-inven")
        )
            
        centra = Layout(Panel(view, style="bright_black"))
        
        while True:
            #informacion de la entidad
            text_entidad = f"☠ Contenido de {self.nombre} (jubilado):\n"
            if self.inventario:
                for item in self.inventario:
                    if item.cantidad == 1:
                        text_entidad += f"[green4]ⵚ[/] [white]{item.nombre}[/]\n"
                    else:
                        text_entidad += f"[green4]ⵚ[/] [white]{item.nombre} x({item.cantidad})[/]\n"
            else:
                #tenemos que salir de inmediato de ente bucle ya que no hay mas que hacer
                break
            
            #informacion del inventario del jugador
            text_player= f"[b]Tienes:[/]\n"
            if jugador.inventario:
                for item in jugador.inventario:
                    if item.cantidad == 1:
                        text_player += f"[green4]ⵚ[/] [white]{item.nombre}[/]\n"
                    else:
                        text_player += f"[green4]ⵚ[/] [white]{item.nombre} x({item.cantidad})[/]\n"
            else:
                text_player = "[bright_black]⌬ No tienes nada en tu inventario[/]"
                
            #actualizamos el GUI
            #inventario de entidad
            view["conten"]["e-inven"].update(Panel(Text.from_markup(text_entidad), style="dodger_blue2", title="Inventario Del Difunto"))
            
            #inventario del jugador
            view["conten"]["p-inven"].update(Panel(Text.from_markup(text_player), style="orange3",title="Tu inventario"))
            
            #imprimimos el layout 
            consola.print(centra)
            
            #aqui debera escribir que desea hacer con el contenido
            comando = str(input("> ")).lower().split()
            view["response"].visible = False
            
            if not comando:
                view["response"].update(Panel(f"⌬ Debes especificar que quieres tomar", style="info"))
                view["response"].visible = True
                continue
            
            match comando[0]:
                case "tomar":
                    if len(comando) > 1:
                        #toma todo el contenido del cofre
                        if comando[1] == "*":
                            items = self.inventario[:]  # copia
                            for item in items:
                                if jugador.agregar_inventario(item):
                                    self.extraer_inventario(item)
                                else:
                                    view["response"].update(Panel("algo salo mal", style="alert"))
                                    view["response"].visible=True
                                    break
                            else:
                                #actualizamos info del baner
                                view["response"].update(Panel("has tomado todo.", style="exito"))
                                view["response"].visible = True
                                
                                #actualizamos inventariado del difunto
                                view["conten"]["e-inven"].update(Panel("⌬ Aqui no hay nada", style="bright_black"))
                                
                                #imprimimos la actualizacion
                                consola.print(centra)
                                consola.input("⌬ Presiona cualquier cosita para continuar")
                            continue
                        
                        for item in self.inventario:
                            if comando[1] == "cofre":
                                limpiar_consola()
                                print("⌘No puedes tomar un cofre")
                                print(" ")
                                continue
                            elif item.nombre.lower() == comando[1]:
                                resultado = jugador.agregar_inventario(item) 
                                if isinstance(resultado, Panel):
                                    #actualizamos layout
                                    view["response"].update(resultado)
                                    view["response"].visible = True
                                    break
                                elif resultado == True:
                                    self.extraer_inventario(item)
                                    view["response"].update(Panel(f"⌬ Has tomado {item.nombre}", style="exito"))
                                    view["response"].visible = True
                                    break
                                else:
                                    break
                        else:
                            limpiar_consola()
                            view["response"].update(Panel(f"⌬ No hay {comando[1]} aqui", style="info"))
                            view["response"].visible = True
                            continue
                    else:
                        view["response"].update(Panel(f"⌬ Debes especificar que quieres tomar", style="info"))
                        view["response"].visible = True
                        continue
                case "dejar":
                    if len(comando) > 1:
                        for item in jugador.inventario:
                            if item.nombre.lower() == comando[1]:
                                self.agregar_inventario(item)
                                jugador.extraer_inventario(item)
                                view["response"].update(Panel(f"⌬ Has dejado {item.nombre}", style="exito"))
                                view["response"].visible = True
                                break
                        else:
                            view["response"].update(Panel(f"⌬ No tienes {comando[1]} en tu inventario", style="info"))
                            view["response"].visible = True
                            continue
                    else:
                        view["response"].update(Panel(f"⌬ Debes especificar que quieres dejar", style="info"))
                        view["response"].visible = True
                        continue
                case "inventario":
                    limpiar_consola()
                    jugador.mostrar_inventario()
                    continue
                case "salir":
                    limpiar_consola()
                    break
                case _:
                    limpiar_consola()
                    view["response"].update(Panel(f"⌬ Comando invalido", style="info"))
                    view["response"].visible = True
                    continue

    def soltar_azar(self):
        probabilidad =0.4
        if not self.inventario:
            return
        
        seleccionados = [item for item in self.inventario if random.random() < probabilidad]
        return seleccionados

    # aqui van las rutinas de la entidad lo que hace, aun no se como hacerlo
    def rutina_activada(self, rutina):
        pass

    def presentacion(self):
        """esta funcion presenta la entidad, lo ideal es que se extienda esta clase deacuerdo a la raza o tipo de entidad"""
        print(f"✧{self.nombre} es una entidad sin clase")
        print(f"✧{self.descripcion}")
    
    def calcular_ventaja(self, contrincante):
        """esta funcion devuelve si hay ventaja en el combate y devuelve true si hay ventaja y false si no hay ventaja y iguales si son iguales"""
        #cuando el nivel de combate del jugador es mayor al del contrincante
        if self.nivel_combate > contrincante.nivel_combate:
            print(f"⌘¡{self.nombre} tiene ventaja sobre {contrincante.nombre}!")
            print(" ")
            return True
        #cuando el nivel de combate del contrincante es mayor al del jugador
        elif self.nivel_combate < contrincante.nivel_combate:
            print(f"⌘¡{contrincante.nombre} tiene ventaja sobre {self.nombre}!")
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
                return f"⌘ [white]{self.nombre} ha fallado el ataque[/]\n"

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌘ Has causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

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
                return f"⌘ [white]{self.nombre} ha fallado el ataque[/]\n"

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌘Has causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

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
                return f"⌘ [white]{self.nombre} ha fallado el ataque[/]\n"

            #calculo de daño
            daño_base = self.habilidades["atacar"]
            daño_minimo = daño_base // 2
            daño_final = random.randint(int(daño_minimo), int(daño_base))
            #aqui comprobamos que el daño no sea negativo
            if daño_final < 0:
                daño_final = 0
            #hacemos daño al contrincante
            contrincante.vida = max(0, contrincante.vida - daño_final)
            return f"⌘ Ha causado [white]{daño_final}[/] de daño a {contrincante.nombre}\n"

    def ataque_probabilidad(self, probabilidad:float):
        """esta funcion calcula la probabilidad de ataque y devuelve True o False"""
        return random.random() < probabilidad
    
    def defender(self):
        """esta funcion hace que el jugador se defienda cambie el booleano de defensa_activa a True pero al final de su turno se debe desactivar desde afuera"""
        self.defensa_activa = True
        return f"⌘ [green]{self.nombre} se defiende[/]\n"
    
    def agregar_inventario(self, objeto):
        if isinstance(objeto, list):
            for nuevo_item in objeto:
                for item in self.inventario:
                    if item.nombre == nuevo_item.nombre:
                        item.cantidad += nuevo_item.cantidad
                        break
                else:
                    self.inventario.append(nuevo_item)
        else:
            for item in self.inventario:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.inventario.append(objeto)
       
    def extraer_inventario(self, objeto):
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
            
    
# -----------ENTIDADESSSSSSS----------------------------------------------
#estendemos la clase entidad para crear razas o tipos de entidades
#humanos
class humano(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=5, habilidades = { "atacar": 5,"defender": 5 }, animo=50, diagrama:Text=Text("aqui imagen en ASCII")):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades, animo, diagrama)
    def presentacion(self):
        return Text.from_markup(f"✧{self.nombre} es un humano\n [bright_black]{self.descripcion}[/]")
#ELFOS  
class elfo(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=8, habilidades = { "atacar": 8,"defender": 15 }, animo=50, diagrama:Text=Text("aqui imagen en ASCII")):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades, animo, diagrama)
    def presentacion(self):
        return Text.from_markup(f"✧{self.nombre} es un elfo\n [bright_black]{self.descripcion}[/]")
#ORCOS
class orco(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=3, habilidades = { "atacar": 15,"defender": 12 }, animo=50, diagrama:Text=Text("aqui imagen en ASCII")):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades, animo, diagrama)
    def presentacion(self):
        return Text.from_markup(f"✧{self.nombre} es un orco\n [bright_black]{self.descripcion}[/]")
        
#DUENDES
class duende(entidad):
    def __init__(self, nombre, dialogos, vida, descripcion = None, rutinas=None, nivel_combate=2, habilidades = { "atacar": 2,"defender": 2 }, animo=50, diagrama:Text=Text("aqui imagen en ASCII")):
        super().__init__(nombre, dialogos, vida, descripcion, rutinas, nivel_combate, habilidades, animo, diagrama)
    def presentacion(self):
        return Text.from_markup(f"✧{self.nombre} es un duende\n [bright_black]{self.descripcion}[/]")


   
# aqui creamos los dialogos de la entidad para que pueda hablar cuando llamemos a la función de la clase estos son una base y deberían modificarse o añadir un diccionario de listas más especializado para cada entidad

feliz = [
    "¡Hoy es un gran día!",
    "Me siento increíblemente bien.",
    "No puedo dejar de sonreír.",
    "Todo parece ir perfectamente.",
    "La vida es maravillosa.",
    "Estoy lleno de energía y alegría.",
    "Hoy todo me sale bien.",
    "Me siento agradecido por todo lo que tengo.",
    "¡Qué felicidad me da este momento!"
]

# Lista de frases neutras
neutro = [
    "Hoy es un día como cualquier otro.",
    "No tengo nada especial que comentar.",
    "Todo parece normal.",
    "Ni bien ni mal, simplemente neutral.",
    "No siento nada en particular.",
    "Hoy no tengo emociones fuertes.",
    "Todo está tranquilo y sin cambios.",
    "No hay nada nuevo bajo el sol.",
    "Sigo mi rutina como siempre."
]

# Lista de frases enojadas
enojado = [
    "¡Estoy furioso!",
    "No puedo creer que esto esté pasando.",
    "Todo me está saliendo mal.",
    "¡Estoy harto de esta situación!",
    "No quiero hablar con nadie.",
    "La gente me está sacando de quicio.",
    "No soporto más esta injusticia.",
    "Estoy a punto de explotar de rabia.",
    "¡Basta ya, no aguanto más!"
]

# Lista de frases repetitivas
repetitivo = [
    "Lo mismo de siempre.",
    "Otra vez lo mismo.",
    "No hay nada nuevo que decir.",
    "Siempre es igual.",
    "Repitiendo lo mismo una y otra vez.",
    "Cada día es una repetición del anterior.",
    "No hay cambios, todo sigue igual.",
    "Me aburro de tanta monotonía.",
    "Otra vez la misma historia."
]

# Lista de frases tristes
triste = [
    "Hoy me siento muy mal.",
    "No tengo ganas de hacer nada.",
    "Todo parece gris y sin sentido.",
    "No puedo dejar de llorar.",
    "Me siento solo y abandonado.",
    "La tristeza me invade por completo.",
    "No encuentro consuelo en nada.",
    "Siento que el mundo está en mi contra.",
    "No sé cómo salir de este pozo."
]

dialogos_ejemplos = {
    "normal": neutro,
    "content": feliz,
    "triste": triste,
    "enojado": enojado,
    "repetido": repetitivo
}

#aqui creamos a los personajes


#humanos de valle lidien
petriscax = humano("Petriscax", dialogos_ejemplos, 100, "Un anciano de vastante edad, cabello y barba larga y blanca su cara refleja una vida llena de vivencias y penurias que quedan marcadas en el tiempo.", nivel_combate=29, habilidades={"atacar":20,"defender":25}, animo=50, diagrama=imagen_assci(os.path.join(humanos_ruta, "humano_anciano.png")))

marcelito = humano("Marcelito", dialogos_ejemplos, 100, "Un chico joven. muy reservado, cabello corto y lentes arcaicos, con fuerte sentido de moral y justicia.", nivel_combate=11, habilidades={"atacar":18,"defender":15}, animo=50, diagrama=imagen_assci(os.path.join(humanos_ruta, "humano_2.png")))

laura = humano("Laura", dialogos_ejemplos, 100, "Una chica joven y alegre, optimista y energica, morena cabello largo negro, y una sonrisa sin igual, en las tardes trabaja en la herreria de su tio.",nivel_combate=9,habilidades={"atacar":14,"defender":10}, animo=50, diagrama=imagen_assci(os.path.join(humanos_ruta,"laura.jpg")))

laura.agregar_inventario([monedax10, monedax10, monedax10, escudo])

madre = humano("Madre", dialogos_ejemplos, 100, "Esta mujer es tu madre, una persona gastada pero con porte inquebrantable que ha llevado una vida dificil pero con mucho amor, pues tu su hijo es su mas grande logro, lee algunas veces y se impresiona con la simplesa de la vida.", diagrama=imagen_assci(os.path.join(humanos_ruta,"humano_feme1.png")))

matrifutchka = duende("Mtrifutchka", dialogos_ejemplos, 80, "Este sujeto, es curioso y misterioso, se arrincona a una esquina del lugar donde menos pega a luz, parece herido, pero no permite hablar, una vibra oscura irradia de el", nivel_combate=35, habilidades={"atacar": 34, "defender": 22}, animo=25, diagrama=imagen_assci(os.path.join(duendes_ruta,"duende_sangano.png")))

rufian = orco("melchorro", dialogos_ejemplos, 130, "A prendas rasgadas y maltratades este sujeto irradia un mal augurio, pues la vida no fue sutil con el, su cuerpo lleno de sicatrices y heridas lo demuestran, a de ser un gerrero fijo", nivel_combate=20, habilidades={"atacar": 20, "defender": 23}, animo=10, diagrama=imagen_assci(os.path.join(orco_ruta,"orco_regular.png")))



if __name__ == "__main__":
    # aqui creamos la entidad
    """marcelito = humano("marcelito", dialogos_ejemplos, 100)
    marcelito.presentacion()
    marcelito.hablar("repetido")"""


