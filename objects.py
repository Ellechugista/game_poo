from utils import *
class objeto:
    def __init__(self, nombre, descripcion, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}, diagrama:Text=Text("example disegn here ASCII")):
        self.nombre = nombre
        self.descripcion = descripcion
        self.diagrama = diagrama
        self.cantidad = cantidad
        self.efectos = efectos
        self.peso = round(peso, 2)
    def clonar(self):
        # Crea una nueva instancia con los mismos atributos
        nueva_instancia = self.__class__.__new__(self.__class__)
        
        # Copia todos los atributos (incluyendo los heredados y los nuevos)
        for key, value in self.__dict__.items():
            setattr(nueva_instancia, key, value)
        
        return nueva_instancia

    def describir(self):
        #GUI
        view = Layout()
        
        #centrador
        view.split_column(
            Layout(Panel(Text("Descripcion de objeto", justify="center"), style="green"), size=3),
            Layout(name="centrador", size=28)
        )
        
        #secciones
        view["centrador"].split_row(
            Layout(name="descrip", ratio=2),
            Layout(name="diagrama",size=45)
        )
        
        #ACTUALIZAMOS
        descripcion = Text.from_markup(
            f"[red]◈[/red][b] Nombre:[/b] {self.nombre}\n[green]▣[/green][b] Estadisticas:[/b] {', '.join([f'{k} = {v}' for k, v in self.efectos.items()])}\n[cyan]⁂[/cyan][b] Cantidad:[/b] {self.cantidad}\n[orange3]⇯[/orange3][b] Peso:[/b] {self.peso}k\n[yellow]➧[/yellow][b] Descripcion:[/b]\n [yellow]{self.descripcion}[/]"
        )
        
        #actualizamos la info del objeto
        view["centrador"]["diagrama"].update(
            Panel(self.diagrama, title="Imagen", style="dodger_blue1")
        )
        
        #actualizamos la info del objeto
        view["centrador"]["descrip"].update(
            Panel(descripcion, title="Descirpcion",style="white")
        )
        
        #panel centrador 
        centra = Layout(Panel(view, style="bright_black"))
        
        #imprimimos el view
        consola.print(centra)
        consola.input("⌬ Presiona cualquier cosita para continuar")
        return
        
#clase para crear objetos consumibles
class consumible(objeto):
    def __init__(self, nombre, descripcion, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}, **keys):
        super().__init__(nombre, descripcion, cantidad, peso, efectos, **keys)
        
    def usar(self, jugador):
        """esta funcion funciona para efectuar el efecto inmediato del objeto consumible, necesita una instancia d ela clase jugador"""
        if jugador:
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    total_vida = jugador.vida + valor
                    if total_vida > jugador.vida_limite:
                        jugador.vida = jugador.vida_limite
                    else:
                        jugador.vida += valor 
                else:
                    print("⌬ No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                consola.print(self.cantidad)
                jugador.extraer_inventario(self, cantidad = 1)
                return Panel(f"⌬ Has usado {self.nombre}", style="exito")
                print(" ")
                
class vestimenta(objeto):
    def __init__(self, nombre, descripcion, tipo, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0, "carga":0}, **keys):
        super().__init__(nombre, descripcion, cantidad, peso, efectos, **keys)
        self.tipo = tipo
        
    def vestir(self, jugador):
        """esta funcion sirve para equipar el objeto en el jugador"""
        if jugador:
            #esto solo aplica los efectos en el personaje
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    jugador.vida += valor
                    #si o si agrandar el limite de vida
                    jugador.vida_limite += valor
                elif efecto == "defensa":
                    jugador.habilidades["defender"] += valor
                elif efecto == "ataque":
                    jugador.habilidades["atacar"] += valor
                elif efecto == "carga":
                    jugador.limite_inventario += valor
                        
                else:
                    print("⌬ No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                #sacamos el objeto del inventario normal y  lo pasamos al inventario de equipo
                resultado = jugador.agregar_vestimenta(self)
                if resultado == True:
                    jugador.extraer_inventario(self)
                    return Panel(f"⌬ Has equipado {self.nombre}", style="exito")
                else:
                    return resultado
    
    def desequipar(self, jugador):
        if jugador:
            #esto solo aplica los efectos en el personaje
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    #si o si agrandar el limite de vida
                    jugador.vida_limite = jugador.vida_limite - valor
                    #y tambien restar la vida extra
                    jugador.vida -= valor 
                    if jugador.vida < 0:
                        jugador.vida = 1
                elif efecto == "defensa":
                    jugador.habilidades["defender"] -= valor
                elif efecto == "ataque":
                    jugador.habilidades["atacar"] -= valor
                elif efecto == "carga":
                    jugador.limite_inventario -= valor
                else:
                    print("⌬ No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                #sacamos el objeto del inventario normal y  lo pasamos al inventario de equipo
                jugador.extraer_vestimenta(self)
                jugador.agregar_inventario(self)
                print(f"⌬ Has desequipado {self.nombre}")
                print(" ")
            
            
#clase encargada de los contenedores
class contenedor:
    def __init__(self, nombre,descripcion:str="", contenido:list=[], cantidad:int=1):
        self.nombre = nombre
        self.contenido = contenido
        self.descripcion = descripcion
        self.cantidad = cantidad

    def describir(self):
        """esta funcion da una descripcion del contenedor"""
        return Panel(f"⌬ [white]{self.descripcion}[/]", title="Descripcion de contenedor", style="green4")

    def abrir(self, jugador):
        """esta funcion imprime el contenido del contenedor y ver si quiere salir o no del panel del cofre para que agarre algo o lo deje"""
        limpiar_consola()
        
        #gui
        view=Layout()
        
        #seccionamos 
        view.split_column(
            Layout(name="response", size=3, visible=False),
            Layout(name="descrip", size=4),
            Layout(name="conten", size=24)
        )
        
        view["conten"].split_row(
            Layout(name="e-inven"),
            Layout(name="p-inven")
        )
            
        centra = Layout(Panel(view, style="bright_black"))
        
        while True:
            #mostramos la info
            view["descrip"].update(self.describir())
            
            #contenido del cofre
            text_entidad = f"⌬ Contenido de {self.nombre}:\n"
            if self.contenido:
                for item in self.contenido:
                    if item.cantidad == 1:
                        text_entidad += f"[yellow]❂[/] [white]{item.nombre}[/]\n"
                    else:
                        text_entidad += f"[yellow]❂[/] [white]{item.nombre} (x{item.cantidad})[/]"
            else:
                text_entidad = "[bright_black]⌬ No tienes nada en tu inventario[/]"
            
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
            view["conten"]["e-inven"].update(Panel(Text.from_markup(text_entidad), style="dodger_blue2", title="Contenido del Contenedor"))
            
            #inventario del jugador
            view["conten"]["p-inven"].update(Panel(Text.from_markup(text_player), style="orange3",title="Tu inventario", subtitle=f"{jugador.peso_inventario}g/{jugador.limite_inventario}g", subtitle_align="right"))
            
            #imprimimos el layout 
            consola.print(centra)
                
            #preguntamos por la accion
            comando = str(input("➥ ") ).lower().split()
            
            if not comando:
                view["response"].update(Panel(f"⌬ Escribe una accion valida.", style="alert"))
                view["response"].visible = True
                continue
            
            match comando[0]:
                case "tomar":
                    if len(comando) > 1:
                        #toma todo el contenido del cofre
                        if comando[1] == "*":
                            items = self.contenido[:]  # copia
                            for item in items:
                                if jugador.agregar_inventario(item):
                                    self.extraer(item)
                                else:
                                    print("algo salo mal")
                                    break
                            else:
                                view["response"].update(Panel(f"⌬ has tomado todo.", style="exito"))
                                view["response"].visible = True
                            continue
                            
                        #toma deacuerdo al nombre escrito
                        for item in self.contenido:
                            if comando[1] == "cofre":
                                limpiar_consola()
                                print("⌬ No puedes tomar un cofre")
                                print(" ")
                                continue
                            elif item.nombre.lower() == comando[1]:
                                if jugador.agregar_inventario(item):
                                    self.extraer(item)
                                    view["response"].update(Panel(f"⌬ Has tomado {item.nombre}.", style="exito"))
                                    view["response"].visible = True
                                    break
                                else:
                                    break
                        else:
                            view["response"].update(Panel(f"⌬ No hay {comando[1]} aqui.", style="info"))
                            view["response"].visible = True
                    else:
                        view["response"].update(Panel("⌬ Debes especificar que quieres tomar", style="info"))
                        view["response"].visible = True
                case "dejar":
                    if len(comando) > 1:
                        for item in jugador.inventario:
                            if item.nombre.lower() == comando[1]:
                                self.agregar(item)
                                jugador.extraer_inventario(item)
                                view["response"].update(Panel(f"⌬ Has dejado {item.nombre}", style="info"))
                                view["response"].visible = True
                                break
                        else:
                            view["response"].update(Panel(f"⌬ No tienes {comando[1]} en tu inventario", style="info"))
                            view["response"].visible = True
                    else:
                        view["response"].update(Panel(f"⌬ Debes especificar que quieres dejar", style="info"))
                        view["response"].visible = True
                case "inventario":
                    limpiar_consola()
                    result = jugador.mostrar_inventario()
                    if isinstance(result, Panel):
                        view["response"].update(result)
                        view["response"].visible = True      
                case "salir":
                    limpiar_consola()
                    break
                case _:
                    view["response"].update(Panel(f"⌬ Debes digitar un comando valido.", style="info"))
                    view["response"].visible = True
                    continue

    def agregar(self, objeto):
        """esta funcion agrega uno o varios objetos al contenedor, en caso de varios debe ser una lista"""
        if isinstance(objeto, list):
            for nuevo_item in objeto:
                for item in self.contenido:
                    if item.nombre == nuevo_item.nombre:
                        item.cantidad += nuevo_item.cantidad
                        break
                else:
                    self.contenido.append(nuevo_item)
        else:
            for item in self.contenido:
                if item.nombre == objeto.nombre:
                    item.cantidad += objeto.cantidad
                    break
            else:
                self.contenido.append(objeto)
    
    def extraer(self, objeto):
        """esta funcion elimina un objeto del contenedor"""
        for item in self.contenido:
            if item.nombre == objeto.nombre:
                if item.cantidad > objeto.cantidad:
                    item.cantidad -= objeto.cantidad
                elif item.cantidad == objeto.cantidad:
                    self.contenido.remove(item)
                else:
                    print(f"No tienes suficiente cantidad de {objeto.nombre} en tu inventario")
                break
    
    def extraer_todos(self, objeto):
        """esta funcion elimina todos los objetos del contenedor"""
        for item in self.contenido:
            if item.nombre == objeto.nombre:
                self.contenido.remove(item)
                break
            
    def llenar(self, objeto, calidad:str=["malo", "normal", "bueno", "excelente"]):
        """esta funcion llenara el cofre de manera alazar deacuerdo a su calidad"""
        pass
        #malo_list = [espada, escudo, hacha, lanza, casco, coraza, botas, guantes]
        #normal_list = [casco_cuero, coraza_cuero, botas_cuero, guantes_cuero]
        #bueno_list = [orbe_verde, orbe_rojo, baston_curativo]
        #excelente_list = [monedax10, monedax5, monedax2, moneda, orbe]
        
        match calidad:
            case "malo":
                pass
                
#creamos la clase cofres
class cofre(contenedor):
    def __init__(self, nombre="Cofre", descripcion:str="Un cofre de madera y chapa de metal gastado, muy comun", contenido:list=[], cantidad:int=1):
        super().__init__(nombre, descripcion, contenido, cantidad)
class cofre_madera(cofre):
    def __init__(self, nombre="Cofre_madera", descripcion:str="Un cofre de madera antigua y refinada, algo gastada pero de un valor historico bastante grande", contenido:list=[], cantidad:int=1):
        super().__init__(nombre, descripcion, contenido, cantidad)
#creamos la clase armario
class armario(contenedor):
    def __init__(self, nombre:str="Armario", descripcion:str="Un armario que almacena prendas para la vida cotidiana", contenido:list=[], cantidad:int=1):
        super().__init__(nombre, descripcion, contenido, cantidad)
        



#creamos objetos magicos
orbe_verde = objeto("Orbe verde", "objeto magico con modificador estadistico", efectos={"vida":10})
orbe_rojo = objeto("Orbe rojo", "objeto magico con modificador estadistico", efectos={"vida":-5, "ataque": 8, "defensa":2})
baston_curativo = objeto("Baston_curativo", "Un baston de madera antiguo que rebosa de vida.", efectos={"vida":5})

#objetos generales que son acumulables
monedax10 = objeto("moneda", "una moneda de oro", 10, peso=0.1)
monedax5 = objeto("moneda", "una moneda de oro", 5, peso=0.5)
monedax2 = objeto("moneda", "una moneda de oro", 2, peso=0.2)
moneda = objeto("moneda", "una moneda de oro", peso=0.1)
orbe = objeto("orbe", "un orbe de poder")


#elementos de guerra
espada_madera = vestimenta("Espada_madera", "Una espada de madera, un arma solida de defenza precaria","arma", efectos={"ataque":3}, peso=2, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "espada.png")))
espada_metal = vestimenta("Espada_metal", "Una espada de metal gastado, un arma simple de defenza precaria","arma", efectos={"ataque":5}, peso=3, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "espada.png")))
espada_acero = vestimenta("Espada_acero", "Una espada de acero filosa y de calidad normla, muy comun en soldados y guardias","arma", efectos={"ataque":7}, peso=7, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "espada.png")))
espada_ebano = vestimenta("Espada_ebanoo", "Una espada de Ebano muy rara y tipica de la segunda era, con un filo espectacular, pero peso extremo","arma", efectos={"ataque":13}, peso=10, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "espada.png")))

escudo = vestimenta("Escudo", "Un escudo de madera","escudo", efectos={"defensa":10}, peso=4, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "escudo.png")))
hacha = vestimenta("Hacha", "Un hacha de guerra","arma", efectos={"ataque":8}, peso=3, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "hacha_normal.png")))
lanza = vestimenta("Lanza", "Una lanza de hierro","arma", efectos={"ataque":6}, peso=2.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "lanza.png")))

#armaduras hierro
casco = vestimenta("Casco_hierro", "Un casco de hierro","casco", efectos={"defensa":3}, peso=4.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "casco_hierro.png")))
coraza = vestimenta("Coraza_hierro", "Una coraza de hierro", "coraza", efectos={"defensa":6}, peso=10, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "coraza_hierro.png")))
pantalones = vestimenta("Pantalones_hierro", "Pantalones de hierro","pantalones", efectos={"defensa":5}, peso=8, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "pantalon_hierro.png")))
botas = vestimenta("Botas_hierro", "Botas de hierro","botas", efectos={"defensa":4}, peso=19, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "botas_hierro.png")))
guantes = vestimenta("Guantes_hierro", "Guantes de hierro", "guantes", efectos={"defensa":3}, peso=4.8, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "guantes_hierro.png")))

#armaduras cuero
casco_cuero = vestimenta("Casco_cuero", "Un casco de cuero con poca defenza pero util para trabajo ligero.","casco", efectos={"defensa":2}, peso=2.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "casco_cuero.png")))
coraza_cuero = vestimenta("Coraza_cuero", "Una coraza de cuero con poca defenza pero util para trabajo ligero.","coraza", efectos={"defensa":4}, peso=7.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "coraza_cuero.png")))
pantalones_cuero = vestimenta("Pantalones_cuero", "Pantalones de cuero con poca defenza pero util para trabajo ligero.","pantalones", efectos={"defensa":3}, peso=5,  diagrama=imagen_assci(os.path.join(vestimentas_ruta, "pantalon_cuero.png")))
botas_cuero = vestimenta("Botas_cuero", "Botas de cuero con poca defenza pero util para trabajo ligero.","botas", efectos={"defensa":2}, peso=2, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "botas_cuero.png")))
guantes_cuero = vestimenta("Guantes_cuero", "Guantes de cuero con poca defenza pero util para trabajo ligero.","guantes", efectos={"defensa":1}, peso=1.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "guantes_cuero.png")))

#armaduras plata
casco_plata = vestimenta("Casco_plata", "Un casco de plata bien forjado, usado en las guerras antiguas.","casco", efectos={"defensa":2}, peso=2.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "casco_plata.png")))
coraza_plata = vestimenta("Coraza_plata", "Una coraza de plata, bien forjado, usado en las guerras antiguas.","coraza", efectos={"defensa":4}, peso=7.5)
pantalones_plata = vestimenta("Pantalones_plata", "Pantalones de plata, bien forjado, usado en las guerras antiguas.","pantalones", efectos={"defensa":3}, peso=5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "pantalon_hierro.png")))
botas_plata = vestimenta("Botas_plata", "Botas de plata, bien forjado, usado en las guerras antiguas.","botas", efectos={"defensa":2}, peso=2, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "botas_hierro.png")))
guantes_plata = vestimenta("Guantes_plata", "Guantes de plata, bien forjado, usado en las guerras antiguas.","guantes", efectos={"defensa":1}, peso=1.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "guantes_hierro.png")))

#armaduras opalo
casco_opalo = vestimenta("Casco_opalo", "Un casco de opalo, este minerar es la cuspide economica intercambiada entre legendas, su escases y raresa lo hacen un materias de profunda calidad", "casco", efectos={"defensa":2}, peso=2.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "casco_opalo.png")))

coraza_opalo = vestimenta("Coraza_opalo", "Una coraza de opalo, este minerar es la cuspide economica intercambiada entre legendas, su escases y raresa lo hacen un materias de profunda calidad de coraza", "coraza",efectos={"defensa":4}, peso=7.5)

pantalones_opalo = vestimenta("Pantalones_opalo", "Pantalones de opalo, este minerar es la cuspide economica intercambiada entre legendas, su escases y raresa lo hacen un materias de profunda calidad de pantalones","pantalones", efectos={"defensa":3}, peso=5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "pantalon_hierro.png")))

botas_opalo = vestimenta("Botas_opalo", "Botas de opalo, este minerar es la cuspide economica intercambiada entre legendas, su escases y raresa lo hacen un materias de profunda calidad botas", "botas", efectos={"defensa":2}, peso=2, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "botas_hierro.png")))

guantes_opalo = vestimenta("Guantes_opalo", "Guantes de opalo, este minerar es la cuspide economica intercambiada entre legendas, su escases y raresa lo hacen un materias de profunda calidad de guantes", "guantes",efectos={"defensa":1}, peso=1.5, diagrama=imagen_assci(os.path.join(vestimentas_ruta, "guantes_hierro.png")))


#mochilas
mochila_pequeña = vestimenta("Mochila_pequeña", "Una mochila de cuero con espacio pequeño cabria un perro.", "mochila", 1, peso=4.5, efectos={"carga":15}, diagrama=imagen_assci(os.path.join(objetos_ruta, "mochilas", "mochila_1.png")))
mochila_mediana = vestimenta("Mochila_mediana", "Una mochila de cuero mediana cuyo carisma permite almacenar un cuerpo sin cabeza sin problema", "mochila", 1, peso=6.5, efectos={"vida":10,"carga":28}, diagrama=imagen_assci(os.path.join(objetos_ruta, "mochilas", "mochila_2.png"), stilos="deep_sky_blue1"))
mochila_grande = vestimenta("Mochila_grande", "Una mochila de cuero y estibas de madera despegables digna de un maestro explorador e ingeniero capaz de lugar comprimir espacio suficiente para todas tus aventuras", "mochila", 1, peso=8.5, efectos={"carga":40}, diagrama=imagen_assci(os.path.join(objetos_ruta, "mochilas", "mochila_3.png")))
mochila_agujero = vestimenta("Mochila_cosmica", "Aberracion natural que ha traido tencion a la misma realidad creada por el demonio khemer en las montañas rocosas de Rivendeile, te entra esta realidad y la otra", "mochila", 1, peso=18, efectos={"carga":100}, diagrama=imagen_assci(os.path.join(objetos_ruta, "mochilas", "mochila_cosmica.png")))

#consimibles de vida
pocion_vida = consumible("Pocion_vida", "Una pocion de vida", efectos={"vida":20}, peso=1.5)
manzana = consumible("Manzana", "Una manzana fresca", efectos={"vida":5}, peso=0.5)
zanahoria = consumible("Zanahoria", "Una zanahoria fresca", efectos={"vida":3}, peso=0.2)



if __name__ == "__main__":
    monedax10 = objeto("moneda", "una moneda de oro", 10)
    monedax5 = objeto("moneda", "una moneda de oro", 5)
    monedax2 = objeto("moneda", "una moneda de oro", 2)
    moneda = objeto("moneda", "una moneda de oro")
    orbe = objeto("orbe", "un orbe de poder")
    print(isinstance(manzana, consumible))

