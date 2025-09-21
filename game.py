# -*- coding: utf-8 -*-
# archivo principal
from lugares import *
from personajes import *
from player import *
from batallas import *
from utils import *
from misiones import *
import time
import pickle
#render
from rich.panel import Panel
from rich.table import Table


#clase madre donde el flujo del juego se desarrolla, aqui se manejan los objetos y el flujo del juego
class Game:
    def __init__(self):
        self.player = player("Mariano", casa, 100, habilidades = {"atacar": 100, "defender": 100}, control_juego=self)
        self.enemigos_derrotados = 0
        self.registros_batallas = []
        self.version = "0.1.7"
        
    def guardar_datos(self, name_file = "datos.pkl"):
        """guarda los datos del juego"""
        #verifica si existe la carpeta saves
        #si no existe la crea
        path = os.path.dirname(os.path.abspath(__file__))
        
        if not os.path.exists(os.path.join(path, "saves")):
            os.makedirs(os.path.join(path, "saves"))

        carpeta_saves = os.path.join(path, "saves")
        
        # Guardamos los datos del juego y las entidades
        datos_game = {
            "estado_game": self.__dict__,
            "entidades": [(ent.nombre, ent.__dict__) for ent in RegistroEntidades.obtener_todos()], #esta linea magica hace muchas cosas raras, pero por cada entidad dentro del registro de entidades, va a crear una dupla de datos con el nombre d ela entidad y su diccionario de atributos, lo que guarda toda la info delos personajes
            "lugares": [(lugar.nombre, lugar.__dict__) for lugar in RegistroLugares.obtener_todos()],
        }
        
        #nombre de archivo con la fecha y hora actual
        date_file = time.strftime("%Y-%m-%d", time.localtime())
        nombre_archivo = os.path.join(carpeta_saves, date_file + "_" + name_file)
        
        # Guardamos en un archivo
        with open(nombre_archivo, "wb") as f:
            pickle.dump(datos_game, f)
        
        bar_carga(2, "⌬ Guardando datos...")
        
        consola.print("⌬ Datos guardados")
         
        
    def cargar_datos(self):
        """carga los datos del juego"""
        #verifica si existe la carpeta saves
        #si no existe la crea
        path = os.path.dirname(os.path.abspath(__file__))
        
        if not os.path.exists(os.path.join(path, "saves")):
            consola.print("⌬ No hay archivos de guardado")
             
            return False

        carpeta_saves = os.path.join(path, "saves")
        archivos = os.listdir(carpeta_saves)
        
        #aqui se imprimen los archivos disponibless para cargar
        consola.clear()
        
        tabla_archivos = Table(title="Archivos de guardado disponibles", style="info")
        tabla_archivos.add_column("👁", justify="left", style="dark_green bold")
        tabla_archivos.add_column("Nombre de archivo", justify="left", style="bold cyan")
        tabla_archivos.add_column("Fecha", justify="right", style="bold")

        for archivo in archivos:
            tabla_archivos.add_row("⌬", archivo, archivo[:10])
        
        consola.print(tabla_archivos)
        
         
        consola.print("⌬ Cual archivo quieres cargar?")
        nombre_archivo = str(consola.input("➥ ") ).lower()
        if nombre_archivo.endswith(".pkl"):
            nombre_archivo = nombre_archivo[:-4]
        
        #si decidio eliminarlo de la carpeta
        if nombre_archivo.startswith("del"):
            nombre_archivo = nombre_archivo[3:]
            #procedemos a eliminar
            consola.clear()
            os.remove(os.path.join(carpeta_saves, nombre_archivo + ".pkl"))
            return Panel(f"⌬ Partida [bold]{nombre_archivo}[/bold] eliminada CORRECTAMENTE", style="alert")
            
        
        archivo = os.path.join(carpeta_saves, nombre_archivo + ".pkl")
        if not os.path.isfile(archivo):
            return Panel("⌬ El archivo no existe.", style="info")

        consola.clear()
        consola.print("⌬ Inicio proceso de carga")
         
        try:
             # Cargamos los datos
            with open(archivo, "rb") as f:
                datos = pickle.load(f)
                
            # 1. Primero restauramos los personajes
            for entidad_nombre, atributos in datos["entidades"]:
                # Buscamos si ya existe
                if entidad_nombre in RegistroEntidades._entidades:
                    entidad_existente = RegistroEntidades._entidades[entidad_nombre]
                    entidad_existente.__dict__.update(atributos)  # Actualizamos sus atributos (vida, nombre, etc.)
                else:
                    # Si no existe (raro), lo creamos, no deberia pasar ya que el nombre es exacto he inigualable si suscede se podria duplicar el personaje :(
                    nueva_entidad = entidad(
            nombre=atributos["nombre"],
            dialogos=atributos.get("dialogos", {}),
            vida=atributos["vida"],
            descripcion=atributos.get("descripcion"),
            rutinas=atributos.get("rutinas"),
            nivel_combate=atributos.get("nivel_combate", 4),
            habilidades=atributos.get("habilidades", {"atacar": 5, "defender": 5}),
            animo=atributos.get("animo", 50)
        )
                    nueva_entidad.__dict__.update(atributos)
            #2. Luego restauramos los lugares
            for lugar_nombre, atributos in datos["lugares"]:
                # Buscamos si ya existe
                if lugar_nombre in RegistroLugares._lugar:
                    lugar_existente = RegistroLugares._lugar[lugar_nombre]
                    lugar_existente.__dict__.update(atributos)
                else:
                    #si existe que no deberia
                    nuevo_lugar = lugar(
                        nombre = atributos.get("nombre"),
                        descripcion = atributos.get("descripcion"),
                        presentes = atributos.get("presentes"),
                        objetos = atributos.get("objetos"),
                        conexiones = atributos.get("conexiones"),
                        bloqueado = atributos.get("bloqueado"),
                        razon = atributos.get("razon"),
                    )
                    nuevo_lugar.__dict__.update(atributos)
                    
             #3. Luego restauramos el juego
            self.__dict__.update(datos["estado_game"])
            
            bar_carga(3,"⌬ Cargando datos...")      
            consola.print("⌬ Datos cargados correctamente.")
             
            return True
        except FileNotFoundError:
            consola.print("⌬ No se encontró un archivo de guardado. Iniciando un nuevo juego.")
             
            return False
        except EOFError:
            consola.print("⌬ El archivo de guardado está vacío. Iniciando un nuevo juego.")
             
            return False
        except pickle.UnpicklingError:
            consola.print("⌬ Error al cargar el archivo de guardado. El archivo puede estar corrupto.")
             
            return False
        except AttributeError:
            consola.print("⌬ Error al cargar los datos. Asegúrate de que el archivo de guardado sea compatible.")
             
            return False
        except TypeError:
            consola.print("⌬ Error al cargar los datos. Asegúrate de que el archivo de guardado sea compatible.")
             
            return False
        except Exception as e:
            consola.print(f"⌬ Error al cargar los datos: {e}")
             
            return False
        
    def save_registro_batalla(self, batalla):
        """guarda el registro de la batalla"""
        consola.print("⌬ Guardando registro de batalla...")
         
        self.registros_batallas.append(batalla)
        consola.print("⌬ Batalla guardada")
         
    
    def mostrar_registros_batallas(self):
        """muestra el registro de batallas"""
        consola.clear()
        
        #gui
        view = Layout()
        
        view.split_column(
            Layout(name="conten")
        )
        
        lista = []
        
        if self.registros_batallas: 
            for batalla in self.registros_batallas[-4:]:
                lista.append(batalla.informe_batalla())   
        else:
            return Panel("⌬ No hay registros de batallas", style="alert")
        
        # Agrupamos los panels
        content = Group(*lista)
        view["conten"].update(content)
        
        #centrador
        centra = Layout(Panel(view, style="bright_black"))
        
        consola.print(centra)   
         
        consola.input("⌬ Presiona cualquier cosita para continuar")
        
    def menu(self):
        #menu principal
        consola.clear()
        
        #layout GUI
        contenido = Layout(name="contenido")
        contenido.split_column(
            Layout(name="response", size=3 ,visible=False),
            Layout(name="menu")
        )
        
        contenido["menu"].split_column(
            Layout(name="titulo", size=10),
            Layout(name="opciones")
        )
        
        #partimos opciones para añadir un diagrama
        contenido["menu"]["opciones"].split_row(
            Layout(name="seleccion"),
            Layout(name="diagrama", size=80)
        )
        
        
        view =Layout(Panel(contenido, title="Bienvenido".upper(), subtitle="By [green]ellechugista[/]", subtitle_align="right"))
        
        while True:
            #actualizamos el contenido GUI
            contenido["menu"]["titulo"].update(Panel(Text(r"""+==========================================================================+
|     ██████╗  █████╗ ███╗   ███╗███████╗    ██████╗  ██████╗  ██████╗     |
|    ██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔══██╗██╔═══██╗██╔═══██╗    |
|    ██║  ███╗███████║██╔████╔██║█████╗█████╗██████╔╝██║   ██║██║   ██║    |
|    ██║   ██║██╔══██║██║╚██╔╝██║██╔══╝╚════╝██╔═══╝ ██║   ██║██║   ██║    |
|    ╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ██║     ╚██████╔╝╚██████╔╝    |
|     ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝    ╚═╝      ╚═════╝  ╚═════╝     |
+==========================================================================+""", justify="center"), style="b dark_orange3"))
            #panel de informacion
            contenido["menu"]["opciones"]["seleccion"].update(Panel(Text.from_markup(r"""[white]⌬ Iniciar juego 
⌬ Guardar juego 
⌬ Cargar juego
[bright_black]⌬ Salir del juego[/]
⌬ Volver[/]"""), title="Bienvenido al juego de role [green][bold]GAME-POO[/bold][/green]",subtitle=f"V [green]{self.version}[/]",subtitle_align="right", style="cyan"))

            #panel de diagrama
            contenido["menu"]["opciones"]["diagrama"].update(imagen_assci(os.path.join("assets", "paisaje_2.jpg"), 70, "green",justify="center"))
            
            consola.print(view)
            
            comando = str(consola.input("➥ ")).lower().split()
            
            #reiniciamos el response
            contenido["response"].visible= False
            
            if comando[0] == "iniciar":
                
                #actualizamos contenido
                contenido["menu"]["opciones"].update(Panel("⌬ Cual sera el nombre del guerreo?"))
                
                #reinprimimos
                consola.print(view)
                
                nombre = str(consola.input("➥ ")).lower()
                if not nombre:
                    contenido["response"].update(Panel("⌬ Debes especificar un nombre valido a tu personaje"))
                    contenido["response"].visible = True
                    continue
                
                self.player = player(nombre, casa, 100, habilidades = {"atacar": 10, "defender": 10}, nivel_combate=10, control_juego=self)
                consola.clear()
                self.iniciar()
            elif comando[0] == "salir":
                seguro = str(consola.input("⌬ Estas seguro que quieres salir? (si/no) ")).lower()
                if seguro == "si" or seguro == "s":
                    consola.clear()
                    consola.print("⌬ Gracias por jugar")
                    exit()
                elif seguro == "no" or seguro == "n":
                    consola.clear()
                    continue
                else:
                    consola.clear()
                    consola.print("⌬ Comando no valido")
                     
            elif comando[0] == "guardar":
                consola.clear()
                if len(comando) > 1:
                    nombre_archivo = comando[1] + ".pkl"
                else:
                    nombre_archivo = "datos.pkl"
                    
                self.guardar_datos(nombre_archivo)
                
            elif comando[0] == "cargar":
                consola.clear()
                
                cargado = self.cargar_datos()
                if isinstance(cargado, Panel):
                    contenido["response"].update(cargado)
                    contenido["response"].visible = True
                elif cargado == True:
                    self.iniciar()          
                else:
                    contenido["response"].update(Panel("⌬ No se pudo cargar el juego", style="info"))
                    contenido["response"].visible = True
                     
            elif comando[0] == "volver":
                consola.clear()
                break
                    
            else:
                contenido["response"].update(Panel("⌬ Comando no valido", style="info"))
                contenido["response"].visible = True
                 

    def iniciar(self):
        limpiar_consola()
        #aqui se maneja el input del jugador prara ver que  accion quiere hacer dentro de cada escenario y se le muestra la informacion en desarrollo
        
        #GUI consol con rich
        info_panel=Layout()
        
        info_panel.split_column(
            Layout(Panel("Info", style="info"),name="response", size=3, visible=False),
            Layout(name="general", ratio=1)
        )
        
        #panel de informacion
        info_panel["general"].split_row(
            Layout(name="info_lugar", ratio=4),
            Layout(name="estadisticas", ratio=2)
        )
        
        #layout de info lugar
        info_panel["general"]["info_lugar"].split_column(
            Layout(name="descrip_lugar", size=20),
            Layout(name="conexiones", size=8)
        )
        
        #intentamos darle alto a la columna estadisticas
        info_panel["general"]["estadisticas"].split_column(
            Layout(name="estadis_player", size=7),
            Layout(name="misiones", size=21)
        )
        
        view=Layout(Panel(info_panel, subtitle=f"V {self.version}", subtitle_align="right",style="grey46"))
        
        while True:
            lugar_actual = self.player.lugar_actual
            
            #actualizamos el GUI
            #actualizamos descripcion lugar
            info_panel["general"]["info_lugar"]["descrip_lugar"].update(
                lugar_actual.presentar_lugar()
            )
            
            #actualizamos direcciones disponibles
            info_panel["general"]["info_lugar"]["conexiones"].update(
                lugar_actual.presentar_conexiones()
            )
            
            #actualizamos estadisticas de jugador
            info_panel["general"]["estadisticas"]["estadis_player"].update(
                self.player.estadisticas()
            )
            
            #actualizamos estadisticas de jugador
            info_panel["general"]["estadisticas"]["misiones"].update(
                self.player.mostrar_misiones()
            )
            
            #imprimimos el GUI
            consola.print(view)
            
            #preguntamos por la accion
            comando = str(input("➥ ") ).lower().split()
            
            #quitamos las respuesta ya mostradas
            info_panel["response"].visible = False
            
            #validamos que comando no sea none
            if not comando:
                consola.clear()
                consola.print("⌬ Escoje una accion valida.")
                consola.print("")
                continue
                
            match comando[0]:
                case "ir":
                    if len(comando) > 1:
                        resultado = self.player.mover_a(comando[1])
                        if resultado:
                            info_panel["response"].update(resultado)
                            info_panel["response"].visible=True
                    else:
                        info_panel["response"].update(Panel("⌬ Debes especificar a donde quieres ir.", style="info"))
                        #activamos la seccion d einformacion
                        info_panel["response"].visible = True
                case "tomar":
                    consola.clear()
                    info_panel["response"].update(self.player.tomar_objeto(comando[1]))
                    info_panel["response"].visible= True
                case "abrir":
                    if len(comando) > 1:
                        if lugar_actual.objetos:
                            for item in lugar_actual.objetos:
                                if item.nombre.lower() == comando[1]:
                                    item.abrir(self.player)
                                    break
                            else:
                                info_panel["response"](Panel(f"⌬ No hay ningun {comando[1]} para abrir"))
                                 
                    else:
                        consola.clear()
                        consola.print("⌬ Debes espesificar que quieres abrir")
                         
                case "hablar":
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if p.nombre.lower() == comando[1]:
                                    consola.clear()
                                    p.hablar(self.player)
                                    break
                            else:
                                info_panel["response"].update(Panel(f"⌬ No hay nadie llamado {comando[1]}", style="alert"))
                                info_panel["response"].visible = True
                                 
                        else:
                            info_panel["response"].update(Panel("⌬ No hay nadie con quien hablar", style="info"))
                            info_panel["response"].visible = True
                             
                    else:
                        consola.clear()
                        consola.print("⌬ Debes especificar con quien quieres hablar")
                         
                case "inventario":
                    consola.clear()
                    resultado = self.player.mostrar_inventario()
                    if isinstance(resultado, Panel):
                        info_panel["response"].update(resultado)
                        info_panel["response"].visible = True
                case "informacion":
                    consola.clear()
                    if len(comando) > 2:    
                        if self.player.registro_misiones and comando[1] == "mision":
                                id = comando[2]
                                for m in self.player.registro_misiones:
                                    if str(m.id) == id:
                                        m.describir_mision()
                                    else:
                                        info_panel["response"].update(Panel(f"⌬ No existe mision {id} activa.", style="info"))
                                        info_panel["response"].visible = True
                                        break
                        else:
                            info_panel["response"].update(Panel("⌬ No has iniciado misiones.", style = "info"))
                            info_panel["response"].visible = True
                            continue
                        
                    elif len(comando) > 1:
                        if self.player.inventario:
                            for item in self.player.inventario:
                                #consola.print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    #self.player.descrip_objeto(item) old way to do this shit 
                                    item.describir()
                                    break
                            else:
                                info_panel["response"].update(Panel(f"⌬ No tienes {comando[1]} en tu inventario", style="info"))
                                info_panel["response"].visible=True
                                continue
                        else:
                            consola.clear()
                            info_panel["response"].update(Panel("⌬ No tienes nada en tu inventario", style="info")) 
                            info_panel["response"].visible=True
                             
                            continue
                    else:
                        consola.clear()
                        info_panel["response"].update(Panel("⌬ Debes especificar el objeto del que quieres informacion", style="info")) 
                        info_panel["response"].visible=True 
                case "estadisticas":
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if comando[1] == p.nombre.lower():
                                    consola.clear()
                                    p.estadisticas()
                                    break
                            else:
                                info_panel["response"].update(Panel(f"⌬ No hay nadie llamado {comando[1]}", style="info"))
                                info_panel["response"].visible = True
                                 
                        else:
                            info_panel["response"].update(Panel("⌬ No hay nadie para ver sus estadisticas", style="info"))
                            info_panel["response"].visible = True
                             
                case "atacar":
                    #aqui se maneja la batalla
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if comando[1] == p.nombre.lower():
                                    pelea = batalla(self.player, p)
                                    pelea.iniciar()
                                    self.save_registro_batalla(pelea)
                                    self.enemigos_derrotados += 1
                                    break      
                            else:
                                info_panel["response"].update(Panel(f"⌬ No hay nadie llamado {comando[1]}", style="info"))
                                info_panel["response"].visible = True   
                        else:
                            info_panel["response"].update(Panel("⌬ No hay nadie para atacar", style="info"))
                            info_panel["response"].visible = True
                             
                    else:
                        info_panel["response"].update(Panel("⌬ Debes especificar con quien quieres pelear.", style="info"))
                        info_panel["response"].visible = True
                     
                case "registros":
                    resultado = self.mostrar_registros_batallas()
                    if isinstance(resultado, Panel):
                        info_panel["response"].update(resultado)
                        info_panel["response"].visible = True
                case "menu":
                    self.menu()
                case "salir":
                    consola.clear()
                    break
                case _:
                    consola.clear()
                    info_panel["response"].update(Panel("⌬ Comando no valido", style="info"))
                    info_panel["response"].visible = True

    def game_over(self):
        consola.clear()
        consola.print(r"""
 ██████╗  █████╗ ███╗   ███╗███████╗     ██████╗ ██╗   ██╗███████╗██████╗ 
██╔════╝ ██╔══██╗████╗ ████║██╔════╝    ██╔═══██╗██║   ██║██╔════╝██╔══██╗
██║  ███╗███████║██╔████╔██║█████╗      ██║   ██║██║   ██║█████╗  ██████╔╝
██║   ██║██╔══██║██║╚██╔╝██║██╔══╝      ██║   ██║██║   ██║██╔══╝  ██╔══██╗
╚██████╔╝██║  ██║██║ ╚═╝ ██║███████╗    ╚██████╔╝╚██████╔╝███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
""")
        self.player.estadisticas()
        consola.print("")
        consola.print(f"{self.player.nombre} ha fallecido en batalla, como un heroe, ladron, bricon de puesntes, guardia fiel a la prole, o simplemente olgasaneando entre los pueblos del basto reino de Elrond.")
        consola.print("")
        consola.print("ahora solo queda volver a esa gran y maravillosa aventura a la que llamamos vida tu y yo, y bueno espero tu tengas mas que yo, os deseo lo mejor.")
        input("_se despide ellechugista ;)")
        exit()

juego = Game()
      
if __name__ == "__main__":

    juego.menu()
    #juego.iniciar()

