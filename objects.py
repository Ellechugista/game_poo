from utils import *
class objeto:
    def __init__(self, nombre, descripcion, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        self.nombre = nombre
        self.descripcion = descripcion
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
        print(" ")
        print("------------■ Descripcion del objeto ■------------")
        print(f"○Nombre: {self.nombre}")
        print(f"►Descripcion: {self.descripcion}")
        print(f"↨Efectos: {self.efectos}")
        print(f"Cantidad: {self.cantidad}")
        print(f"Peso: {self.peso}")
        print("-------------------------------------------------")
        print(" ")
        
#clase para crear objetos consumibles
class consumible(objeto):
    def __init__(self, nombre, descripcion, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        super().__init__(nombre, descripcion, cantidad, peso, efectos)
        
    def usar(self, jugador):
        """esta funcion funciona para efectuar el efecto inmediato del objeto consumible, necesita una instancia d ela clase jugador"""
        if jugador:
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    jugador.vida += valor
                else:
                    print("⌘No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                jugador.extraer_inventario(self)
                print(f"⌘Has usado {self.nombre}")
                print(" ")
                
class vestimenta(objeto):
    def __init__(self, nombre, descripcion, tipo, cantidad:int=1, peso:float=1, efectos:dict={"ataque":0, "defensa":0, "vida":0}):
        super().__init__(nombre, descripcion, cantidad, peso, efectos)
        self.tipo = tipo
        
    def vestir(self, jugador):
        """esta funcion sirve para equipar el objeto en el jugador"""
        if jugador:
            #esto solo aplica los efectos en el personaje
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    jugador.vida += valor
                elif efecto == "defensa":
                    jugador.habilidades["defender"] += valor
                elif efecto == "ataque":
                    jugador.habilidades["atacar"] += valor
                else:
                    print("⌘No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                #sacamos el objeto del inventario normal y  lo pasamos al inventario de equipo
                
                if jugador.agregar_vestimenta(self):
                    jugador.extraer_inventario(self)
                print(f"⌘Has equipado {self.nombre}")
                print(" ")
    
    def desequipar(self, jugador):
        if jugador:
            #esto solo aplica los efectos en el personaje
            for efecto, valor in self.efectos.items():
                if efecto == "vida":
                    jugador.vida -= valor
                elif efecto == "defensa":
                    jugador.habilidades["defender"] -= valor
                elif efecto == "ataque":
                    jugador.habilidades["atacar"] -= valor
                else:
                    print("⌘No tiene efectos este objeto.")
                    print(" ")
                    break
            else:
                #sacamos el objeto del inventario normal y  lo pasamos al inventario de equipo
                jugador.extraer_vestimenta(self)
                jugador.agregar_inventario(self)
                print(f"⌘Has desequipado {self.nombre}")
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
        print(f"⌘{self.descripcion}")

    def abrir(self, jugador):
        """esta funcion imprime el contenido del contenedor y ver si quiere salir o no del panel del cofre para que agarre algo o lo deje"""
        limpiar_consola()
        while True:
            #mostramos la info
            self.describir()
            print(" ")
            print(f"☺Contenido de {self.nombre}")
            if self.contenido:
                for item in self.contenido:
                    if item.cantidad == 1:
                        print(f"- {item.nombre}")
                    else:
                        print(f"- {item.nombre} (x{item.cantidad})")
            else:
                print("⌘No hay nada aqui.")
                print(" ")
                
            print(" ")
            #aqui debera escribir que desea hacer con el contenido
            comando = str(input("> ")).lower().split()
            match comando[0]:
                case "tomar":
                    if len(comando) > 1:
                        for item in self.contenido:
                            if comando[1] == "cofre":
                                limpiar_consola()
                                print("⌘No puedes tomar un cofre")
                                print(" ")
                                continue
                            elif item.nombre.lower() == comando[1]:
                                if jugador.agregar_inventario(item):
                                    self.extraer(item)
                                    limpiar_consola()
                                    print(f"⌘Has tomado {item.nombre}")
                                    print(" ")
                                    break
                        else:
                            limpiar_consola()
                            print(f"⌘No hay {comando[1]} aqui")
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar que quieres tomar")
                        print(" ")
                case "dejar":
                    if len(comando) > 1:
                        for item in jugador.inventario:
                            if item.nombre.lower() == comando[1]:
                                self.agregar(item)
                                jugador.extraer_inventario(item)
                                limpiar_consola()
                                print(f"⌘Has dejado {item.nombre}")
                                break
                        else:
                            limpiar_consola()
                            print(f"⌘No tienes {comando[1]} en tu inventario")
                            print(" ")
                    else:
                        limpiar_consola()
                        print("⌘Debes especificar que quieres dejar")
                        print(" ")
                case "inventario":
                    limpiar_consola()
                    jugador.mostrar_inventario() 
                case "salir":
                    limpiar_consola()
                    break
                case _:
                    limpiar_consola()
                    print("⌘Que es lo que quieres hacer?")
                    print(" ")

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
        malo_list = [espada, escudo, hacha, lanza, casco, coraza, botas, guantes]
        normal_list = [casco_cuero, coraza_cuero, botas_cuero, guantes_cuero]
        bueno_list = [orbe_verde, orbe_rojo, baston_curativo]
        excelente_list = [monedax10, monedax5, monedax2, moneda, orbe]
        
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
espada = vestimenta("Espada", "Una espada de acero","arma", efectos={"ataque":5}, peso=2)
escudo = vestimenta("Escudo", "Un escudo de madera","escudo", efectos={"defensa":10}, peso=4)
hacha = vestimenta("Hacha", "Un hacha de guerra","arma", efectos={"ataque":8}, peso=3)
lanza = vestimenta("Lanza", "Una lanza de hierro","arma", efectos={"ataque":6}, peso=2.5)

#armaduras hierro
casco = vestimenta("Casco_hierro", "Un casco de hierro","casco", efectos={"defensa":3}, peso=4.5)
coraza = vestimenta("Coraza_hierro", "Una coraza de hierro", "coraza", efectos={"defensa":6}, peso=10)
pantalones = vestimenta("Pantalones_hierro", "Pantalones de hierro","pantalones", efectos={"defensa":5}, peso=8)
botas = vestimenta("Botas_hierro", "Botas de hierro","botas", efectos={"defensa":4}, peso=19)
guantes = vestimenta("Guantes_hierro", "Guantes de hierro", "guantes", efectos={"defensa":3}, peso=4.8)
#armaduras cuero
casco_cuero = vestimenta("Casco_cuero", "Un casco de cuero","casco", efectos={"defensa":2}, peso=2.5)
coraza_cuero = vestimenta("Coraza_cuero", "Una coraza de cuero","coraza", efectos={"defensa":4}, peso=7.5)
pantalones_cuero = vestimenta("Pantalones_cuero", "Pantalones de cuero","pantalones", efectos={"defensa":3}, peso=5)
botas_cuero = vestimenta("Botas_cuero", "Botas de cuero","botas", efectos={"defensa":2}, peso=2)
guantes_cuero = vestimenta("Guantes_cuero", "Guantes de cuero","guantes", efectos={"defensa":1}, peso=1.5)

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

