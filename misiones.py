from player import *
from lugares import *
#from object import *
from personajes import *

class Mision:
    def __init__(self, id:int ,nombre:str, descripcion:str, personaje_asigna:entidad, objetivos:str, dialogos:dict, experiencia:int, recompensas:list, objetos_requeridos:dict):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        #aqui se asigna el personaje que le da la mision al jugador
        self.personaje_asigna = personaje_asigna
        #aqui añadimos a la lista del personaje la mision para que la tenga en su lista
        self.personaje_asigna.misiones_a_dar.append(self)
        
        self.objetivos = objetivos
        #esta lista son los objetos que hay que llevar al lugar o al personaje en cuestion 
        self.objetos_requeridos = objetos_requeridos
        
        self.estado = "inactivo"
        
        #recompenzas
        self.experiencia = experiencia
        self.recompensas = recompensas
        
        #dialoogos de la mision para obtener la mision
        # este dict tendra esta estructura
        # dialogos = {
        #     "iniciar": [
        #    {dialogo1:respuestas[1,2,3]},
        #    {dialogo2:respuestas[1,2,3]},
        #    {dialogo3:respuestas[1,2,3]}
        #     ],
        #     "proceso": [
        #    {dialogo1:respuestas[1,2,3]},
        #    ],
        #     "exito": [
        #    {dialogo1:respuestas[1,2,3]},
        #    {dialogo2:respuestas[1,2,3]},
        #    {dialogo3:respuestas[1,2,3]}
        #     ],
        #     "fracaso": [
        #    {dialogo1:respuestas[1,2,3]},
        #    {dialogo2:respuestas[1,2,3]},
        #    {dialogo3:respuestas[1,2,3]}
        #     ]
        #     }
        self.dialogos = dialogos
        
        #actualizacion y registros de avanze de la mision almacenaran los ultimos textos de los dialogos importantes
        self.registros = []
        
    def iniciar_mision(self, player:player):
        limpiar_consola()
        self.estado = "activo"
        player.agregar_mision(self)
        print(f"[Misión '{self.nombre}' iniciada.]")
        print("")
        
    def dialogos_iniciar(self, jugador:player, view:Layout):
        """esta funcion inicia la secuencia de dialogos y respuestas para iniciar o aceptar una mision"""
        limpiar_consola()
        dialogos_iniciar = self.dialogos["iniciar"]
        for d in dialogos_iniciar:
            #imprime el dialogo y las respuestas
            for key, value in d.items():
                limpiar_consola()
                while True:
                    view["conten"]["dialogos"]["dialogo"].update(Panel(f"[dark_orange3]{self.personaje_asigna.nombre}[/][bright_black]: {key}[/]", style="dodger_blue1", title="Dialogo de Entidad"))
                    
                    #respuestassssss
                    text_respuestas=""
                    text_respuestas += "Respuestas:\n"
                    #añadimos las respuestas
                    for i, respuesta in enumerate(value):
                        text_respuestas += f"[green]{i+1}.[/][white] {respuesta}[/]\n"
                    
                    #añadimos la info como panel al layout
                    view["conten"]["dialogos"]["respuestas"].update(Panel(Text.from_markup(text_respuestas), style="dodger_blue2"))
                    #actualizamos vista
                    view["conten"]["dialogos"]["respuestas"].visible = True
                    
                    #centrador
                    centra = Layout(Panel(view, style="bright_black"))
                    
                    #imprimimos layout 
                    consola.print(centra)
                    try:
                        #añadimos lo que dijo el sujeto a los registros de la mision
                        self.añadir_registro(f"{self.personaje_asigna.nombre}: {key}")
                        #esperar seleccion del jugador y reiniciamos response
                        view["response"].visible = False
                        seleccion = int(input("➥ ")) - 1
                        if seleccion < 0 or seleccion >= len(value):
                            view["response"].update(Panel("⌘ Selección inválida. Intenta de nuevo.", style="alert"))
                            #actualizamos response
                            view["response"].visible = True
                            continue
                        elif seleccion == 0:
                            return
                        
                    except ValueError:
                        view["response"].update(Panel("⌘ Entrada inválida. Por favor, ingresa un número.", style="alert"))
                        #actualizamos response
                        view["response"].visible = True
                        continue
                    break

        #aqui es donde se inicia la mision, se le asigna al jugador y se cambia el estado de la mision a activo
        self.iniciar_mision(jugador)
        self.añadir_registro(f"se ha asignado la mision a {jugador.nombre}")
        #self.añadir_registro(self.dialogos["info"][0])
         
    def dialogos_proceso(self, view:Layout):
        limpiar_consola()
        dialogos_proceso = self.dialogos["proceso"]
        
        for d in dialogos_proceso:
            #imprime el dialogo y las respuestas la llave dialogo del personaje y value lista de respuestas para player
            for key, value in d.items():
                while True:
                    view["conten"]["dialogos"]["dialogo"].update(Panel(f"[dark_orange3]{self.personaje_asigna.nombre}[/][bright_black]: {key}[/]", style="dodger_blue1", title="Dialogo de Entidad"))
                    
                    #respuestassssss
                    text_respuestas=""
                    text_respuestas += "Respuestas:\n"
                    
                    #imprimir las respuestas
                    for i, respuesta in enumerate(value):
                        text_respuestas += f"[green]{i+1}.[/][white] {respuesta}[/]\n"
                    
                    #añadimos la info como panel al layout
                    view["conten"]["dialogos"]["respuestas"].update(Panel(Text.from_markup(text_respuestas), style="dodger_blue2"))
                    #actualizamos vista
                    view["conten"]["dialogos"]["respuestas"].visible = True
                    
                    #centrador
                    centra = Layout(Panel(view, style="bright_black"))
                    
                    #imprimimos layout 
                    consola.print(centra)
                    try:
                        #añadimos lo que dijo el sujeto a los registros de la mision
                        self.añadir_registro(f"{self.personaje_asigna.nombre}: {key}")
                        #esperar seleccion del jugador y reiniciamos response
                        view["response"].visible = False
                        seleccion = int(input("> ")) - 1
                        if seleccion < 0 or seleccion >= len(value):
                            view["response"].update(Panel("⌘ Selección inválida. Intenta de nuevo.", style="alert"))
                            #actualizamos response
                            view["response"].visible = True
                            continue
                        elif seleccion == 0:
                            return
                        
                    except ValueError:
                        view["response"].update(Panel("⌘ Entrada inválida. Por favor, ingresa un número.", style="alert"))
                        #actualizamos response
                        view["response"].visible = True
                        continue
                    break
    
    def describir_mision(self):
        #gui
        view = Layout()
        view.split_column(
            Layout(name="info"),
            Layout(name="registros", size=10)
        )
        
        info=Text.from_markup(f"[cyan]❏ Mision[/]: [white]{self.nombre}\n[blue]⥈ ID[/]: {self.id}\n[green]⎚ objetivo[/]: {self.objetivos}\n[dark_orange3]☖ Estado:[/] {self.estado}[/white]\n[yellow]▩ Descripcion[/]: \n[bright_black]{self.descripcion}[/]\n")
    
        formato=""
        for r in self.registros[-8:]:
            formato += (f"[white][green]⊳[/] {r}[/]\n")
            
        regi = Text.from_markup(formato)
            
        #actualizamos los layouts
        view["info"].update(Panel(info, title="Descripcion de mision", style="chartreuse4"))
        
        view["registros"].update(Panel(regi, title="Registros", style="orange_red1"))
        
        #imprimimos el view
        consola.print(view)
        consola.input("⌬ Presiona cualquier cosita para continuar")
        return
     
    def añadir_registro(self, texto:str):
        texto = texto.lower()
        self.registros.append(texto)
        
    def validar_objeto_inventario(self, jugador:player):
        inventario = jugador.inventario
        if not inventario:
            return 
        resultados = []
        for obje, cantid in self.objetos_requeridos.items():
            encontrado = False
            for oinventario in inventario: 
                if obje.nombre == oinventario.nombre and oinventario.cantidad >= cantid:
                    encontrado = True
                    break
            resultados.append(encontrado)
        return resultados
    
    def completar_mision(self, jugador:player, view:Layout, tipo:str = "exito"):
        if tipo == "exito":
            #cambios de atrivutos
            self.estado = "completado"
            self.añadir_registro(f"[Msision {self.nombre} Completada.]")
            
            #alteramos el animo del personaje 
            self.personaje_asigna.animo += 20
            
            limpiar_consola()
            dialogos_proceso = self.dialogos["exito"]
            
            for d in dialogos_proceso:
                #imprime el dialogo y las respuestas la llave dialogo del personaje y value lista de respuestas para player
                for key, value in d.items():
                    while True:
                        view["conten"]["dialogos"]["dialogo"].update(Panel(f"[dark_orange3]{self.personaje_asigna.nombre}[/][bright_black]: {key}[/]", style="dodger_blue1", title="Dialogo de Entidad"))
                        
                        #respuestassssss
                        text_respuestas=""
                        text_respuestas += "Respuestas:\n"
                        
                        #imprimir las respuestas
                        for i, respuesta in enumerate(value):
                            text_respuestas += f"[green]{i+1}.[/][white] {respuesta}[/]\n"
                        #añadimos la info como panel al layout
                        view["conten"]["dialogos"]["respuestas"].update(Panel(Text.from_markup(text_respuestas), style="dodger_blue2"))
                        #actualizamos vista
                        view["conten"]["dialogos"]["respuestas"].visible = True
                        
                        #centrador
                        centra = Layout(Panel(view, style="bright_black"))
                        
                        #imprimimos layout 
                        consola.print(centra)
                        try:
                            #añadimos lo que dijo el sujeto a los registros de la mision
                            self.añadir_registro(f"{self.personaje_asigna.nombre}: {key}")
                            #esperar seleccion del jugador y reiniciamos response
                            view["response"].visible = False
                            seleccion = int(input("> ")) - 1
                            if seleccion < 0 or seleccion >= len(value):
                                view["response"].update(Panel("⌘ Selección inválida. Intenta de nuevo.", style="alert"))
                                #actualizamos response
                                view["response"].visible = True
                                continue
                            elif seleccion == 0:
                                break
                            
                        except ValueError:
                            view["response"].update(Panel("⌘ Entrada inválida. Por favor, ingresa un número.", style="alert"))
                            #actualizamos response
                            view["response"].visible = True
                            continue
                        
                        break
            
            #actualizamos el inventario
            objetos_eliminados = ""
            if self.objetos_requeridos:
                for o, c in self.objetos_requeridos.items():
                    temp = o
                    temp.cantidad = c
                    jugador.extraer_inventario(temp)
                    objetos_eliminados += f"[red][Se elimino [white]{o.nombre} x {temp.cantidad}[/] de tu inventario][/red]\n"
            
            #entregamos recompensas todas
            pagos = "\n"
            for recompensa in self.recompensas:
                chek = jugador.agregar_inventario(recompensa) 
                if not chek:
                    jugador.lugar_actual.agregar_objeto(recompensa)
                    pagos += f"[green][Se agrego [white]{recompensa.nombre}[/] al lugar][/]\n"
                else:
                    pagos += f"[green][Se agrego [white]{recompensa.nombre}[/] a tu inventario][/]\n"
            
            jugador.nivel_combate += self.experiencia
            
            #imprimimos todo lo realizado
            limpiar_consola()
            view["response"].update(Panel(f"[Msision {self.nombre} Completada.]", style="exito"))
            
            #objetos de mision y recompensas
            view["conten"]["dialogos"]["dialogo"].update(Panel((Text.from_markup(objetos_eliminados)+Text.from_markup(pagos)) if not objetos_eliminados == "" else "", title="Objetos de mision y recompensas"))
            
            #experiencias
            view["conten"]["dialogos"]["respuestas"].update(Panel(f"[Experiencia ganada [white]{self.experiencia}[/]]", title="Experiencia", style="orange3"))
            
            #centrador
            centra=Layout(Panel(view, style="bright_black"))

            consola.print(centra)
            consola.input("⌬ Presiona cualquier cosita para continuar") 
            return
              
        else:
            self.añadir_registro(f"[Mision {self.nombre} Fallida.]")
            #cambios de atrivutos
            self.estado = "fallido"
            #alteramos el animo del personaje 
            self.personaje_asigna.animo -= 10
            
            limpiar_consola()
            dialogos_proceso = self.dialogos["fracaso"]
            
            for d in dialogos_proceso:
                #imprime el dialogo y las respuestas la llave dialogo del personaje y value lista de respuestas para player
                for key, value in d.items():
                    while True:
                        limpiar_consola()
                        print(f"{self.personaje_asigna.nombre}: {key}")
                        print(" ")
                        print("Respuestas:")
                        #imprimir las respuestas
                        for i, respuesta in enumerate(value):
                            print(f"{i+1}. {respuesta}")
                        try:
                            #añadimos lo que dijo el sujeto a los registros de la mision
                            self.añadir_registro(f"{self.personaje_asigna.nombre}: {key}")
                            #esperar seleccion del jugador
                            print(" ")
                            seleccion = int(input("> ")) - 1
                            if seleccion < 0 or seleccion >= len(value):
                                limpiar_consola()
                                print("⌘Selección inválida. Intenta de nuevo.")
                                print(" ")
                                continue
                            elif seleccion == 0:
                                break
                            
                        except ValueError:
                            limpiar_consola()
                            print("⌘Entrada inválida. Por favor, ingresa un número.")
                            print(" ")
                            continue
                        break
            
            #entregamos recompensas incompetas
            pagos = []
            recompensa = self.recompensas[0] #el primer elemento de las recompensas sera solo dinero
            chek = jugador.agregar_inventario(recompensa) 
            if not chek:
                jugador.lugar_actual.agregar_objeto(recompensa)
                pagos.append(f"[Se agrego {recompensa.nombre} al lugar]")
            else:
                pagos.append(f"[Se agrego {recompensa.nombre} a tu inventario]")
            
            jugador.nivel_combate += self.experiencia / 3
            
            #imprimimos todo lo realizado
            limpiar_consola()
            print(f"[Msision {self.nombre} Fallida.]")
            print(pagos if pagos else "")
            print("")
        
        
            
        
#test de la clase mision
dialogos_m1 = {
    "iniciar": [
        {"Ey si tu ven": ["a mi nadie me chitea", "¿que sucede?", "(la mira raro*)"]},
        {"Lo que pasa aqui es que me han robado la produccion diaria y el granuja que se la llevo se fue al este y me parecio verle una espada...": ["no me interesa un carajo.", "ok, ¿y?", "deshonra de melthirt"]},
        {"parecia una espada de Ebano de las guerras de la segunda era, esas son muy dificiles de lidiar": ["no me interesa, gracias", "desgraciados", "adivinare"]},
        {"¿Quieres ayudarme con algo?": ["No tengo tiempo.", "claro, para que soy bueno", "¿Qué necesitas?"]}, 
        {"Necesito que me ayudes a recuperar la producción diaria.": ["No tengo tiempo para eso.", "ok ire a por ellos"]}
    ],
    "proceso": [
        {"¿Cómo va la misión?": ["Todo bien.", "Necesito ayuda."]},
        {"si quieres mas informacion pregunta a la gente del sur, suelen ser muy chismosos.": ["ok",]}
    ],
    "exito": [
        {"Lo lograste mi amigo": ["Gracias.", "Fue fácil."]},
        {"Hare que todos encuchen de tu hasaña aqui en este pequeño valle de lidien":["eso seria grandioso", "diles que su papichulo ya llego"]},
        {"Aqui tienes llevate esto que he estado forjando y la verdad te lo ganaste.": ["te lo agradesco.", "oohhhh una recompenza."]}
    ],
    "fracaso": [
        {"Lo siento, no pudiste completar la misión.": ["Lo intentaré de nuevo.", "No importa."]},
        {"Desafortunadamente ya no confio en ti": ["me vale.", "..."]}
    ],
    "info": [
        {laura:"El granuja se ha ido al sur, intenta preguntar por mas informacion."},
        {marcelito:[
            {"Carajo, en esta vida nadie piensa en los demas...":["...", "¿que sucede?", "disculpe, estoy buscando unos fulanos que debieron pasar corriendo por aqui, ¿lo ha visto?"]},
            {"hombre la gente loca abunda por aqui desde la procesion de Elrond al poder.":["a bueno.", "¿eso es un si?", "¿por donde se ha ido?"]},
            {"se fueron asia  la tienda mertincuntres.": ["(se va epicamente*)", "impartire justicia", "gracias."]}
        ]},
        {rufian:[
            {"Que se le perdio pequeño enqulenque?":["tranquilo hombre", "un pajarito me comento...", "supongo que eres el malnacido que busco"]},
            {"como te atreves desgraciado ya veras...":["no, no, lo siento.", "pa un mueco hay otro mueco", "en nombre de la razon y justicia impartire mi voluntad divina", "(se prepara ferozmente*)"]}
        ]}
    ]
}

DiasLaborados = Mision(1,"Dias Laborados", "Laura ha sufrido un hurto por parte de unos matones lo cual es muy injusto, ayudala a impartir justicia divina contra los infelices.", laura, "Consigue la produccion diaria de laura.", dialogos_m1, experiencia=3, recompensas=[monedax10.clonar(), lanza.clonar()], objetos_requeridos={manzana.clonar():4, espada_acero.clonar():1})
#se debe agregar enlace al personaje que participa en el info de la mision
marcelito.agregar_dialogos_otra_mision(DiasLaborados)
rufian.agregar_dialogos_otra_mision(DiasLaborados)
rufian.agregar_inventario([espada_ebano.clonar(),manzana.clonar(),manzana.clonar(),manzana.clonar(),manzana.clonar(), espada_acero.clonar() ])


#mision2