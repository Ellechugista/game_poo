# archivo principal
from lugares import *
from personajes import *
from player import *
from batallas import *
from utils import *
import time
import pickle

#clase madre donde el flujo del juego se desarrolla, aqui se manejan los objetos y el flujo del juego
class game:
    def __init__(self):
        self.player = player("Mariano", casa, 10, habilidades = {"atacar": 8, "defender": 5})
        self.enemigos_derrotados = 0
        self.registros_batallas = []
        
    def guardar_datos(self, name_file = "datos.pkl"):
        """guarda los datos del juego"""
        #verifica si existe la carpeta saves
        #si no existe la crea
        path = os.path.dirname(os.path.abspath(__file__))
        
        if not os.path.exists(os.path.join(path, "saves")):
            os.makedirs(os.path.join(path, "saves"))

        carpeta_saves = os.path.join(path, "saves")
        
        print("⌘Guardando datos...")
        print(" ")
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
        
        print("⌘Datos guardados")
        print(" ")
        
    def cargar_datos(self):
        """carga los datos del juego"""
        #verifica si existe la carpeta saves
        #si no existe la crea
        path = os.path.dirname(os.path.abspath(__file__))
        
        if not os.path.exists(os.path.join(path, "saves")):
            print("⌘No hay archivos de guardado")
            print(" ")
            return False

        carpeta_saves = os.path.join(path, "saves")
        archivos = os.listdir(carpeta_saves)
        
        #aqui se imprimen los archivos disponibless para cargar
        limpiar_consola()
        print("⌘Archivos de guardado disponibles:")
        for archivo in archivos:
            print(f"⌘{archivo}")
        
        print(" ")
        print("⌘Cual archivo quieres cargar? (sin la extencion .pkl)")
        nombre_archivo = str(input("> ")).lower()
        if nombre_archivo.endswith(".pkl"):
            nombre_archivo = nombre_archivo[:-4]
        
        archivo = os.path.join(carpeta_saves, nombre_archivo + ".pkl")
        if not os.path.isfile(archivo):
            print("⌘El archivo no existe.")
            print(" ")
            return False

        print("⌘Cargando datos...")
        print(" ")
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
                            
            print("⌘Datos cargados correctamente.")
            print(" ")
            return True
        except FileNotFoundError:
            print("⌘No se encontró un archivo de guardado. Iniciando un nuevo juego.")
            print(" ")
            return False
        except EOFError:
            print("⌘El archivo de guardado está vacío. Iniciando un nuevo juego.")
            print(" ")
            return False
        except pickle.UnpicklingError:
            print("⌘Error al cargar el archivo de guardado. El archivo puede estar corrupto.")
            print(" ")
            return False
        except AttributeError:
            print("⌘Error al cargar los datos. Asegúrate de que el archivo de guardado sea compatible.")
            print(" ")
            return False
        except TypeError:
            print("⌘Error al cargar los datos. Asegúrate de que el archivo de guardado sea compatible.")
            print(" ")
            return False
        except Exception as e:
            print(f"⌘Error al cargar los datos: {e}")
            print(" ")
            return False
        
    def save_registro_batalla(self, batalla):
        """guarda el registro de la batalla"""
        print("⌘Guardando registro de batalla...")
        print(" ")
        self.registros_batallas.append(batalla)
        print("⌘Batalla guardada")
        print(" ")
    
    def mostrar_registros_batallas(self):
        """muestra el registro de batallas"""
        limpiar_consola()
        print(" ")
        print("⊢---------------------Registros de Batallas----------------------⊣")
        if self.registros_batallas:
            print(" ")
            for batalla in self.registros_batallas:
                batalla.informe_batalla()
        else:
            print("⌘No hay registros de batallas")
            print(" ")
    
    def menu(self):
        #menu principal
        limpiar_consola()
        while True:
            print("⊢---------------------Menu Principal----------------------⊣")
            print("⌘Bienvenido al juego de role GAME-POO")
            print(" ")
            print("⌘Iniciar juego")
            print("⌘Guardar juego")
            print("⌘Cargar juego")
            print("⌘Salir del juego")
            print("⌘Volver")
            print("----------------------------------------------------------⊣")
            print(" ")
            comando = str(input("> ")).lower().split()
            if comando[0] == "iniciar":
                print(" ")
                print("⌘Cual sera el nombre del guerreo?")
                nombre = str(input("> ")).lower()
                self.player = player(nombre, casa, 10, habilidades = {"atacar": 8, "defender": 8})
                limpiar_consola()
                self.iniciar()
            elif comando[0] == "salir":
                seguro = str(input("⌘Estas seguro que quieres salir? (si/no) ")).lower()
                if seguro == "si" or seguro == "s":
                    limpiar_consola()
                    print("⌘Gracias por jugar")
                    print(" ")
                    exit()
                elif seguro == "no" or seguro == "n":
                    limpiar_consola()
                    continue
                else:
                    limpiar_consola()
                    print("⌘Comando no valido")
                    print(" ")

            elif comando[0] == "guardar":
                limpiar_consola()
                if len(comando) > 1:
                    nombre_archivo = comando[1] + ".pkl"
                else:
                    nombre_archivo = "datos.pkl"
                    
                self.guardar_datos(nombre_archivo)
                
            elif comando[0] == "cargar":
                limpiar_consola()
                
                cargado = self.cargar_datos()
                if cargado:
                    self.iniciar()
                else:
                    print("⌘No se pudo cargar el juego")
                    print(" ")
            
            elif comando[0] == "volver":
                limpiar_consola()
                break
                    
            else:
                limpiar_consola()
                print("⌘Comando no valido")
                print(" ")

    def iniciar(self):
        #aqui se maneja el input del jugador prara ver que  accion quiere hacer dentro de cada escenario y se le muestra la informacion en desarrollo
        while True:
            lugar_actual = self.player.lugar_actual
            lugar_actual.presentar_lugar()
            comando = str(input("> ")).lower().split()
            match comando[0]:
                case "ir":
                    self.player.mover_a(comando[1])
                case "tomar":
                    limpiar_consola()
                    self.player.tomar_objeto(comando[1])
                    print(" ")
                case "abrir":
                    if len(comando) > 1:
                        if lugar_actual.objetos:
                            for item in lugar_actual.objetos:
                                if item.nombre.lower() == comando[1]:
                                    item.abrir(self.player)
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No hay ningun {comando[1]} para abrir")
                                print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes espesificar que quieres abrir")
                        print(" ")
                case "hablar":
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if p.nombre.lower() == comando[1]:
                                    limpiar_consola()
                                    p.hablar()
                                    print(" ")
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No hay nadie llamado {comando[1]}")
                                print(" ")
                        else:
                            limpiar_consola()
                            print("⌘No hay nadie con quien hablar")
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar con quien quieres hablar")
                        print(" ")
                case "inventario":
                    limpiar_consola()
                    self.player.mostrar_inventario()
                    print(" ")
                case "informacion":
                    limpiar_consola()
                    if len(comando) > 1:
                        if self.player.inventario:
                            for item in self.player.inventario:
                                #print(item.nombre.lower())
                                if item.nombre.lower() == comando[1].strip():
                                    self.player.descrip_objeto(item)
                                    print(" ")
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
                case "estadisticas":
                    if len(comando) > 1:
                        if lugar_actual.presentes:
                            for p in lugar_actual.presentes:
                                if comando[1] == p.nombre.lower():
                                    limpiar_consola()
                                    p.estadisticas()
                                    print(" ")
                                    break
                            else:
                                limpiar_consola()
                                print(f"⌘No hay nadie llamado {comando[1]}")
                                print(" ")
                        else:
                            limpiar_consola()
                            print("⌘No hay nadie para ver sus estadisticas")
                            print(" ")
                    else:
                        limpiar_consola()
                        self.player.estadisticas()
                        print(" ")
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
                                    print(" ")
                                else:
                                    limpiar_consola()
                                    print(f"⌘No hay nadie llamado {comando[1]}")
                                    print(" ")
                        else:
                            limpiar_consola()
                            print("⌘No hay nadie para atacar")
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar con quien quieres pelear.")
                        print(" ")
                case "registros":
                    self.mostrar_registros_batallas()
                case "menu":
                    self.menu()
                case "salir":
                    break
                case _:
                    limpiar_consola()
                    print("⌘Comando no valido")
                    print(" ")

if __name__ == "__main__":
    juego = game()
    #juego.menu()
    juego.iniciar()

